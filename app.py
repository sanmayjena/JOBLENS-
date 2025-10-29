import streamlit as st
from src.helper import extract_text_from_pdf,ask_openrouter
from src.job_api import fetch_linkedin_jobs,fetch_naukri_jobs
import base64


def set_background(image_file):
    # Read image and convert to base64
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

    # Inject custom CSS
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Set your background image ---
set_background("Purple Color Background Wallpaper Best HD.jpg")

st.set_page_config(page_title = "JOB LENS", layout="wide")
st.title("JOBLENS 💼🔍")
st.markdown(""""Unlock your career potential with JobLens — your AI-powered guide from resume to offer letter.
Built for ambitious students and professionals, JobLens helps you take charge of your career journey with clarity and confidence.

Tired of sending resumes with no replies? Unsure what skills to learn next? JobLens turns confusion into action with smart, personalized insights.

Key Features:
Key Features:

*   📄 Instant Resume Summary Get a professional, recruiter-ready summary in seconds that highlights your strengths.
*   💡 Skill Gap Analysis See what’s missing to land your dream role by comparing your skills to top industry requirements.
*   🗺️ Learning Roadmap Follow a custom plan with recommended courses to close your gaps fast.
*   🎯 AI Job Matching Find roles tailored to your skills from platforms like LinkedIn and Naukri.
Whether you’re launching your career, aiming higher, or switching paths — JobLens gives you the clarity, confidence, and tools to succeed.""")

uploaded_file = st.file_uploader("Upload your resume (PDF format only)", type=["pdf"])

if uploaded_file:
    with st.spinner("⏳ Processing your resume... finding top opportunities for you! 💫"):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("📄Summarizing your resume..."):
        summary = ask_openrouter(f"Summarize the following resume highlighting skills, education, and experience:\n\n{resume_text}", max_tokens=400)
 
    with st.spinner("Finding skill Gaps ...."):
        gaps = ask_openrouter(f"Analyze this resume and highlight missing skills,certifications and expericences needed for better job oppurtunities:/n/n{resume_text}" ,max_tokens=400)

    with st.spinner("Finding skill Gaps ...."):
        roadmap = ask_openrouter(f"Based on this resume suggest a future roadmap to improve this person career prospects(skills to learn,certification needed,industry exposure):/n/n{resume_text}" ,max_tokens=400)       

    st.markdown("----")
    st.header("📄 Resume Summary:")
    st.markdown(f"<div style='background-color:#eaf4fc; padding:15px; border-radius:10px; font-size:16px; color-white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("----")
    st.header("🛠️Identified Skill Gaps:")
    st.markdown(f"<div style='background-color:#fcebea; padding:15px; border-radius:10px; font-size:16px; color-white;'>{gaps}</div>", unsafe_allow_html=True)

    st.markdown("----")
    st.header("🚀 Career Roadmap:")
    st.markdown(f"<div style='background-color:#e8f7e4; padding:15px; border-radius:10px; font-size:16px; color-white;'>{roadmap}</div>", unsafe_allow_html=True)

    st.success("✅ Analysis Completed Successfully. Best of luck! 🍀")


    if st.button("🔎GET JOB RECOMMENDATIONS"):
        with st.spinner("Searching for top job openings..."):
            keywords = ask_openrouter(f"Based on this resume summary, suggest top 5 job titles/roles that best match the candidate's profile. Provide only the job titles separated by commas. No explanation.\n\n SUMMARY :{summary}", max_tokens=100)
            search_keywords_clean = keywords.replace("\n", "").strip()

        st.success(f"Extracted Job Titles: {search_keywords_clean}")
 
        with st.spinner("Fetching LinkedIn and Naukri job listings..."):
            linkdein_jobs= fetch_linkedin_jobs(search_keywords_clean,rows=50)
            naukri_jobs= fetch_naukri_jobs(search_keywords_clean,rows=50)  

            st.markdown("----")
            st.header("💼 LinkedIn Job Recommendations")

            if linkdein_jobs:
                for job in linkdein_jobs:
                    st.markdown(f"**{job.get('title')} at {job.get('companyName')}")
                    st.markdown(f" 📍{job.get('location')}")
                    st.markdown(f"**Posted On:** {job.get('listedAt')}")
                    st.markdown(f"**Job Type:** {job.get('employmentType')}")
                    st.markdown(f"Apply Link 🔗[Link]({job.get('link')})")
                    st.markdown("---")
            else:
                st.warning("No LinkedIn jobs found matching your profile.")

            st.markdown("----")
            st.header("💼 Naukri Job Recommendations")

            if naukri_jobs:
                for job in naukri_jobs:
                    st.markdown(f"**{job.get('title')} at {job.get('companyName')}")
                    st.markdown(f" 📍{job.get('location')}")
                    st.markdown(f"**Posted On:** {job.get('postedDate')}")
                    st.markdown(f"**Experience Required:** {job.get('experience')}")
                    st.markdown(f"Apply Link 🔗[Link]({job.get('url')})")
                    st.markdown("---")  
            else:
                st.warning("No Naukri jobs found matching your profile.")




