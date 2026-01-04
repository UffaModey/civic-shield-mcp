from mcp.server.fastmcp import FastMCP
from api_tool import chat_completions

# -------------------------------
# MCP Server Setup
# -------------------------------
mcp = FastMCP("CivicShield MCP")

model = "gpt-4o"


@mcp.tool()
async def analyze_risks(text: str, context: dict) -> str:
    """
    Analyze a document to identify digital rights risks for activists in a given
    region and activism context.
    """
    prompt = f"""
You are a digital rights risk analyst supporting activists.

Analyze the document below in the context of:
- Region: {context['region']}
- Type of activism: {context['activism_type']}

Focus on risks related to:
- Surveillance or monitoring
- Data collection, storage, or sharing
- Restrictions on speech, organising, or association
- Unequal enforcement or vague legal powers

Write ONE short paragraph that explains:
1. The main types of risk
2. How severe they are (low / medium / high)
3. An overall risk level

Write clearly and calmly.
Do NOT use legal jargon.
Do NOT give legal advice.

Text:
{text}
"""
    return chat_completions(model, prompt)


@mcp.tool()
async def extract_clauses(text: str) -> str:
    """
    Identify and explain clauses in a document that could pose risks to activists.
    """
    prompt = f"""
You are reviewing a policy or legal document for activist safety.

Identify clauses or sections that could realistically pose risks to activists, such as:
- Broad or vague powers
- Consent buried in complex language
- One-sided obligations
- Surveillance, data sharing, or enforcement provisions

Describe the clauses in plain language and explain why they matter.
Write one clear paragraph.

Text:
{text}
"""
    return chat_completions(model, prompt)


@mcp.tool()
async def simplify_text(text: str, audience: str) -> str:
    """
    Rewrite complex legal or policy text in plain language for a specific audience.
    """
    prompt = f"""
Rewrite the document below for {audience}.

Explain:
- What the document is about
- What it expects from people
- Why it matters to activists

Use plain language.
Avoid legal or corporate terms.
Write 4–6 short sentences.

Text:
{text}
"""
    return chat_completions(model, prompt)


@mcp.tool()
async def recommend_actions(text: str, context: dict) -> str:
    """
    Suggest practical safety and advocacy actions based on identified risks and context.
    """
    prompt = f"""
Based on the risks in this document and the context below:
- Region: {context['region']}
- Type of activism: {context['activism_type']}

Suggest:
1. Practical self-protection steps
2. Questions activists should ask
3. High-level advocacy points

Focus on safety, consent, and collective action.
Write one readable paragraph.

Text:
{text}
"""
    return chat_completions(model, prompt)
