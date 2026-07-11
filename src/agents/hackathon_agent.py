import requests
from bs4 import BeautifulSoup
from src.agents.base_agent import BaseAgent

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}

class HackathonAgent(BaseAgent):
    def __init__(self):
        super().__init__("hackathon_agent")
        self.category = "hackathon"

    def _scrape_devpost(self):
        results = []
        try:
            url = "https://devpost.com/hackathons?search=ai+machine+learning&status=open"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(".hackathon-card, .challenge-card, .link-to-software") or []
            for card in cards[:8]:
                try:
                    title_el = card.select_one(".title, .hackathon-title, h3")
                    link_el = card.select_one("a[href*='/project/'], a[href*='/challenge/']")
                    date_el = card.select_one(".date, .submission-period, .dates")

                    title = title_el.get_text(strip=True) if title_el else None
                    link = link_el["href"] if link_el and link_el.get("href") else None
                    dates = date_el.get_text(strip=True) if date_el else ""

                    if title and link:
                        results.append({
                            "title": title,
                            "company": "Devpost",
                            "location": "Online",
                            "link": link,
                            "description": f"Hackathon: {title} ({dates})",
                            "category": self.category,
                            "source": "Devpost",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Devpost scrape failed: {e}")
        return results

    def _scrape_mlh(self):
        results = []
        try:
            url = "https://mlh.io/seasons/2026/events"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results
            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select(".event, .row .event-card, .item")[:8]:
                try:
                    title_el = card.select_one(".event-name, h3, .title")
                    link_el = card.select_one("a[href*='mlh.io']")
                    date_el = card.select_one(".event-date, .date, .when")

                    title = title_el.get_text(strip=True) if title_el else None
                    link = link_el["href"] if link_el and link_el.get("href") else None
                    dates = date_el.get_text(strip=True) if date_el else ""

                    if title and link:
                        results.append({
                            "title": title,
                            "company": "MLH",
                            "location": "Various",
                            "link": link,
                            "description": f"MLH hackathon: {title} ({dates})",
                            "category": self.category,
                            "source": "MLH",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"MLH scrape failed: {e}")
        return results

    def fetch_opportunities(self):
        opportunities = []
        opportunities.extend(self._scrape_devpost())
        opportunities.extend(self._scrape_mlh())

        if not opportunities:
            self.logger.info("No live results, using fallback data.")
            opportunities = [
                {
                    "title": "AI for Social Good Hackathon",
                    "company": "GitHub & Microsoft",
                    "location": "Online",
                    "link": "https://github.com/ai-for-social-good-hackathon",
                    "description": "Build AI solutions for real-world social challenges.",
                    "category": self.category,
                    "source": "GitHub"
                },
                {
                    "title": "LLM Hackathon by LangChain",
                    "company": "LangChain",
                    "location": "Online",
                    "link": "https://blog.langchain.dev/langchain-hackathon/",
                    "description": "Build innovative applications using LangChain and LLMs.",
                    "category": self.category,
                    "source": "LangChain"
                },
                {
                    "title": "Google AI Hackathon",
                    "company": "Google",
                    "location": "Global",
                    "link": "https://ai.google/hackathons/",
                    "description": "Compete to build cutting-edge AI projects with Google tools.",
                    "category": self.category,
                    "source": "Google"
                },
            ]
        return opportunities
