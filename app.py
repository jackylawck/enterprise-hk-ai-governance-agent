import streamlit as st
import requests

# ==============================================================================
# Microsoft Agents League Hackathon (Adapted for Open-Source Sandbox)
# Project: HK-Enterprise HR & AI Compliance Governance Brain
# System Standard: ISO/IEC 42001:2023 | IAPP AIGP | HK Statutory Law
# Powered by: Streamlit & Hugging Face (Qwen 2.5)
# ==============================================================================

# 1. 網頁介面與標題設定
st.set_page_config(page_title="HK AI Governance Brain (Lite)", page_icon="🛡️", layout="wide")
st.title("🛡️ Hong Kong AI Compliance Governance Brain [Sandbox Lite]")
st.subheader("香港人工智能治理沙盒 (Open-Source Proof-of-Concept)")
st.markdown("---")

# 2. 獲取 Hugging Face 密鑰 (Secrets Vault)
try:
    hf_token = st.secrets["HF_TOKEN"]
except KeyError:
    st.error("🚨 [CONFIG ERROR] 找不到 HF_TOKEN。請確保已在 Streamlit Secrets 中設定。")
    st.stop()

# 👉 核心升級：改用免審批、速度極快且中文理解極強的 Qwen 2.5 開源模型
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"
HEADERS = {"Authorization": f"Bearer {hf_token}"}

# 3. 完美移植你的高階系統管治提示詞 (System Instructions)
SYSTEM_INSTRUCTIONS = (
    "You are the 'Enterprise HR & AI Compliance Governance Brain', an elite risk-auditing agent "
    "designed for integration with Microsoft 365 Copilot and enterprise HR workflows. Your directive is to evaluate "
    "generative AI utilization requests within HR departments against the Primary Governance Reference Framework, "
    "which includes the IAPP AIGP framework, ISO/IEC 42001, and localized Hong Kong legal structures.\n\n"
    "【Mandatory Compliance Boundaries】\n"
    "1. Data Privacy & Minimization: Enforce strict compliance with the HK Personal Data (Privacy) Ordinance (Cap. 486). "
    "Instruct users that candidate resumes or performance files must undergo de-identification pipelines prior to core analysis.\n"
    "2. Algorithmic Non-Discrimination & Fairness: Mitigate Automated Decision-Making (ADM) bias by strict cross-referencing against "
    "Hong Kong's statutory pillars (Cap. 480, Cap. 487, Cap. 527, Cap. 602).\n"
    "3. AI Deployment Governance: Mandate pre-deployment Artificial Intelligence Impact Assessments (AIIA).\n\n"
    "【Output Blueprint Specification】\n"
    "Structure your compliance advice using professional board-level terminology across these headings:\n"
    "- ⚖️ Localized Statutory Risk Assessment\n"
    "- 🛡️ ISO/IEC 42001 & AIGP Operational Alignment\n"
    "- 📊 Artificial Intelligence Impact Assessment (AIIA) Summary\n"
    "- ✅ Mandatory Recommended Actions\n"
    "- ❌ Restricted Operational Practices\n\n"
    "CRITICAL: Conclude with a liability disclaimer stating this constitutes algorithmic advice and requires immediate HITL executive verification."
)

# 4. 側邊欄狀態顯示
with st.sidebar:
    st.success("✅ 系統狀態: 運行中 (SECURE)")
    st.info("🧠 驅動引擎: Qwen-2.5-7B-Instruct")
    st.warning("⚠️ 資源狀態: 由於使用免費開源端點，本地 PDF 知識庫 (Knowledge Base) 暫時停用，將依賴模型預訓練知識及系統提示詞進行推理。")

# 5. 用戶互動區
st.markdown("### 📝 提交方案進行合規審計")
default_query = "Our HR team wants to use an AI tool to automatically screen 500 candidate CVs and rank them by suitability score. What are the compliance requirements under HK law?"
user_input = st.text_area("描述您的 AI 使用案例 (Use Case)：", value=default_query, height=100)

if st.button("🚀 運行治理審計分析 (Run Compliance Audit)", type="primary"):
    if user_input:
        with st.spinner("AI 審計官正在評估架構風險，請稍候..."):
            
            # 使用 Qwen 的專屬 ChatML Prompt 格式
            prompt = f"<|im_start|>system\n{SYSTEM_INSTRUCTIONS}<|im_end|>\n<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 1024, # 確保能輸出完整的報告
                    "temperature": 0.3,     # 保持合規建議的嚴謹性
                    "return_full_text": False
                }
            }
            
            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    # 提取模型生成的文本
                    generated_text = result[0].get("generated_text", "")
                    
                    st.markdown("---")
                    st.markdown("### 📊 審計報告 (Audit Report)")
                    st.write(generated_text)
                else:
                    st.error(f"連線失敗！狀態碼：{response.status_code}。錯誤詳情：{response.text}")
            except Exception as e:
                st.error(f"系統發生嚴重錯誤：{str(e)}")
    else:
        st.warning("請輸入使用案例以進行評估。")
