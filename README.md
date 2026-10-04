---
title: Company Preparation Crew
emoji: 📚
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 6.29.1
python_version: "3.12"
app_file: app.py
pinned: false
license: mit
short_description: AI-powered company interview preparation
---

<div align="center">

# 🎯 Company Preparation Crew

**Autonomous Multi-Agent AI System for Deep Company Research & Verified Interview Preparation**

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow?style=for-the-badge)](https://huggingface.co/spaces/Badal-gaurkhede/Company-preparation-crew)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-orange?style=for-the-badge&logo=crewai)](https://crewai.com)
[![Gradio](https://img.shields.io/badge/Gradio-Web%20UI-ff7c00?style=for-the-badge&logo=gradio)](https://gradio.app)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 📌 Overview

**Company Preparation Crew** is an end-to-end AI agent pipeline designed to help job seekers, consultants, and analysts prepare for company interviews with precision. 

Powered by **CrewAI**, **OpenAI**, **Google Gemini**, and **Serper Dev**, this system orchestrates specialized autonomous agents that perform live web research, synthesize a targeted 1-page interview brief, and ruthlessly fact-check all claims against original source URLs before delivering the final report.

---

## 🚀 Key Features

- 🔍 **Live Real-Time Web Research**: Deep research across recent news (last 6 months), tech stacks, funding, culture, and interview experiences.
- ✍️ **Targeted Role-Specific Prep Brief**: Tailors overview, key products, and intelligent interview questions specifically for the target role.
- 🛡️ **Autonomous Fact-Checking & Source Citing**: Sits an editor agent to cross-verify every claim against source URLs and eliminate hallucinated details.
- 🌐 **Modern Gradio Web UI**: Beautiful, interactive interface with real-time status feedback and smooth brief streaming.
- ⚡ **Multi-LLM Architecture**: Leverages OpenAI GPT-4o-mini for research & writing and Gemini 3.6 Flash for editorial fact-checking.
- 💻 **Dual Execution**: Run easily via modern Gradio Web UI or through standard CrewAI CLI.

---

## 🏗️ Multi-Agent Architecture

```text
                                 ┌─────────────────────────┐
                                 │   User Inputs Target    │
                                 │  Company & Target Role  │
                                 └────────────┬────────────┘
                                              │
                                              ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                                   CrewAI Pipeline                                      │
 │                                                                                        │
 │  ┌────────────────────────┐    ┌────────────────────────┐    ┌──────────────────────┐  │
 │  │ 🔍 Research Analyst    │───▶│ ✍️ Prep Writer          │───▶│ 🛡️ Fact-Checker      │  │
 │  │ • Live Web Search      │    │ • 1-Page Prep Brief    │    │ • Verify All Sources │  │
 │  │ • Sourced Facts & News │    │ • Smart Questions      │    │ • Filter Hallucinate │  │
 │  │ (GPT-4o-mini + Serper) │    │ (GPT-4o-mini)          │    │ (Gemini Flash)       │  │
 │  └────────────────────────┘    └────────────────────────┘    └──────────┬───────────┘  │
 │                                                                         │              │
 └─────────────────────────────────────────────────────────────────────────┼──────────────┘
                                                                           │
                                                                           ▼
                                                             ┌─────────────────────────┐
                                                             │   Final Verified Brief  │
                                                             │  (Gradio UI / Markdown) │
                                                             └─────────────────────────┘
```

### Agent Roles

| Agent | Model | Primary Responsibility | Tools |
| :--- | :--- | :--- | :--- |
| **🔍 Company Research Analyst** | `openai/gpt-4o-mini` | Uncovers accurate, recent news, funding, tech stack, and interview notes. | `SerperDevTool` (Google Search) |
| **✍️ Interview Prep Writer** | `openai/gpt-4o-mini` | Transforms raw research into a structured, highly actionable one-page brief. | — |
| **🛡️ Fact-Checking Editor** | `gemini/gemini-3.6-flash` | Validates every statement against original source URLs, stripping out unsupported claims. | — |

---

## 📂 Project Structure

```
company_pre_crew/
├── app.py                         # Hugging Face Spaces / Gradio entrypoint
├── pyproject.toml                 # Project metadata and dependencies (uv / pip)
├── requirements.txt               # Standalone requirements
├── .env.example                   # Environment variable template
├── output/
│   └── result.md                  # Latest generated interview brief
└── src/
    └── company_pre_crew/
        ├── __init__.py
        ├── crew.py                # CrewBase configuration and agent assembly
        ├── gradio_app.py          # Gradio UI implementation & streaming engine
        ├── main.py                # CLI runner & test scripts
        └── config/
            ├── agents.yaml        # Agent roles, goals, and LLM definitions
            └── tasks.yaml         # Task descriptions, expected outputs & dependencies
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.10 to 3.12
- [uv](https://docs.astral.sh/uv/) (recommended) or `pip`
- API Keys for:
  - [OpenAI](https://platform.openai.com/) (`OPENAI_API_KEY`)
  - [Serper Dev](https://serper.dev/) (`SERPER_API_KEY`)
  - [Google AI Studio](https://aistudio.google.com/) (`GEMINI_API_KEY`)

### 2. Clone the Repository
```bash
git clone https://github.com/Badal123-tech/CompanyPreCrew.git
cd CompanyPreCrew
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Install Dependencies

Using **uv** (recommended):
```bash
uv sync
```

Or using **pip**:
```bash
pip install -r requirements.txt
```

---

## 🖥️ Running the Application

### Option 1: Launch the Gradio Web Interface
```bash
# Using uv
uv run python app.py

# Or with python directly
python app.py
```
Open your browser at `http://localhost:7860`.

### Option 2: Run via CLI
```bash
# Using CrewAI CLI runner
crewai run

# Or directly through main.py
uv run python -m company_pre_crew.main
```

---

## 🌐 Live Demo on Hugging Face Spaces

Try the live interactive version directly in your browser:
👉 [**Hugging Face Space: Company Preparation Crew**](https://huggingface.co/spaces/Badal-gaurkhede/Company-preparation-crew)

---

## 🛠️ Customization

- **Modify Agent Personas**: Update `src/company_pre_crew/config/agents.yaml` to change LLM models, prompts, or backstories.
- **Adjust Report Structure**: Edit `src/company_pre_crew/config/tasks.yaml` to include custom sections (e.g. salary insights, compensation analysis, specific coding challenges).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).