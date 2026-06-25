from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_ats(resume, jd):

    cv = CountVectorizer()

    matrix = cv.fit_transform([resume, jd])

    similarity = cosine_similarity(matrix)

    score = similarity[0][1] * 100

    return round(score, 2)