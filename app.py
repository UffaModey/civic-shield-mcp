import gradio as gr
from pdf_utils import extract_text_from_pdf

# Import the MCP instance from server.py
from server import mcp


# -------------------------------
# Gradio → MCP Orchestration
# -------------------------------
async def run_full_analysis(text, pdf_file, region, activism_type):
    if pdf_file is not None:
        document_text = extract_text_from_pdf(pdf_file)
    elif text and text.strip():
        document_text = text
    else:
        return (
            "No document provided.",
            "No document provided.",
            "No document provided.",
            "No document provided.",
        )

    context = {"region": region, "activism_type": activism_type}

    # Call MCP tools
    risks = await mcp.call_tool(
        "analyze_risks", {"text": document_text, "context": context}
    )

    clauses = await mcp.call_tool("extract_clauses", {"text": document_text})

    summary = await mcp.call_tool(
        "simplify_text", {"text": document_text, "audience": "grassroots activists"}
    )

    actions = await mcp.call_tool(
        "recommend_actions", {"text": document_text, "context": context}
    )

    return (
        risks[1]["result"],
        clauses[1]["result"],
        summary[1]["result"],
        actions[1]["result"],
    )


# -------------------------------
# Gradio UI
# -------------------------------
with gr.Blocks() as demo:
    gr.Markdown("## 🛡️ CivicShield – Digital Rights Risk Analyzer")
    gr.Markdown("Upload a PDF or paste text. Files are **not stored**.")

    text_input = gr.Textbox(lines=10, label="Paste document text")

    pdf_input = gr.File(file_types=[".pdf"], label="Upload PDF document")

    region = gr.Dropdown(["Nigeria", "Kenya", "UK", "Global South"], label="Region")

    activism = gr.Dropdown(
        ["Feminist organising", "Journalism", "Youth activism"],
        label="Type of Activism",
    )

    analyze_btn = gr.Button("Analyze Document")

    risks_out = gr.Textbox(label="Risk Analysis", lines=5)
    clauses_out = gr.Textbox(label="Problematic Clauses", lines=5)
    summary_out = gr.Textbox(label="Plain Language Summary", lines=5)
    actions_out = gr.Textbox(label="Recommended Actions", lines=5)

    analyze_btn.click(
        run_full_analysis,
        inputs=[text_input, pdf_input, region, activism],
        outputs=[risks_out, clauses_out, summary_out, actions_out],
    )


if __name__ == "__main__":
    demo.launch(mcp_server=True)
