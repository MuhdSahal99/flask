import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from mistralai import Mistral
from utils.text_processing import preprocess_text
from utils.resume_parser import parse_resume
import os 

os.environ["MISTRAL_API_KEY"] = "YAStnObU6ttfdXL5JucZfUFWo0z1PaiA"

class JobMatcher:
    def __init__(self, job_listing_path=None):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        if job_listing_path:
            self.jobs_df = pd.read_csv(job_listing_path)
            self.jobs_df['processed_description'] = self.jobs_df['description'].apply(preprocess_text)
            self.job_embeddings = self.model.encode(self.jobs_df['processed_description'].tolist())

        # Initialize mistral
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        self.client = Mistral(api_key=self.api_key)
        self.embedding_model = "mistral-embed"
        self.chat_model = "mistral-large-latest"

    def process_resume(self, resume_input):
        # Determine if the input is a file object or a string
        if hasattr(resume_input, 'read'):
            # It's a file object, so parse it
            resume_text = parse_resume(resume_input)
        elif isinstance(resume_input, str):
            # It's already a string, so use it directly
            resume_text = resume_input
        else:
            raise ValueError("Invalid input type. Expected file object or string.")

        processed_resume = preprocess_text(resume_text)
        resume_embedding = self.model.encode([processed_resume])[0]

        similarities = cosine_similarity([resume_embedding], self.job_embeddings)[0]
        top_indices = similarities.argsort()[-5:][::-1]

        recommendations = []
        for idx in top_indices:
            job_title = self.jobs_df.iloc[idx]['title']
            job_description = self.jobs_df.iloc[idx]['description']
            similarity = float(similarities[idx])

            # Use Gemini to generate a personalized job description
            prompt = f"""Based on the following job description and resume, provide advice for the candidate in the following format:

                Job Description:
                {job_description}

                Candidate's Resume:
                {resume_text}

                Please provide your response in the following format:

                ### Key Skills the Candidate Should Highlight
                [List 5-7 key skills the candidate should emphasize, based on the job description and their resume]

                ### Potential Interview Questions They Might Face
                [List 5-7 potential interview questions related to the job and the candidate's background]

                ### Tips for Tailoring Their Application
                [Provide 5-7 specific tips for the candidate to tailor their application to this job]

                Ensure each section is clearly separated and each point starts with a hyphen (-)."""

            response = self.client.chat.complete(
                model=self.chat_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]
            )
            personalized_description = response.choices[0].message.content

            recommendations.append((job_title, similarity, personalized_description))

        return recommendations

    def match_candidates(self, job_description, resumes):
        processed_job = preprocess_text(job_description)
        job_embedding = self.model.encode([processed_job])[0]

        processed_resumes = [preprocess_text(resume) for resume in resumes]
        resume_embeddings = self.model.encode(processed_resumes)

        similarities = cosine_similarity([job_embedding], resume_embeddings)[0]
        top_indices = similarities.argsort()[-5:][::-1]

        matches = []
        for idx in top_indices:
            resume = resumes[idx]
            similarity = float(similarities[idx])

            # Use Gemini to generate a match summary
            prompt = f"Based on the following job description and resume, provide a concise summary of why this candidate might be a good match:\n\nJob Description: {job_description}\n\nResume: {resume}"
            response = self.client.chat.complete(
                model=self.chat_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]
            )
            match_summary = response.choices[0].message.content

            matches.append((resume, similarity, match_summary))

        return matches