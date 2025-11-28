# Import python packages
import shutil
import sys
import warnings
import logging
import uuid
import os

# Suppress all warnings
warnings.filterwarnings('ignore')
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
logging.getLogger('google_genai.types').setLevel(logging.ERROR)
logging.getLogger('google.adk').setLevel(logging.ERROR)

# Gemini packages
from google.genai import types

# MCP and ADK packages
from mcp import StdioServerParameters
from google.adk.agents import LlmAgent, Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner, InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

print("✅ Components imported successfully.")

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


# Setup retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

print(f"✅ Retry configuration setp")


# Locate biomcp and configure BioMCP mcp tool
def find_biomcp():
    """Locate biomcp executable."""
    biomcp_path = shutil.which("biomcp")
    if not biomcp_path:
        possible_paths = [
            os.path.join(sys.prefix, "bin", "biomcp"),
            os.path.join(os.path.dirname(sys.executable), "biomcp"),
            os.path.expanduser("~/.local/bin/biomcp")
        ]
        for path in possible_paths:
            if os.path.exists(path):
                biomcp_path = path
                break

        if biomcp_path:
            print(f"Using BioMCP at: {biomcp_path}")

        else:
            print("⚠️ biomcp not found - run !pip install biomcp-python")

    print(f"✅ BioMCP loaded and located in path: {biomcp_path}")
    return biomcp_path


# Configure BioMCP MCP tool
biomcp_path = find_biomcp()

if not biomcp_path:
    raise RuntimeError("biomcp executable not found. Please install with: pip install biomcp-python")

mcp_bio_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=biomcp_path,
            args=["run"],
            env={"MCP_LOG_LEVEL": "debug"}
        ),
        timeout=120,
    )
)

print(f"✅ Created BioMCP mcp tool")


# Pausable preference function tool
def get_output_preference(tool_context: ToolContext) -> dict:
    """Ask user for output preference."""
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint="Would you like 'comprehensive' (detailed summaries + references) or 'simple' (article only) output?",
            payload={"preference_type": "output_format"}
        )
        return {
            "status": "pending",
            "message": "Waiting for user preference..."
        }
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "confirmed",
            "message": "User preference received."
        }
    else:
        return {
            "status": "rejected",
            "message": "User cancelled."
        }


def exit_loop():
    return {"status": "approved", "message": "Article approved."}

print(f"✅ Define Get_output_preference and exit_loop functions")


# Helper function (check for approval)
def check_for_approval(events):
    """Check if events contain approval request."""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (part.function_call and
                    part.function_call.name == "adk_request_confirmation"):
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id,
                    }
    return None

print(f"✅ Helper function created")


# Define all agents

# Coordinator Agent
coordinator_agent = Agent(
    name="CoordinatorAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""Call get_output_preference tool. After user responds, check their message:
    - If 'comprehensive': output "comprehensive"
    - If 'simple': output "simple"
    - Default: "simple"
    Output ONLY the preference word.""",
    tools=[FunctionTool(func=get_output_preference)],
    output_key="user_preference",
)
print("✅ coordinator_agent created.")


# Biomedical researcher Agent: Search various online databases for information on clinical trials and current research for a particular disease or research area.
bio_researcher = Agent(
    name="bio_researcher",
    model=Gemini(
        model="gemini-2.5-flash", 
        retry_options=retry_config
    ), 
    instruction="You are a researcher. Use the mcp tool to find research and clinical trial information. Include known mutations associated with this disease. Only output a brief summary with appropriate references.",
    tools=[mcp_bio_server],
    output_key="bio_research",
)
print("✅ bio_researcher created.")


# Health Researcher Agent: Performs google search focusing on medical breakthroughs for a particular disease or research area.
health_researcher = Agent(
    name="HealthResearcher",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""Research recent medical breakthroughs for a particular disease or research area. Include 3 significant advances,
their practical applications, and estimated timelines. Keep the report concise (100 words). Include relevant references.""",
    tools=[google_search],
    output_key="health_research",  # The result will be stored with this key.
)

print("✅ health_researcher created.")


# Aggregator Agent
aggregator_agent = Agent(
    name="AggregatorAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""Combine these findings into an executive summary:
    **Research:** {bio_research}
    **News:** {health_research}
    Highlight key takeaways (200 words).""",
    output_key="executive_summary",
)
print("✅ aggregator_agent created.")


# Scientific article writer agent
initial_science_writer_agent = Agent(
    name="InitialScienceWriterAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""Based on: {executive_summary}, write a first draft article (100-150 words).
    Output only the article text.""",
    output_key="current_science_article",
)
print("✅ initial_science_writer_agent created.")


# Scientific and article critique agent
critic_agent = Agent(
    name="CriticAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""Review: {current_science_article}
    If well-written with references: respond "APPROVED"
    Otherwise: provide 2-3 suggestions.""",
    output_key="critique",
)
print("✅ critic_agent created.")


# Article refiner agent
refiner_agent = Agent(
    name="RefinerAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""Draft: {current_science_article}
    Critique: {critique}
    If critique is "APPROVED": call exit_loop
    Otherwise: rewrite incorporating feedback.""",
    output_key="current_science_article",
    tools=[FunctionTool(exit_loop)],
)
print("✅ refiner_agent created.")


# Final output agent
final_output_agent = Agent(
    name="FinalOutputAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""Based on: {user_preference}
    
    If COMPREHENSIVE:
    **EXECUTIVE SUMMARY**
    {executive_summary}

    **KEY DEVELOPMENTS**
    {health_research} (2-3 points only)
    
    If SIMPLE:
    {current_science_article}""",
    output_key="final_output",
)
print("✅ final_output_agent created.")


# Pipeline Construction

# Article refinement loop
article_refinement_loop = LoopAgent(
    name="ArticleRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2,
)

# Research pipeline
research_pipeline = SequentialAgent(
    name="ResearchPipeline",
    sub_agents=[
        bio_researcher,      # Run FIRST (before pause)
        health_researcher,   # Run SECOND (before pause)
    ],
)

# Root Agent to orchestrate agent flow
test_root_agent = SequentialAgent(
    name="TestPipeline",
    sub_agents=[
        coordinator_agent,              # THEN ask for preference (pause here)
        research_pipeline,              # Do all research FIRST
        aggregator_agent,               # Resume: aggregate results
        initial_science_writer_agent,   # Write article
        article_refinement_loop,        # Refine
        final_output_agent,             # Format output
    ],
)

print(f"✅ Pipeline constructed")


# App and Runner setup
session_service = InMemorySessionService()

# Renamed from test_app to _archived_test_app to prevent ADK auto-discovery
_archived_test_app = App(
    name="article_coordinator_test",
    root_agent=test_root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

test_runner = Runner(
    app=_archived_test_app,
    session_service=session_service,
)

print(f"✅ App and Runner configured")


async def run_test_workflow(query: str):
    """Run workflow with user interaction."""
    
    print(f"\n{'='*60}")
    print(f"User > {query}\n")
    
    session_id = f"test_{uuid.uuid4().hex[:8]}"
    
    await session_service.create_session(
        app_name="article_coordinator_test",
        user_id="test_user",
        session_id=session_id
    )
    
    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    events = []
    
    print("🔄 Starting...")
    async for event in test_runner.run_async(
        user_id="test_user",
        session_id=session_id,
        new_message=query_content
    ):
        events.append(event)
    
    approval_info = check_for_approval(events)
    
    if approval_info:
        print(f"⏸️  Pausing for preference...\n")
        
        user_choice = input("Your choice (comprehensive/simple): ").strip()
        print(f"\n✅ You selected: {user_choice}\n")
        
        confirmation_response = types.FunctionResponse(
            id=approval_info["approval_id"],
            name="adk_request_confirmation",
            response={"confirmed": True},
        )
        
        combined_content = types.Content(
            role="user",
            parts=[
                types.Part(function_response=confirmation_response),
                types.Part(text=user_choice)
            ]
        )
        
        print("🔄 Resuming...")
        async for event in test_runner.run_async(
            user_id="test_user",
            session_id=session_id,
            new_message=combined_content,
            invocation_id=approval_info["invocation_id"],
        ):
            pass  # Just process
        
        print(f"✅ Completed\n")
    
    # Display output
    session = await session_service.get_session(
    app_name="article_coordinator_test",  # Use the actual app name
    user_id="test_user",                  # Use the actual user ID
    session_id=session_id
    )
    if session and 'final_output' in session.state:
        print("\n" + "="*60)
        print("FINAL OUTPUT:")
        print("="*60)
        print(session.state['final_output'])
    elif session:
        print(f"\nState keys: {list(session.state.keys())}")
    else:
        print("\nSession not found")

if __name__ == "__main__":
    import asyncio
    user_query = "Summarize recent advances in the treatment of gardener syndrome"
    asyncio.run(run_test_workflow(user_query))