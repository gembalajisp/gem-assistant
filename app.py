from google import genai
from pypdf import PdfReader
import streamlit as st

st.set_page_config(
    page_title="GeM Online Assistant",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("🛡️ Online GeM Assistant")
st.caption("Cloud Hosted | Mobile Friendly | Free AI Audit")

st.subheader("Tender Document Compliance Audit")

company_profile = st.text_area(
    "Your Company Profile & Documents",
    value="""- GST Registered
- MSME / Udyam Registered
- Annual Turnover: ₹50 Lakhs
- ISO 9001 Certified
- Past Experience: 3 Government supply orders completed""",
    height=120,
)

uploaded_file = st.file_uploader("Upload GeM Tender ATC PDF", type=["pdf"])

if uploaded_file and st.button("Run Cloud AI Audit", use_container_width=True):
    with st.spinner("Analyzing document using Cloud Gemini AI..."):
        try:
            reader = PdfReader(uploaded_file)
            tender_text = "".join(
                [page.extract_text() or "" for page in reader.pages]
            )

            # Securely retrieve API key from Streamlit Cloud Secrets
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

            prompt = f"""
            You are an expert GeM Tender Consultant. Compare the Tender text against the Company Profile.
            
            TENDER TEXT SNIPPET:
            {tender_text[:4000]}
            
            COMPANY PROFILE:
            {company_profile}
            
            TASK:
            1. Extract main qualification criteria (Turnover, Experience, MSME, ISO, etc.).
            2. Mark each requirement as PASS or MISSING based on the company profile.
            3. Highlight any critical penalty or strict delivery clauses.
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )

            st.markdown("### Audit Report")
            st.markdown(response.text)

        except Exception as e:
            st.error(
                f"Error running cloud analysis. Check your Gemini API key in Streamlit secrets. Details: {str(e)}"
            )
