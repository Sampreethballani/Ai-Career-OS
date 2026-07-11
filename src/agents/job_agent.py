import requests
from bs4 import BeautifulSoup
from src.agents.base_agent import BaseAgent

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("job_agent")
        self.category = "job"

    def _scrape_linkedin(self):
        results = []
        try:
            url = "https://www.linkedin.com/jobs/search/?keywords=AI%20Machine%20Learning%20Engineer&geoId=&f_TPR=r604800"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results

            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(".base-card") or soup.select(".job-search-card") or []

            for card in cards[:10]:
                try:
                    title_el = card.select_one(".base-search-card__title, .job-card-list__title")
                    company_el = card.select_one(".base-search-card__subtitle, .job-card-container__company-name")
                    link_el = card.select_one("a[href*='/jobs/view']")
                    loc_el = card.select_one(".job-search-card__location, .base-search-card__metadata")

                    title = title_el.get_text(strip=True) if title_el else None
                    company = company_el.get_text(strip=True) if company_el else None
                    link = link_el["href"] if link_el and link_el.get("href") else None
                    location = loc_el.get_text(strip=True) if loc_el else "Remote"

                    if title and link:
                        results.append({
                            "title": title,
                            "company": company or "Unknown",
                            "location": location,
                            "link": link,
                            "description": f"AI/ML Engineer role at {company or 'tech company'}",
                            "category": self.category,
                            "source": "LinkedIn",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"LinkedIn jobs scrape failed: {e}")
        return results

    def _scrape_indeed(self):
        results = []
        try:
            url = "https://in.indeed.com/jobs?q=AI+Machine+Learning+Engineer&l=&from=search"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results

            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(".job_seen_beacon, .jobCard, .result") or []

            for card in cards[:10]:
                try:
                    title_el = card.select_one(".jobTitle, .title, h2")
                    company_el = card.select_one(".companyName, .company, .company_info")
                    link_el = card.select_one("a[href*='/viewjob']")
                    loc_el = card.select_one(".companyLocation, .location, .jobLoc")

                    title = title_el.get_text(strip=True) if title_el else None
                    company = company_el.get_text(strip=True) if company_el else None
                    link = link_el["href"] if link_el and link_el.get("href") else None
                    location = loc_el.get_text(strip=True) if loc_el else "Remote"

                    if title and link:
                        if not link.startswith("http"):
                            link = "https://in.indeed.com" + link
                        results.append({
                            "title": title,
                            "company": company or "Unknown",
                            "location": location,
                            "link": link,
                            "description": f"Job: {title}",
                            "category": self.category,
                            "source": "Indeed",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Indeed jobs scrape failed: {e}")
        return results

    def _scrape_github(self):
        results = []
        try:
            url = "https://api.github.com/search/issues?q=label:hiring+label:ai+state:open&sort=created&order=desc&per_page=10"
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                for item in response.json().get("items", [])[:10]:
                    results.append({
                        "title": item["title"],
                        "company": item["user"]["login"],
                        "location": "Remote",
                        "link": item["html_url"],
                        "description": (item.get("body") or "")[:300],
                        "category": self.category,
                        "source": "GitHub",
                    })
        except Exception as e:
            self.logger.error(f"GitHub jobs scrape failed: {e}")
        return results

    def _scrape_google_careers(self):
        results = []
        try:
            url = "https://www.google.com/about/careers/applications/jobs/results/?category=DATA_CENTER_OPERATIONS,DEVELOPER_ENGINEERING,SOFTWARE_ENGINEERING&q=AI+Machine+Learning"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results

            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select(".job-card, .gc-card, article")[:5]:
                try:
                    title_el = card.select_one("h3, .job-title, .gc-title")
                    link_el = card.select_one("a[href*='/careers']")
                    loc_el = card.select_one(".location, .gc-location")

                    title = title_el.get_text(strip=True) if title_el else None
                    link = link_el["href"] if link_el and link_el.get("href") else None
                    location = loc_el.get_text(strip=True) if loc_el else "Mountain View, CA"

                    if title and link:
                        if not link.startswith("http"):
                            link = "https://www.google.com" + link
                        results.append({
                            "title": title,
                            "company": "Google",
                            "location": location,
                            "link": link,
                            "description": f"Google career: {title}",
                            "category": self.category,
                            "source": "Google Careers",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Google Careers scrape failed: {e}")
        return results

    def fetch_opportunities(self):
        opportunities = []

        opportunities.extend(self._scrape_linkedin())
        opportunities.extend(self._scrape_indeed())
        opportunities.extend(self._scrape_github())
        opportunities.extend(self._scrape_google_careers())

        if not opportunities:
            self.logger.info("No live results, using fallback data.")
            opportunities = [
                {
                    "title": "AI/ML Engineer",
                    "company": "Microsoft",
                    "location": "Redmond, WA",
                    "link": "https://careers.microsoft.com/ai-engineer",
                    "description": "Design and deploy large-scale AI systems with LLMs.",
                    "category": self.category,
                    "source": "Microsoft Careers"
                },
                {
                    "title": "LLM Research Scientist",
                    "company": "Anthropic",
                    "location": "San Francisco, CA",
                    "link": "https://anthropic.com/careers/research-scientist",
                    "description": "Research and develop safe frontier AI models.",
                    "category": self.category,
                    "source": "Anthropic Careers"
                },
                {
                    "title": "Machine Learning Engineer",
                    "company": "Amazon",
                    "location": "Seattle, WA",
                    "link": "https://amazon.jobs/ml-engineer",
                    "description": "Build ML systems for Alexa and AI services.",
                    "category": self.category,
                    "source": "Amazon Jobs"
                },
            ]

        return opportunities
