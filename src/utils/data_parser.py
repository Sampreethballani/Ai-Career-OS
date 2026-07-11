import re
from datetime import datetime

def parse_salary(text):
    if not text:
        return None
    patterns = [
        r'(?:₹|Rs\.?|INR)\s?([\d,]+)\s*(?:-|to|–)\s*(?:₹|Rs\.?|INR)?\s?([\d,]+)',
        r'\$([\d,]+)\s*(?:-|to|–)\s*\$?([\d,]+)',
        r'(?:₹|Rs\.?|INR)\s?([\d,]+)\s*/\s*(?:month|yr|year)',
        r'\$([\d,]+)\s*/\s*(?:month|yr|year)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) == 2:
                return {"min": int(groups[0].replace(",", "")), "max": int(groups[1].replace(",", ""))}
            return {"min": int(groups[0].replace(",", "")), "max": None}
    return None


def parse_date(text):
    if not text:
        return None
    formats = [
        "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y",
        "%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(text.strip(), fmt)
        except ValueError:
            continue
    return None


def normalize_location(location):
    if not location:
        return "N/A"
    location = location.strip()
    known_remote = ["remote", "work from home", "wfh", "anywhere", "online"]
    if location.lower() in known_remote:
        return "Remote"
    return location


def extract_skills(text):
    if not text:
        return []
    skills_keywords = [
        "python", "java", "c++", "javascript", "typescript", "go", "rust",
        "tensorflow", "pytorch", "keras", "jax", "langchain", "llm",
        "machine learning", "deep learning", "nlp", "computer vision",
        "transformers", "bert", "gpt", "rag", "fine-tuning",
        "docker", "kubernetes", "aws", "gcp", "azure",
        "sql", "mongodb", "redis", "postgresql",
        "fastapi", "flask", "django", "spring",
        "git", "linux", "rest api", "graphql",
    ]
    text_lower = text.lower()
    found = []
    for skill in skills_keywords:
        if skill in text_lower:
            found.append(skill)
    return found


def clean_html(html_text):
    if not html_text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', html_text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean
