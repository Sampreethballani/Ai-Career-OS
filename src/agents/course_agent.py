import requests
from bs4 import BeautifulSoup
from src.agents.base_agent import BaseAgent

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}

class CourseAgent(BaseAgent):
    def __init__(self):
        super().__init__("course_agent")
        self.category = "course"

    def _scrape_class_central(self):
        results = []
        try:
            url = "https://www.classcentral.com/search?q=ai+machine+learning+llm"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results
            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select(".course-list-card, .course-card, .course")[:8]:
                try:
                    title_el = card.select_one(".course-name, .name, h2, h3")
                    provider_el = card.select_one(".provider, .institution, .source")
                    link_el = card.select_one("a[href*='/course/'], a[href*='/university/']")

                    title = title_el.get_text(strip=True) if title_el else None
                    provider = provider_el.get_text(strip=True) if provider_el else "Unknown"
                    link = link_el["href"] if link_el and link_el.get("href") else None

                    if title and link:
                        if not link.startswith("http"):
                            link = "https://www.classcentral.com" + link
                        results.append({
                            "title": title,
                            "company": provider,
                            "location": "Online",
                            "link": link,
                            "description": f"Online course: {title} by {provider}",
                            "category": self.category,
                            "source": "Class Central",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Class Central scrape failed: {e}")
        return results

    def _scrape_coursera(self):
        results = []
        try:
            url = "https://www.coursera.org/search?query=AI+machine+learning+LLM&index=prod_all_products"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results
            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select(".cds-ProductCard, .card-content, .card")[:8]:
                try:
                    title_el = card.select_one(".cds-ProductCard-title, .card-title, h3")
                    provider_el = card.select_one(".cds-ProductCard-partner, .partner-name, .provider")
                    link_el = card.select_one("a[href*='/learn/'], a[href*='/specializations/']")

                    title = title_el.get_text(strip=True) if title_el else None
                    provider = provider_el.get_text(strip=True) if provider_el else "Coursera"
                    link = link_el["href"] if link_el and link_el.get("href") else None

                    if title and link:
                        if not link.startswith("http"):
                            link = "https://www.coursera.org" + link
                        results.append({
                            "title": title,
                            "company": provider,
                            "location": "Online",
                            "link": link,
                            "description": f"Coursera course: {title}",
                            "category": self.category,
                            "source": "Coursera",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Coursera scrape failed: {e}")
        return results

    def fetch_opportunities(self):
        opportunities = []
        opportunities.extend(self._scrape_class_central())
        opportunities.extend(self._scrape_coursera())

        if not opportunities:
            self.logger.info("No live results, using fallback data.")
            opportunities = [
                {
                    "title": "Deep Learning Specialization",
                    "company": "deeplearning.ai",
                    "location": "Online",
                    "link": "https://www.coursera.org/specializations/deep-learning",
                    "description": "Master deep learning with TensorFlow, CNNs, RNNs, and transformers.",
                    "category": self.category,
                    "source": "Coursera"
                },
                {
                    "title": "Generative AI with LLMs",
                    "company": "DeepLearning.AI & AWS",
                    "location": "Online",
                    "link": "https://www.coursera.org/learn/generative-ai-with-llms",
                    "description": "Learn prompt engineering, fine-tuning, and RLHF for LLMs.",
                    "category": self.category,
                    "source": "Coursera"
                },
                {
                    "title": "CS229: Machine Learning",
                    "company": "Stanford University",
                    "location": "Online",
                    "link": "https://cs229.stanford.edu/",
                    "description": "Stanford's legendary ML course covering theory and practice.",
                    "category": self.category,
                    "source": "Stanford"
                },
            ]
        return opportunities
