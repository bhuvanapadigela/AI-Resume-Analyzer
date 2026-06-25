import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pdfplumber
from docx import Document
import re
from collections import Counter

st.set_page_config(
    page_title="AI Career Intelligence Platform",
    layout="wide"
)

# -----------------------------
# JOB DATABASE
# -----------------------------

JOB_DATABASE = {
    "Data Analyst": {
        "skills": [
            "python","sql","excel",
            "power bi","tableau",
            "pandas"
        ],
        "salary":"6-12 LPA"
    },

    "Data Scientist": {
        "skills":[
            "python","machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "sql"
        ],
        "salary":"8-20 LPA"
    },

    "ML Engineer":{
        "skills":[
            "python",
            "machine learning",
            "docker",
            "aws",
            "tensorflow",
            "pytorch"
        ],
        "salary":"10-25 LPA"
    },

    "Backend Developer":{
        "skills":[
            "python",
            "django",
            "flask",
            "mysql",
            "postgresql"
        ],
        "salary":"5-15 LPA"
    },

    "Frontend Developer":{
        "skills":[
            "react",
            "javascript",
            "html",
            "css"
        ],
        "salary":"5-12 LPA"
    },

    "Full Stack Developer":{
        "skills":[
            "react",
            "nodejs",
            "mongodb",
            "javascript"
        ],
        "salary":"7-18 LPA"
    },

    "AI Engineer":{
        "skills":[
            "python",
            "nlp",
            "deep learning",
            "transformers",
            "llm"
        ],
        "salary":"12-30 LPA"
    }
}

# -----------------------------
# SKILL LIST
# -----------------------------

ALL_SKILLS = list(set(
    skill
    for job in JOB_DATABASE.values()
    for skill in job["skills"]
))

# -----------------------------
# RESUME PARSER
# -----------------------------

def extract_text(uploaded_file):

    text = ""

    if uploaded_file.name.endswith(".pdf"):

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                if page.extract_text():
                    text += page.extract_text()

    elif uploaded_file.name.endswith(".docx"):

        doc = Document(uploaded_file)

        for para in doc.paragraphs:
            text += para.text

    return text.lower()

# -----------------------------
# SKILL EXTRACTION
# -----------------------------

def extract_skills(text):

    found = []

    for skill in ALL_SKILLS:

        if skill.lower() in text:
            found.append(skill)

    return list(set(found))

# -----------------------------
# EXPERIENCE
# -----------------------------

def get_experience(text):

    patterns = [
        r'(\d+)\+?\s+years',
        r'(\d+)\+?\s+yrs',
        r'(\d+)\+?\s+year'
    ]

    for p in patterns:

        match = re.search(
            p,
            text.lower()
        )

        if match:
            return int(match.group(1))

    return 0

# -----------------------------
# EDUCATION
# -----------------------------

def detect_education(text):

    degrees = []

    keywords = [
        "b.tech",
        "bachelor",
        "m.tech",
        "master",
        "phd"
    ]

    for k in keywords:

        if k in text:
            degrees.append(k)

    return degrees

# -----------------------------
# JOB MATCHING
# -----------------------------

def recommend_jobs(skills):

    recommendations = []

    for role,data in JOB_DATABASE.items():

        required = data["skills"]

        matched = len(
            set(skills) &
            set(required)
        )

        score = (
            matched /
            len(required)
        ) * 100

        missing = list(
            set(required)
            -
            set(skills)
        )

        recommendations.append({

            "Role": role,
            "Match Score":
            round(score,2),

            "Salary":
            data["salary"],

            "Missing Skills":
            ", ".join(missing)
        })

    return pd.DataFrame(
        recommendations
    ).sort_values(
        by="Match Score",
        ascending=False
    )

# -----------------------------
# CAREER PROFILE
# -----------------------------

def generate_profile(skills):

    if "machine learning" in skills:
        return "AI / Machine Learning Professional"

    elif "react" in skills:
        return "Web Developer"

    elif "sql" in skills:
        return "Data Analyst"

    else:
        return "General Software Engineer"

# -----------------------------
# UI
# -----------------------------

st.title(
    "🚀 AI Career Intelligence Platform"
)

resume = st.file_uploader(
    "Upload Resume",
    type=["pdf","docx"]
)

if resume:

    text = extract_text(resume)

    skills = extract_skills(text)

    exp = get_experience(text)

    edu = detect_education(text)

    profile = generate_profile(skills)

    jobs = recommend_jobs(skills)

    # -----------------
    # METRICS
    # -----------------

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Skills Found",
        len(skills)
    )

    c2.metric(
        "Experience",
        exp
    )

    c3.metric(
        "Education",
        len(edu)
    )

    c4.metric(
        "Job Matches",
        len(jobs)
    )

    # -----------------
    # PROFILE
    # -----------------

    st.header(
        "Career Profile"
    )

    st.success(profile)

    # -----------------
    # SKILLS
    # -----------------

    st.header(
        "Detected Skills"
    )

    st.write(skills)

    # -----------------
    # TOP JOBS
    # -----------------

    st.header(
        "Recommended Jobs"
    )

    st.dataframe(
        jobs,
        use_container_width=True
    )

    # -----------------
    # MATCH CHART
    # -----------------

    fig = px.bar(
        jobs.head(10),
        x="Role",
        y="Match Score",
        color="Match Score",
        title="Job Match Scores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------
    # BEST MATCH
    # -----------------

    best_job = jobs.iloc[0]

    st.header(
        "Best Career Match"
    )

    st.success(
        f"""
        Role: {best_job['Role']}

        Match: {best_job['Match Score']}%

        Expected Salary:
        {best_job['Salary']}
        """
    )

    # -----------------
    # SKILL GAP
    # -----------------

    st.header(
        "Skill Gap Analysis"
    )

    st.warning(
        best_job["Missing Skills"]
    )

    # -----------------
    # RESUME STRENGTH
    # -----------------

    score = min(
        100,
        len(skills)*8 +
        exp*5
    )

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={
                "text":
                "Resume Strength"
            }
        )
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    # -----------------
    # CAREER ROADMAP
    # -----------------

    st.header(
        "Career Roadmap"
    )

    st.info(
        f"""
        To become a stronger
        {best_job['Role']},

        learn:
        {best_job['Missing Skills']}
        """
    )

    # -----------------
    # DOWNLOAD REPORT
    # -----------------

    csv = jobs.to_csv(
        index=False
    )

    st.download_button(
        "Download Career Report",
        csv,
        "career_report.csv",
        "text/csv"
    )