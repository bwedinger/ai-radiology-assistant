import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using your API key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🧠 AI Radiology Dictation Assistant")
st.markdown("Dictate or paste your radiology case details below. The assistant will ask clarifying questions and generate a structured report.")

# Step 1: Input the case
case_input = st.text_area("🗣️ Case Dictation", placeholder="E.g., CT Abdomen shows a 2.5 cm liver lesion in segment VIII...", height=200)

if st.button("Generate Questions and Report"):
    if not case_input.strip():
        st.warning("Please enter case details first.")
    else:
        with st.spinner("💬 Thinking..."):

            # Step 2: Ask the model to generate follow-up questions
            prompt_qs = (
                "You are a radiology assistant. Based on this dictated case, ask 2–3 concise follow-up questions "
                "to clarify or improve the final report:\n\n" + case_input
            )

            q_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt_qs}],
                temperature=0.4,
            )

            followup_questions = q_response.choices[0].message.content.strip()
            st.subheader("🤔 Suggested Follow-up Questions")
            st.markdown(followup_questions)

            # Step 3: Use case input to generate a clean report with impression
            prompt_report = (
                "You are a radiology AI assistant. Read the following case dictation and generate a concise, "
                "structured radiology report with headings (FINDINGS and IMPRESSION):\n\n" + case_input
            )

            report_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt_report}],
                temperature=0.3,
            )

            final_report = report_response.choices[0].message.content.strip()
            st.subheader("📄 Final Report")
            st.text(final_report)
