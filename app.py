import os
import sys
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FileSearchTool

# ==============================================================================
# Microsoft Agents League Hackathon Submission: Enterprise Agents Track
# Project: HK-Enterprise HR & AI Compliance Governance Brain
# System Standard: ISO/IEC 42001:2023 | IAPP AIGP | HK Statutory Law
# Requires: azure-ai-projects==2.2.0, azure-identity>=1.15.0,<3.0.0
# ==============================================================================

KB_DIR = os.environ.get("KB_DIR", os.path.dirname(os.path.abspath(__file__)))
REQUIRE_KB = os.environ.get("REQUIRE_KB", "true").lower() == "true"

KB_FILES = [
    os.path.join(KB_DIR, "PCPD_ai_protection_framework.pdf"),
    os.path.join(KB_DIR, "Digital_Policy_Office_Ethical_AI_Framework_en.pdf"),
    os.path.join(KB_DIR, "Digital_Policy_Office_HK_GenAI_Technical_Guideline_en.pdf"),
    os.path.join(KB_DIR, "ISOIEC_42001_2023_International_Standard.pdf"),
]

SYSTEM_INSTRUCTIONS = (
    "You are the 'Enterprise HR & AI Compliance Governance Brain', an elite risk-auditing agent "
    "designed for integration with Microsoft 365 Copilot and enterprise HR workflows. Your directive is to evaluate "
    "generative AI utilization requests within HR departments against the Primary Governance Reference Framework, "
    "which includes the IAPP AIGP framework, ISO/IEC 42001, and localized Hong Kong legal structures.\n\n"

    "【Mandatory Compliance Boundaries - Primary Governance Reference Framework】\n"
    "1. Data Privacy & Minimization: Enforce strict compliance with the HK Personal Data (Privacy) Ordinance (Cap. 486). "
    "Instruct users that candidate resumes or performance files must undergo de-identification pipelines prior to core analysis.\n"
    "2. Algorithmic Non-Discrimination & Fairness: Mitigate Automated Decision-Making (ADM) bias by strict cross-referencing against "
    "Hong Kong's statutory pillars, including Cap. 480, Cap. 487, Cap. 527, and Cap. 602. Ensure output maintains algorithmic fairness.\n"
    "3. AI Deployment Governance: Mandate pre-deployment Artificial Intelligence Impact Assessments (AIIA), "
    "enforce transparency and explainability in HR AI use cases, and establish continuous post-deployment monitoring protocols.\n\n"

    "【Output Blueprint Specification】\n"
    "You must structure your compliance advice using professional board-level governance terminology across these exact headings:\n"
    "- ⚖️ Localized Statutory Risk Assessment (Evaluating Legal & Boardroom Exposure)\n"
    "- 🛡️ ISO/IEC 42001 & AIGP Operational Alignment (Processes & Framework Mapping)\n"
    "- 📊 Artificial Intelligence Impact Assessment (AIIA) Summary (Risk Proportionality)\n"
    "- ✅ Mandatory Recommended Actions (Do's for Corporate HR Personnel)\n"
    "- ❌ Restricted Operational Practices (Don'ts to Mitigate High-Stakes Violations)\n\n"

    "CRITICAL: Conclude every single assessment with a standardized enterprise liability disclaimer stating that the output "
    "constitutes algorithmic advice and requires immediate Human-in-the-Loop (HITL) executive verification before operational rollout."
)


def _upload_kb_files(client: AIProjectClient) -> list[str]:
    """Upload existing KB files; raise error or skip gracefully based on REQUIRE_KB."""
    file_ids: list[str] = []

    for filepath in KB_FILES:
        if os.path.exists(filepath):
            with open(filepath, "rb") as fh:
                uploaded = client.agents.upload_file_and_poll(
                    file=fh,
                    purpose="assistants",
                )
            file_ids.append(uploaded.id)
            print(f"[LOG] Uploaded: {os.path.basename(filepath)} -> ID: {uploaded.id}")
        else:
            msg = f"KB file not found at path: {filepath}"
            if REQUIRE_KB:
                raise FileNotFoundError(msg)
            print(f"[WARN] {msg}, skipping.")

    return file_ids


def _build_file_search_tool(client: AIProjectClient, file_ids: list[str]):
    """Build FileSearchTool only when real file IDs are available."""
    if not file_ids:
        print("[WARN] No KB files uploaded. Agent will run without grounded knowledge base.")
        return None, None

    vector_store = client.agents.create_vector_store_and_poll(
        file_ids=file_ids,
        name="HK-HR-AI-Governance-AIMS-KV",
    )

    tool = FileSearchTool(vector_store_ids=[vector_store.id])
    print(f"[SUCCESS] VectorStore created. ID: {vector_store.id}")

    return tool.definitions, tool.resources


def deploy_governance_agent(client: AIProjectClient):
    """Deploy the HK HR AI Governance Agent with File Search grounding."""
    print("[LOG] Starting Enterprise Governance Agent Deployment Sequence...")

    print("[LOG] Indexing HK regulatory frameworks into VectorStore...")
    file_ids = _upload_kb_files(client)
    tool_definitions, tool_resources = _build_file_search_tool(client, file_ids)

    print("[LOG] Provisioning Enterprise Governance Agent...")
    model_name = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o")

    create_kwargs = {
        "model": model_name,
        "name": "Enterprise-HR-AI-Governance-Brain",
        "instructions": SYSTEM_INSTRUCTIONS,
    }

    if tool_definitions:
        create_kwargs["tools"] = tool_definitions
        create_kwargs["tool_resources"] = tool_resources

    agent = client.agents.create_agent(**create_kwargs)

    print(f"[SUCCESS] Enterprise Governance Agent activated. ID: {agent.id}")
    return agent


def _extract_message_text(message) -> str:
    """Best-effort extraction of assistant message text across SDK response shapes."""
    parts = []

    for item in getattr(message, "content", []) or []:
        text_obj = getattr(item, "text", None)

        if text_obj is not None:
            value = getattr(text_obj, "value", None)
            if value:
                parts.append(value)
                continue

        if isinstance(item, dict):
            text = item.get("text")
            if isinstance(text, dict) and text.get("value"):
                parts.append(text["value"])
            elif isinstance(text, str):
                parts.append(text)

    return "\n".join(parts).strip()


def run_demo_query(agent, client: AIProjectClient):
    """Quick smoke-test: proves File Search + Compliance Blueprint works end-to-end."""
    test_query = (
        "Our HR team wants to use an AI tool to automatically screen 500 candidate CVs "
        "and rank them by suitability score. What are the compliance requirements under HK law?"
    )

    print("\n" + "=" * 70)
    print("[DEMO] Running post-deployment compliance query...")
    print(f"[DEMO] User Input: '{test_query}'")
    print("=" * 70)

    thread = client.agents.create_thread()

    client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=test_query,
    )

    run = client.agents.create_and_process_run(
        thread_id=thread.id,
        agent_id=agent.id,
    )

    print(f"[DEMO] Run processed with status: {run.status}")

    messages = client.agents.list_messages(thread_id=thread.id)

    assistant_response_found = False

    for msg in messages.data:
        if getattr(msg, "role", None) == "assistant":
            response_text = _extract_message_text(msg)
            print(f"\n[AGENT RESPONSE]\n{response_text or '[No assistant text content found]'}\n")
            assistant_response_found = True
            break

    if not assistant_response_found:
        print("[WARN] No assistant response found in thread messages.")

    print("=" * 70)


def main():
    project_endpoint = os.environ.get("PROJECT_ENDPOINT")

    if not project_endpoint:
        print("[CONFIG ERROR] PROJECT_ENDPOINT is not set.", file=sys.stderr)
        print(
            "Expected format: https://<resource>.services.ai.azure.com/api/projects/<name>",
            file=sys.stderr,
        )
        sys.exit(1)

    client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(),
    )

    try:
        deployed_agent = deploy_governance_agent(client)

        if deployed_agent:
            run_demo_query(deployed_agent, client)

    except FileNotFoundError as fnf_err:
        print(f"\n[FILE ERROR] {fnf_err}", file=sys.stderr)
        print(
            "[HINT] Ensure all 4 PDFs are uploaded to the exact same directory as app.py, "
            "or set KB_DIR to the folder containing the PDFs.",
            file=sys.stderr,
        )
        sys.exit(2)

    except Exception as error:
        print(f"\n[CRITICAL ERROR] {error}", file=sys.stderr)
        sys.exit(3)

    finally:
        if hasattr(client, "close"):
            client.close()
        print("[LOG] AIProjectClient connection safely closed. Deployment script finished.")


if __name__ == "__main__":
    main()
