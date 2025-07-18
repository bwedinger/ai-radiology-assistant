import streamlit as st
import openai

st.title("🧠 AI Radiology Dictation Assistant")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Step 1: Dictation
dictation = st.text_area("🗣️ Dictate your case here:")

if dictation:
    # Step 2: Generate follow-up questions
    with st.spinner("🤖 Thinking..."):
        prompt_qs = f"You are a radiology assistant. The radiologist dictated the following case: {dictation}\n\nSuggest 2-3 specific follow-up questions to clarify findings."
        q_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt_qs}],
            temperature=0.4
        )
        questions = q_response.choices[0].message.content
        st.subheader("🔍 Suggested Follow-up Questions:")
        st.write(questions)

    # Step 3: Generate structured report
    if st.button("📝 Generate Report"):
        with st.spinner("Compiling report..."):
            prompt_report = f"Write a structured radiology report and impression based on this dictation: {dictation}"
            report_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt_report}],
                temperature=0.3
            )
            report = report_response.choices[0].message.content
            st.subheader("📄 Structured Report:")
            st.write(report)
