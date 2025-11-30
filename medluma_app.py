"""
Medluma - AI-powered Disease Information Portal
Web-enabled version for ADK
"""

import os
import shutil
import sys
from google.genai import types
from mcp import StdioServerParameters
from google.adk.agents import Agent, SequentialAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.google_search_tool import google_search


# Setup retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


# Locate biomcp
biomcp_path = shutil.which("biomcp")
if not biomcp_path:
    # Build a list of possible paths to search for the executable
    possible_paths = []
    if sys.platform == "win32":
        # On Windows, pip installs executables in the 'Scripts' directory
        possible_paths.extend([
            os.path.join(sys.prefix, "Scripts", "biomcp.exe"),
            os.path.join(os.path.dirname(sys.executable), "biomcp.exe"),
            os.path.expanduser("~\\.local\\bin\\biomcp.exe")
        ])
    else:
        # On Linux and macOS, it's usually in the 'bin' directory
        possible_paths.extend([
            os.path.join(sys.prefix, "bin", "biomcp"),
            os.path.join(os.path.dirname(sys.executable), "biomcp"),
            os.path.expanduser("~/.local/bin/biomcp")
        ])

    for path in possible_paths:
        if os.path.exists(path):
            biomcp_path = path
            break

if not biomcp_path:
    raise RuntimeError("biomcp not found - run: pip install biomcp-python")


# Configure BioMCP MCP tool
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


# Tool functions
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
    """Exit the refinement loop."""
    return {"status": "approved", "message": "Article approved."}


# Define Agents

# Coordinator Agent
coordinator_agent = Agent(
    name="CoordinatorAgent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    description="Determine user output preference for article detail level.",
    instruction="""Call get_output_preference tool. After user responds, check their message:
    - If 'comprehensive': output "comprehensive"
    - If 'simple': output "simple"
    - Default: "simple"
    Output ONLY the preference word.""",
    tools=[FunctionTool(func=get_output_preference)],
    output_key="user_preference",
)

# Biomedical researcher Agent
bio_researcher = Agent(
    name="BioResearcher",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    description="Research biomedical information using the mcp tool.",
    instruction="""You are a biomedical researcher. Use the mcp tool to find:
    1. current research findings,
     2. clinical trial information including the phase the trial is at and whether it is accepting patients,  
     3. known mutations associated with this disease,
     4. recent advancements in treatment options,
     5. relevant statistics such as prevalence, mortality rates, and demographic data,
     6. any other pertinent biomedical information,
     7. currently available therapies and their effectiveness including FDA-approved drugs (and drugs 
     awaiting FDA approval) and emerging treatments.
     8. genetic markers linked to the disease.
    After gathering the information, summarize the key findings in a concise report (200 words).
    Always include references to the sources of your information.
    Include sections with headings for clarity. Output ONLY the report.""",
    tools=[mcp_bio_server],
    output_key="bio_research",
)

# Health Researcher Agent
health_researcher = Agent(
    name="HealthResearcher",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    description="Research recent medical breakthroughs for a particular disease or research area.",
    instruction="""Research recent medical breakthroughs for a particular disease or research area. 
    Include 3 significant advances, their practical applications, and estimated timelines. 
    Keep the report concise (100 words). Include relevant references.""",
    tools=[google_search],
    output_key="health_research",
)

# Aggregator Agent
aggregator_agent = Agent(
    name="AggregatorAgent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    description="Combine biomedical and health research findings into an executive summary.",
    instruction="""Combine these findings into an executive summary:
    **Research:** {bio_research}
    **News:** {health_research}
    Highlight key takeaways (200 words).""",
    output_key="executive_summary",
)

# Scientific article writer agent
initial_science_writer_agent = Agent(
    name="InitialScienceWriterAgent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    description="Write a first draft scientific article based on the executive summary.",
    instruction="""Based on: {executive_summary}, write a first draft article (100-150 words).
    Output only the article text.""",
    output_key="current_science_article",
)

# Scientific and article critique agent
critic_agent = Agent(
    name="CriticAgent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    description="Review the scientific article draft and provide feedback or approval.",
    instruction="""Review: {current_science_article}
    If well-written with references: respond "APPROVED"
    Otherwise: provide 2-3 suggestions.""",
    output_key="critique",
)

# Article refiner agent
refiner_agent = Agent(
    name="RefinerAgent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    description="Refine the scientific article draft based on critique feedback.",
    instruction="""Draft: {current_science_article}
    Critique: {critique}
    If critique is "APPROVED": call exit_loop
    Otherwise: rewrite incorporating feedback.""",
    output_key="current_science_article",
    tools=[FunctionTool(exit_loop)],
)

# Final output agent
final_output_agent = Agent(
    name="FinalOutputAgent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    description="Generate the final output based on user preference.",
    instruction="""Based on: {user_preference}
    
    If COMPREHENSIVE:
    Use the {bio_research} output and create a final output with the following sections:

    **BACKGROUND**
    Provide context on the disease including definition, causes, risk factors and symptoms.

    **SUMMARY**
   Create a concise executive summary outlining key advances, their practical applications 
   (including treatment options), and estimated timelines.
    
    **KEY DEVELOPMENTS**
    {health_research} (2-3 points only)

    **REFERENCES**
    List all references used in research.
    
    If SIMPLE:
    {current_science_article}""",
    output_key="final_output",
)


# Build Pipeline

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
        bio_researcher,
        health_researcher,
    ],
)

# Root Agent
root_agent = SequentialAgent(
    name="MedlumaRootAgent",
    sub_agents=[
        coordinator_agent,
        research_pipeline,
        aggregator_agent,
        initial_science_writer_agent,
        article_refinement_loop,
        final_output_agent,
    ],
)


# Create the App
app = App(
    name="medluma",
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)


# Export the app and root_agent so ADK can find them
__all__ = ["app", "root_agent"]

if __name__ == "__main__":
    print("✅ Medluma app configured for web interface")
    print(f"App name: {app.name}")
