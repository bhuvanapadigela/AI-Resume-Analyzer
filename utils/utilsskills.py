skill_db = [
    "python",
    "java",
    "c++",
    "sql",
    "react",
    "nodejs",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "power bi",
    "tableau",
    "excel",
    "aws",
    "azure",
    "docker",
    "kubernetes"
]

def extract_skills(text):

    text = text.lower()

    found = []

    for skill in skill_db:
        if skill in text:
            found.append(skill)

    return found