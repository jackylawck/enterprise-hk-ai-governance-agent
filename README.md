# 🏆 Enterprise HR & AI Compliance Governance Brain
**Microsoft Agents League Hackathon 2026 — Enterprise Agents Track Submission**

---

## 📋 Overview
An enterprise-grade, production-ready AI governance agent built natively on the **Azure AI Foundry (v1.0.0 SDK)**. This autonomous brain acts as a digital regulatory auditor integrated into corporate workflows, evaluating human resources generative AI utilization requests against strict international standards and localized regional legal structures.

---

## 🛡️ Governance & Regulatory Framework Alignment
Designed and architected from a corporate governance perspective, this agent enforces compliance boundaries across the **4 IAPP AIGP Domains** and organizational risk structures:

* **ISO/IEC 42001:2023 Standard**: Enforces an AI Management System (AIMS) workflow to evaluate systemic algorithmic transparency, accountability, and risk proportionality.
* **IAPP AIGP Framework**: Directs pre-deployment Artificial Intelligence Impact Assessments (AIIA) and mandates ongoing deployment oversight.
* **Hong Kong Statutory Protections**:
    * **Data Privacy**: Aligned with the **Personal Data (Privacy) Ordinance (Cap. 486)**, mandating data minimization and pre-analysis de-identification pipelines.
    * **Algorithmic Fairness**: Mitigates automated decision-making (ADM) bias by auditing inputs against Hong Kong's anti-discrimination pillars (**Cap. 480 Sex, Cap. 487 Disability, Cap. 527 Family Status, and Cap. 602 Race Ordinances**).
* **Human-in-the-Loop (HITL)**: Enforces a mandatory executive verification boundary, backing every compliance output with an enterprise liability disclaimer.

---

## 🏗️ Technical Architecture
Built with reliability, reproducibility, and production safety in mind:

* **Orchestration**: Natively powered by the latest `azure-ai-projects` SDK Client Core (`AIProjectClient`).
* **Knowledge Grounding (RAG - Bring Your Own License)**: Uses the official Microsoft `FileSearchTool` integrated with a secure `VectorStore` to index the single source of truth (SSoT). 
* **Core System Guardrails**: Strict adherence to Hong Kong's anti-discrimination statutory pillars (Cap. 480, 487, 527, 602) is hardcoded directly into the agent's `SYSTEM_INSTRUCTIONS` prompt, ensuring baseline algorithmic fairness before RAG retrieval.
* **Reasoning Engine**: Defaulted to enterprise-grade `gpt-4o` for deep multi-step compliance reasoning.
* **Post-Deployment Self-Test**: Equipped with a robust `run_demo_query` hook that executes an automated end-to-end smoke test upon successful cloud provisioning.

---

## 🚀 Setup & Execution

### 1. Knowledge-Base Setup (Compliance & BYOL Policy)
This repository does not redistribute copyrighted standards or protected statutory PDF documents. To run the RAG grounding pipeline, users must obtain authorised copies of the applicable documents and place them locally in your configured directory:
* *ISO/IEC 42001:2023 International Standard Spec*
* *PCPD Artificial Intelligence: Personal Data Protection Framework*
* *Digital Policy Office: Ethical Artificial Intelligence Framework*
* *Digital Policy Office: Hong Kong Generative AI Technical and Application Guideline*

### 2. Environment Variables Configuration
The infrastructure client utilizes explicit environment variable injection to prevent hardcoded credentials:
```bash
export PROJECT_ENDPOINT="https://<your-resource-name>[.services.ai.azure.com/api/projects/](https://.services.ai.azure.com/api/projects/)<your-project-name>"
export MODEL_DEPLOYMENT_NAME="gpt-4o"
