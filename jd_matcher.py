from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text: str, job_description: str) -> dict:
    texts = [resume_text, job_description]

    vectorizer = TfidfVectorizer().fit_transform(texts)
    similarity_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    score = round(similarity_matrix[0][0] * 100, 2)

    return {
        "match_score_percent": score,
        "message": get_feedback(score)
    }

def get_feedback(score):
    if score > 80:
        return "Excellent match! You're highly suitable."
    elif score > 60:
        return "Good match. Consider adding more relevant keywords."
    elif score > 40:
        return "Average match. Try tailoring your resume better."
    else:
        return "Low match. Consider customizing your resume deeply."
