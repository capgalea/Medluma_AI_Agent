# 🏥 Medluma - AI-Powered Disease Information Portal

<div align="center">

<img src=images/medluna_capstone_image.png  alt="Medluma Banner" width="500" height="500" style="display: block; margin: 0 auto;">

### 🎯 Bridge the gap between complex medical data and accessible health information

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4?logo=google)](https://developers.google.com/)

[Demo Video](images/medluma_example.webm) • [Documentation](#-architecture) • [Quick Start](#-quick-start) • [Contact](#-contact)

</div>

---

## 📖 Overview

**Medluma** is a comprehensive, AI-powered disease information portal that leverages multi-agent orchestration to automate the retrieval, synthesis, and presentation of medical knowledge. Built with Google's Agent Development Kit (ADK) and powered by Gemini 2.0, it provides tailored insights ranging from detailed biomedical research to simplified health news—all in one place.

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

<div align="center">

<img src="images/disease_condition_research_flow.svg"   alt="Medluma Workflow - Multi-Agent Architecture" width="400" style="display: block; margin: 0 auto;">

*Complete workflow showing the multi-agent orchestration process*

</div>

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

## 📂 Project Structure

```
Medluma_AI_Agent/
├── medluma_app.py                      # Main application entry point
├── medluma.py                          # Legacy/alternative implementation
├── adk.config.yaml                     # ADK web server configuration
├── requirements.txt                    # Python dependencies
├── LICENSE                             # MIT License
├── README.md                           # This file
├── .env                                # Environment variables (create this)
├── .gitignore                          # Git ignore rules
│
├── medluma/                            # Application package
│   └── __init__.py                     # Package initializer
│
├── images/                             # Assets and media
│   ├── medluma_example.webm            # Demo video
│   ├── disease_condition_research_flow.svg  # Workflow diagram
│   ├── disease_info_generation.png     # Process diagram
│   ├── medluna_capstone_image.png      # Banner image
│   ├── medluna_image.png               # Architecture image
│   └── future_app_medluna.png          # Future vision mockup
## 🚀 Future Enhancements

<div align="center">

![Future Vision](images/future_app_medluna.png)

*Vision for expanded capabilities*

</div>

- 🌍 **Multi-language Support** - Reach global audiences with translations
- 📱 **Mobile Application** - iOS and Android apps for on-the-go access
- 🔔 **Personalized Health Alerts** - Customized notifications for followed conditions
- 📈 **Trending Disease Tracking** - Real-time monitoring of emerging health topics
- 🤝 **Collaborative Research** - Share and annotate reports with teams
- 🔗 **API Access** - Programmatic integration for healthcare systems
- 📚 **Knowledge Base** - Build institutional memory of past queriesw diagram
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

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Google ADK](https://developers.google.com/)** - Agent Development Kit powering the multi-agent architecture
- **[BioMCP](https://github.com/ckreiling/biomcp)** - Biological Model Context Protocol for medical data access  
- **[Gemini 2.0 Flash](https://deepmind.google/technologies/gemini/)** - Advanced AI models driving the intelligent agents
- **Open Source Community** - For the amazing tools and libraries that make this possible

## 📧 Contact

**Charles Galea**  
📧 Email: [galea.charlesa@gmail.com](mailto:galea.charlesa@gmail.com)  
🐙 GitHub: [@capgalea](https://github.com/capgalea)

For bug reports and feature requests, please [open an issue](https://github.com/capgalea/Medluma_AI_Agent/issues).

## 🌟 Support

If you find Medluma useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs and suggesting features
- 🤝 Contributing to the codebase
- 📢 Sharing with others who might benefit

---

<div align="center">

![Medluma Architecture](images/medluna_image.png)

*Empowering healthcare professionals and patients with AI-driven medical insights*

</div>
