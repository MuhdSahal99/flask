import streamlit as st
from job_matcher import JobMatcher

def show():
    st.title("AI Recruiter: Precision Candidate Finder")

    # Input for job description
    job_description = st.text_area("Enter the job description")

    # Input for resumes
    st.subheader("Enter Candidate Resumes")
    resumes = []
    for i in range(5):  # Allow up to 5 resumes
        resume = st.text_area(f"Resume {i+1}", key=f"resume_{i}")
        if resume:
            resumes.append(resume)

    if st.button("Find Matching Candidates"):
        if job_description and resumes:
            # Initialize JobMatcher
            job_matcher = JobMatcher()

            # Process the job description and resumes
            matches = job_matcher.match_candidates(job_description, resumes)

            # Display matches
            st.subheader("Top Candidate Matches:")
            for i, (resume, similarity, summary) in enumerate(matches, 1):
                st.write(f"{i}. Candidate {i}")
                st.write(f"Match: {similarity * 100:.2f}%")
                st.write(f"   Summary: {summary}")
                st.write("---")
        else:
            st.warning("Please enter a job description and at least one resume.")