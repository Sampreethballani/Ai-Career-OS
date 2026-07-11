import requests
from bs4 import BeautifulSoup
from src.agents.base_agent import BaseAgent

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}

class ScholarshipAgent(BaseAgent):
    def __init__(self):
        super().__init__("scholarship_agent")
        self.category = "scholarship"

    def _scrape_scholarships_com(self):
        results = []
        try:
            url = "https://www.scholarships.com/financial-aid/search/?q=computer+science+artificial+intelligence"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results
            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select(".scholarship-item, .result-item, .search-result")[:8]:
                try:
                    title_el = card.select_one(".scholarship-name, .title, h3")
                    provider_el = card.select_one(".provider, .sponsor, .organization")
                    link_el = card.select_one("a[href*='/scholarship/']")
                    amount_el = card.select_one(".amount, .award, .value")

                    title = title_el.get_text(strip=True) if title_el else None
                    provider = provider_el.get_text(strip=True) if provider_el else "Various"
                    link = link_el["href"] if link_el and link_el.get("href") else None
                    amount = amount_el.get_text(strip=True) if amount_el else "Varies"

                    if title and link:
                        if not link.startswith("http"):
                            link = "https://www.scholarships.com" + link
                        results.append({
                            "title": title,
                            "company": provider,
                            "location": "Global",
                            "link": link,
                            "description": f"Scholarship: {title} - Award: {amount}",
                            "category": self.category,
                            "source": "Scholarships.com",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Scholarships.com scrape failed: {e}")
        return results

    def _scrape_fastweb(self):
        results = []
        try:
            url = "https://www.fastweb.com/college-scholarships/scholarships/computer-science"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results
            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select(".scholarship, .result, .search-result-item")[:8]:
                try:
                    title_el = card.select_one(".title, h3, .scholarship-name")
                    provider_el = card.select_one(".provider, .sponsor, .awarder")
                    link_el = card.select_one("a[href*='/scholarships/']")

                    title = title_el.get_text(strip=True) if title_el else None
                    provider = provider_el.get_text(strip=True) if provider_el else "Various"
                    link = link_el["href"] if link_el and link_el.get("href") else None

                    if title and link:
                        if not link.startswith("http"):
                            link = "https://www.fastweb.com" + link
                        results.append({
                            "title": title,
                            "company": provider,
                            "location": "Global",
                            "link": link,
                            "description": f"Scholarship: {title}",
                            "category": self.category,
                            "source": "Fastweb",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Fastweb scrape failed: {e}")
        return results

    def fetch_opportunities(self):
        opportunities = []
        opportunities.extend(self._scrape_scholarships_com())
        opportunities.extend(self._scrape_fastweb())

        if not opportunities:
            self.logger.info("No live results, using fallback data.")
            opportunities = [
                {
                    "title": "Google AI Impact Scholarship",
                    "company": "Google",
                    "location": "Global",
                    "link": "https://ai.google/education/scholarships/",
                    "description": "Scholarship for underrepresented students pursuing AI/ML education.",
                    "category": self.category,
                    "source": "Google AI"
                },
                {
                    "title": "Knight-Hennessy Scholars Program",
                    "company": "Stanford University",
                    "location": "Stanford, CA",
                    "link": "https://knight-hennessy.stanford.edu/",
                    "description": "Full graduate scholarship for emerging leaders in tech.",
                    "category": self.category,
                    "source": "Stanford"
                },
                {
                    "title": "B.Tech CS Merit Scholarship",
                    "company": "Various Indian Institutes",
                    "location": "India",
                    "link": "https://scholarships.gov.in/",
                    "description": "Merit-based scholarship for B.Tech Computer Science students.",
                    "category": self.category,
                    "source": "National Scholarship Portal"
                },
            ]
        return opportunities
