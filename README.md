---
title: Company Preparation Crew
emoji: 📚
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 6.29.1
python_version: "3.12"
app_file: src/company_pre_crew/gradio_app.py
pinned: false
license: mit
short_description: AI-powered company interview preparation
---
# CompanyPreCrew

An AI-powered company interview preparation system built with **CrewAI** and **Gradio**.

The application uses multiple AI agents to research a company, generate a targeted interview preparation brief, and fact-check the information before presenting the final result.

## Features

- 🔍 Company research
- ✍️ AI-generated interview preparation
- 🛡️ Fact-checking and verification
- 🤖 Multi-agent CrewAI architecture
- 🌐 Gradio web interface
- 🔎 Live web research using search tools
- 📄 Formatted and raw Markdown output

## Architecture

```text
User
  ↓
Gradio Interface
  ↓
CrewAI
  ├── Researcher Agent
  ├── Writer Agent
  └── Editor / Fact-checker Agent
          ↓
      Final Brief