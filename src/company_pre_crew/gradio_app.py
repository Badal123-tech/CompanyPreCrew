import queue
import threading
import time
import gradio as gr
try:
    import spaces  # For Hugging Face ZeroGPU environments
except ImportError:
    class _MockSpaces:
        def GPU(self, fn):
            return fn

    spaces = _MockSpaces()

from company_pre_crew.crew import CompanyPrepCrew

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

.header-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border-radius: 16px;
    padding: 32px 28px;
    margin-bottom: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.4);
    color: white;
}

.header-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(129, 140, 248, 0.4);
    color: #a5b4fc;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.header-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    background: linear-gradient(120deg, #ffffff 30%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.header-subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    line-height: 1.5;
    max-width: 680px;
}

.pipeline-container {
    display: flex;
    gap: 12px;
    margin-top: 20px;
    flex-wrap: wrap;
}

.agent-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 8px 14px;
    border-radius: 10px;
    font-size: 0.82rem;
    color: #e2e8f0;
}

.agent-pill strong {
    color: #38bdf8;
}

.generate-btn {
    background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 12px 24px !important;
    border-radius: 10px !important;
    border: none !important;
    box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.35) !important;
    transition: all 0.2s ease !important;
}

.generate-btn:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.45) !important;
}

.output-box {
    background: #ffffff;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    padding: 24px;
    min-height: 480px;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
}

.dark .output-box {
    background: #1e293b;
    border-color: #334155;
}

.status-badge {
    font-size: 0.88rem;
    color: #475569;
    margin-top: 6px;
}
"""

theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="slate",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Plus Jakarta Sans"), "sans-serif"],
).set(
    button_primary_background_fill="linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%)",
    button_primary_background_fill_hover="linear-gradient(135deg, #4338ca 0%, #2563eb 100%)",
    block_border_width="1px",
    block_radius="12px",
    input_background_fill="*neutral_50",
)


def stream_final_brief_only(company_name: str, target_role: str):
    """
    Runs the multi-agent pipeline and streams ONLY the final verified brief
    directly into the UI smoothly word-by-word.
    """
    if not company_name.strip() or not target_role.strip():
        gr.Warning("Please enter both Company Name and Target Role.")
        yield (
            "### ⚠️ Missing Required Inputs\n\nPlease fill in both **Company Name** and **Target Role** to start.",
            "",
            "Inputs missing",
        )
        return

    inputs = {
        "company_name": company_name.strip(),
        "target_role": target_role.strip(),
    }

    event_queue = queue.Queue()
    start_time = time.time()

    def run_crew():
        try:
            crew_instance = CompanyPrepCrew().crew()
            result = crew_instance.kickoff(inputs=inputs)
            event_queue.put(("done", str(result.raw)))
        except Exception as e:
            event_queue.put(("error", str(e)))

    # Start background execution
    thread = threading.Thread(target=run_crew, daemon=True)
    thread.start()

    # While running, show clean waiting state in output
    loading_animation = ["⏳", "🔍", "✍️", "🛡️", "✨"]
    step_idx = 0

    while thread.is_alive():
        try:
            event_type, data = event_queue.get(timeout=0.6)
            if event_type in ("done", "error"):
                event_queue.put((event_type, data))
                break
        except queue.Empty:
            icon = loading_animation[step_idx % len(loading_animation)]
            step_idx += 1
            elapsed = round(time.time() - start_time, 1)

            waiting_display = (
                f"### {icon} Researching & Preparing Brief for **{inputs['company_name']}**...\n\n"
                f"Autonomous agents are currently executing:\n"
                f"- **Step 1/3:** Deep live web research on news, tech stack, and financials\n"
                f"- **Step 2/3:** Synthesizing targeted brief for **{inputs['target_role']}**\n"
                f"- **Step 3/3:** Fact-checking and verifying claims against sources\n\n"
                f"*Elapsed time: {elapsed}s — Output will stream below immediately once verified...*"
            )

            yield (
                waiting_display,
                "",
                f"⏳ Crew running... ({elapsed}s)",
            )

    # Process the completion or error
    try:
        event_type, data = event_queue.get(timeout=2.0)
    except queue.Empty:
        event_type, data = "error", "Execution timed out or ended unexpectedly."

    if event_type == "error":
        err_display = (
            f"### ❌ Generation Failed\n\n"
            f"```text\n{data}\n```\n\n"
            f"**Troubleshooting:**\n"
            f"- Verify API keys in `.env` (`OPENAI_API_KEY`, `SERPER_API_KEY`, `GEMINI_API_KEY`)\n"
            f"- Ensure valid model names in `agents.yaml`"
        )
        yield err_display, "", "❌ Execution failed"
        return

    # Stream ONLY the final verified brief word-by-word into the UI
    final_text = data
    total_time = round(time.time() - start_time, 1)

    words = final_text.split(" ")
    current_text = ""
    chunk_size = 2  # Stream 2 words per tick for smooth reading

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i : i + chunk_size])
        if current_text:
            current_text += " " + chunk
        else:
            current_text = chunk

        yield (
            current_text + " ▍",
            current_text,
            f"✨ Streaming final brief... ({total_time}s)",
        )
        time.sleep(0.015)  # 15ms per token tick

    # Final completed output without cursor
    yield (
        final_text,
        final_text,
        f"✅ Brief Ready ({total_time}s) • Fact-checked & Verified",
    )


with gr.Blocks(title="CompanyPrep AI") as demo:

    # Hero Banner
    gr.HTML("""
    <div class="header-box">
        <div class="header-badge">
            <span>✨</span> Multi-Agent Intelligence System
        </div>
        <div class="header-title">Company Interview Prep Brief</div>
        <div class="header-subtitle">
            Autonomous CrewAI agents research live news, tech stacks, and culture — synthesized and fact-checked in real time.
        </div>
        <div class="pipeline-container">
            <div class="agent-pill">🔍 <span>1. Researcher</span> <strong>GPT-4o Mini + Serper</strong></div>
            <div class="agent-pill">✍️ <span>2. Writer</span> <strong>GPT-4o Mini</strong></div>
            <div class="agent-pill">🛡️ <span>3. Editor</span> <strong>Gemini 2.0 Flash + Serper</strong></div>
        </div>
    </div>
    """)

    with gr.Row():
        # Left Configuration Column
        with gr.Column(scale=4):
            with gr.Group():
                gr.Markdown("### 🎯 Target Parameters")
                company_input = gr.Textbox(
                    label="Target Company",
                    placeholder="e.g. OpenAI, Stripe, Datadog, Apple",
                    lines=1,
                    max_lines=1,
                )
                role_input = gr.Textbox(
                    label="Target Role / Level",
                    placeholder="e.g. Senior Machine Learning Engineer, Staff PM",
                    lines=1,
                    max_lines=1,
                )

                gr.Markdown("#### ⚡ Quick Examples")
                gr.Examples(
                    examples=[
                        ["Stripe", "Senior Infrastructure Engineer"],
                        ["OpenAI", "Member of Technical Staff"],
                        ["Google", "Staff Product Manager"],
                        ["Datadog", "Lead Solutions Architect"],
                    ],
                    inputs=[company_input, role_input],
                    label="",
                )

                with gr.Row():
                    clear_btn = gr.ClearButton(
                        components=[company_input, role_input],
                        value="Clear",
                        variant="secondary",
                    )
                    submit_btn = gr.Button(
                        "Generate Brief 🚀",
                        variant="primary",
                        elem_classes=["generate-btn"],
                    )

                status_label = gr.Markdown(
                    "Ready for inputs.", elem_classes=["status-badge"]
                )

        # Right Output Brief Column
        with gr.Column(scale=7):
            with gr.Tabs():
                with gr.TabItem("📄 Formatted Brief"):
                    output_markdown = gr.Markdown(
                        value="*Your comprehensive interview brief will stream here in real time...*",
                        elem_classes=["output-box"],
                    )

                with gr.TabItem("📋 Raw Markdown & Export"):
                    output_raw = gr.Code(
                        label="Markdown Source",
                        language="markdown",
                        lines=18,
                    )

    # Wire streaming generator
    submit_btn.click(
        fn=stream_final_brief_only,
        inputs=[company_input, role_input],
        outputs=[output_markdown, output_raw, status_label],
    )


def run_gui():
    demo.launch(
        theme=theme,
        css=CUSTOM_CSS,
        share=False,
        inbrowser=True,
        ssr_mode=False,
    )


if __name__ == "__main__":
    run_gui()