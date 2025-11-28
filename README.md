# 🏥 Medluma - AI-Powered Disease Information Portal

[![Medluma](medluna_capstone_image.png)](medluma_example.webm)

> 🎯 **Bridge the gap between complex medical data and accessible health information**

**Medluma** is a comprehensive, AI-powered disease information portal that leverages multi-agent orchestration to automate the retrieval, synthesis, and presentation of medical knowledge. Get tailored insights ranging from detailed biomedical research to simplified health news—all in one place.

## 📹 Demo

Watch the demo: [medluma_example.webm](medluma_example.webm)

## ✨ Features

- 🔬 **Biomedical Research Integration** - Direct access to clinical trials, genetic mutations, and research papers via BioMCP
- 📰 **Real-time Health News** - Latest medical breakthroughs and developments from trusted sources
- 🤖 **Multi-Agent Architecture** - Specialized AI agents working together for comprehensive analysis
- 📝 **Quality Assurance Loop** - Built-in critic-refiner system ensures accuracy and clarity
- 🎚️ **Adaptive Output** - Choose between comprehensive reports or simplified summaries
- 🔄 **Resumable Sessions** - Continue your research across multiple sessions

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8+
# Google ADK installed
pip install google-adk biomcp-python
```

### Installation

```bash
# Clone the repository
git clone https://github.com/capgalea/Medluma_AI_Agent.git
cd Medluma_AI_Agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with your API keys
```

### Running the App

```bash
# Activate your virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac

# Start the web interface
adk web
```

Navigate to `http://127.0.0.1:8000` in your browser.

![Medluma Workflow](disease_condition_research_flow.svg)

## 🎯 Problem Statement

Navigating the vast ocean of medical information is a daunting task for both healthcare professionals and the general public:

- ⏰ **Time-consuming** - Searching disparate sources (clinical trials, genomic databases, news outlets)
- 📊 **Information overload** - Too much data, difficult to synthesize
- 🔬 **Complexity barrier** - Medical texts alienate laypeople
- 🎓 **Depth vs. accessibility** - Professionals need precision, public needs clarity

**There is a critical need for a system that intelligently aggregates verified data and adapts output to the reader's expertise level.**

## 💡 Solution

Medluma deploys a **team of specialized AI agents** acting as an on-demand medical research team:

✅ **Autonomous Data Gathering** - Query biological databases (BioMCP) and real-time web sources  
✅ **Quality Assurance** - Critic-Refiner loop ensures accuracy before output  
✅ **Dynamic Formatting** - Toggle between "Comprehensive" (professionals) and "Simple" (general public)  
✅ **Verified Information** - Minimize hallucinations with retrieved, factual data  

> 🌟 **Democratizing access to high-level medical insights**

## 🏗️ Architecture

At the heart of Medluma is **sophisticated multi-agent orchestration** powered by Google's Gemini models. Rather than a single LLM trying to do everything, the workload is distributed among domain experts.

### 🤖 The Agent Team

#### 🔬 **Biological Data Specialist** (`bio_researcher`)
Connects to `mcp_bio_server` for deep dives into:
- Research papers and publications
- Active clinical trials
- Genetic mutations associated with diseases

#### 📰 **News Analyst** (`health_researcher`)
Uses `Google Search` to scan for:
- Recent medical breakthroughs
- News highlights and press releases
- Practical applications of new therapies

#### 🔄 **Synthesis Engine** (`aggregator_agent`)
Bridges the gap by creating a unified **Executive Summary** from:
- Structured biomedical data
- Latest news highlights
- Key takeaways for users

#### ✍️ **The Writer's Room**

```
Initial Writer → Critic → Approved? 
                   ↑         ↓ No
                   ←── Refiner
                         ↓ Yes
                   Final Output
```

- **`initial_science_writer_agent`** - Drafts initial article from executive summary
- **`critic_agent`** - Quality control gatekeeper reviewing clarity, citations, and flow
- **`refiner_agent`** - Enters refinement loop, rewriting based on feedback until approved

#### 🎛️ **Orchestration** (`coordinator_agent`)
Manages user interaction flow and routing logic:
- **Comprehensive** mode for professionals
- **Simple** mode for general awareness

## 🛠️ Essential Tools and Utilities

### 🧬 **BioMCP Server** (`mcp_bio_server`)
Model Context Protocol (MCP) tool for interfacing with specialized biological datasets:
- ✅ Factual grounding for mutations and clinical studies
- ✅ Structured medical data beyond standard web searches
- ✅ Access to verified scientific databases

### 🔍 **Google Search** (`google_search`)
Real-time web scanning by `health_researcher`:
- 📅 Most current events and press releases
- 📢 Media coverage of diseases and treatments
- 🆕 Breaking medical news

### 🔁 **Validation Loop** (`exit_loop`)
Quality assurance mechanism:
- ✓ Breaks drafting cycle when `critic_agent` approves
- ✓ Prevents infinite loops
- ✓ Guarantees editorial quality standards

## 🎓 Technical Highlights

- **🏗️ Sequential Agent Pipeline** - Coordinated workflow through multiple specialized agents
- **🔄 Loop Agent** - Iterative refinement with quality gates
- **💾 Resumable Sessions** - Built-in session management for long-running research
- **⚡ Retry Configuration** - Robust error handling with exponential backoff
- **🔧 Tool Integration** - MCP and Google Search for comprehensive data access

## 📊 Use Cases

### 👩‍⚕️ Healthcare Professionals
- Quick literature reviews on specific conditions
- Latest clinical trial information
- Genetic mutation summaries

### 👨‍🔬 Researchers
- Automated initial research gathering
- Comprehensive disease profiles
- Reference-rich reports

### 👥 General Public
- Understanding complex medical conditions
- Simplified health news summaries
- Accessible disease information

## 🔧 Configuration

The `adk.config.yaml` file specifies the app configuration:

```yaml
apps:
  - path: ./medluma_app.py
    app_name: app
```

## 📂 Project Structure

```
Medluma_AI_Agent/
├── medluma_app.py          # Main application file
├── adk.config.yaml         # ADK configuration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── medluma/               # Package directory
│   └── __init__.py
├── Medluna_mermaid.png    # Workflow diagram
├── medluma_example.webm   # Demo video
└── README.md              # This file
```

## 🚀 Future Enhancements

![Future Vision](future_app_medluna.png)

- 🌍 Multi-language support
- 📱 Mobile application
- 🔔 Personalized health alerts
- 📈 Trending disease tracking
- 🤝 Collaborative research features

## 💡 Value Proposition

Medluma demonstrates the potential of agentic workflows in the healthcare domain:

- **Reduced Cognitive Load** - Automates initial literature review for researchers
- **Translation Layer** - Converts complex jargon into understandable summaries for patients
- **Minimized Hallucinations** - Leverages specialized tools like BioMCP for verified, factual data
- **Quality Through Iteration** - Critic-Refiner loop mimics real-world editorial processes
- **Depth and Reliability** - Multi-agent specialization achieves what single-shot prompts cannot

## 📝 License

This project is licensed under the terms included in the [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- **Google ADK** - Agent Development Kit powering the multi-agent architecture
- **BioMCP** - Biological Model Context Protocol for medical data access
- **Gemini 2.0 Flash** - Advanced AI models driving the agents

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

<div align="center">

**Built with ❤️ using Google ADK and Gemini 2.0**

![Medluma Architecture](medluna_image.png)

</div>
