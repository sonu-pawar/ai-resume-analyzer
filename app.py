import re
import fitz
import streamlit as st

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "SQL": ["sql"],
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "NLP": ["nlp", "natural language processing"],
    "Excel": ["excel"],
    "Power BI": ["power bi"],
    "HTML": ["html"],
    "CSS": ["css"],
    "JavaScript": ["javascript"],
    "React": ["react"],
    "Git": ["git", "github"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],
    "Communication": ["communication"],
    "Problem Solving": ["problem solving", "problem-solving"],
}


def extract_pdf_text(file):
    with fitz.open(
        stream=file.getvalue(),
        filetype="pdf"
    ) as pdf:
        return "\n".join(page.get_text() for page in pdf)


def find_skills(text):
    text = text.lower()
    found = []

    for skill, aliases in SKILLS.items():
        for alias in aliases:
            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )
            if re.search(pattern, text):
                found.append(skill)
                break

    return sorted(found)


st.title("📄 AI Resume Analyzer")
st.write(
    "Compare your resume with a job description "
    "and identify matching skills."
)

uploaded = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

job = st.text_area(
    "Paste the job description",
    height=200
)

if st.button("Analyze Resume", type="primary"):
    if uploaded is None:
        st.error("Please upload a PDF resume.")
    elif not job.strip():
        st.error("Please enter a job description.")
    else:
        try:
            resume_text = extract_pdf_text(uploaded)

            if not resume_text.strip():
                st.error(
                    "No selectable text found. "
                    "Scanned PDFs need OCR support."
                )
            else:
                resume_skills = set(find_skills(resume_text))
                job_skills = set(find_skills(job))

                if not job_skills:
                    st.warning(
                        "No supported skills found "
                        "in the job description."
                    )
                else:
                    matched = sorted(
                        resume_skills & job_skills
                    )
                    missing = sorted(
                        job_skills - resume_skills
                    )
                    score = round(
                        100 * len(matched) / len(job_skills)
                    )

                    st.header("Analysis Results")
                    a, b, c = st.columns(3)
                    a.metric("Match Score", f"{score}%")
                    b.metric("Matched Skills", len(matched))
                    c.metric("Potential Gaps", len(missing))

                    st.progress(score / 100)

                    st.caption(
                        "This is a keyword-overlap score, "
                        "not a prediction of hiring success."
                    )

                    left, right = st.columns(2)

                    with left:
                        st.subheader("✅ Matching Skills")
                        if matched:
                            for skill in matched:
                                st.write(f"- {skill}")
                        else:
                            st.write("No matching skills detected.")

                    with right:
                        st.subheader("📚 Potential Skill Gaps")
                        if missing:
                            for skill in missing:
                                st.write(f"- {skill}")
                        else:
                            st.write("No detected skill gaps.")

                    st.subheader("💡 Suggested Next Steps")
                    if missing:
                        st.write(
                            "Consider learning these skills if "
                            "they are relevant to your goals: "
                            + ", ".join(missing)
                        )
                        st.write(
                            "Only add skills to your resume "
                            "when you genuinely have them."
                        )
                    else:
                        st.write(
                            "Review your experience and projects "
                            "to demonstrate your skills."
                        )

                    report = (
                        f"Resume Match Score: {score}%\n"
                        f"Matched Skills: {', '.join(matched)}\n"
                        f"Potential Gaps: {', '.join(missing)}\n"
                    )

                    st.download_button(
                        "Download Report",
                        data=report,
                        file_name="resume_analysis.txt",
                        mime="text/plain"
                    )

        except Exception:
            st.error(
                "Unable to read this PDF. "
                "Please try another valid PDF."
            )
