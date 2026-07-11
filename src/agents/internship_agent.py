import requests
import re
from bs4 import BeautifulSoup
from src.agents.base_agent import BaseAgent

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

class InternshipAgent(BaseAgent):
    def __init__(self):
        super().__init__("internship_agent")
        self.category = "internship"

    def _scrape_internshala(self):
        results = []
        try:
            url = "https://internshala.com/internships/keywords-ai-ml-artificial-intelligence-machine-learning/"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results

            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(".internship_meta") or soup.select(".individual_internship") or []

            for card in cards[:10]:
                try:
                    title_el = card.select_one(".job-title-href, .profile, .heading_4_5")
                    company_el = card.select_one(".company-name, .company_name, .link_display_like_text")
                    link_el = card.select_one("a[href*='/internship/']")
                    loc_el = card.select_one(".location, .locations, .row_1c_icon")
                    desc_el = card.select_one(".text-container, .job_detail, .point")

                    title = title_el.get_text(strip=True) if title_el else None
                    company = company_el.get_text(strip=True) if company_el else None
                    link = link_el["href"] if link_el and link_el.get("href") else None
                    location = loc_el.get_text(strip=True) if loc_el else "Remote"
                    description = desc_el.get_text(strip=True)[:300] if desc_el else ""

                    if title and link:
                        if not link.startswith("http"):
                            link = "https://internshala.com" + link
                        results.append({
                            "title": title,
                            "company": company or "Unknown",
                            "location": location,
                            "link": link,
                            "description": description,
                            "category": self.category,
                            "source": "Internshala",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Internshala scrape failed: {e}")
        return results

    def _scrape_linkedin(self):
        results = []
        try:
            url = "https://www.linkedin.com/jobs/search/?keywords=AI%20ML%20internship&geoId=&f_TPR=r604800"
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
                    location_el = card.select_one(".job-search-card__location, .base-search-card__metadata")

                    title = title_el.get_text(strip=True) if title_el else None
                    company = company_el.get_text(strip=True) if company_el else None
                    link = link_el["href"] if link_el and link_el.get("href") else None
                    location = location_el.get_text(strip=True) if location_el else "Remote"

                    if title and link:
                        results.append({
                            "title": title,
                            "company": company or "Unknown",
                            "location": location,
                            "link": link,
                            "description": f"AI/ML Internship at {company or 'tech company'}",
                            "category": self.category,
                            "source": "LinkedIn",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"LinkedIn scrape failed: {e}")
        return results

    def _scrape_github(self):
        results = []
        try:
            url = "https://api.github.com/search/issues?q=label:internship+label:ai+state:open&sort=created&order=desc&per_page=10"
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                for item in response.json().get("items", []):
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
            self.logger.error(f"GitHub scrape failed: {e}")
        return results

    def _scrape_indeed(self):
        results = []
        try:
            url = "https://in.indeed.com/jobs?q=AI+ML+internship&l=&from=search"
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
                    location_el = card.select_one(".companyLocation, .location, .jobLoc")

                    title = title_el.get_text(strip=True) if title_el else None
                    company = company_el.get_text(strip=True) if company_el else None
                    link = link_el["href"] if link_el and link_el.get("href") else None
                    location = location_el.get_text(strip=True) if location_el else "Remote"

                    if title and link:
                        if not link.startswith("http"):
                            link = "https://in.indeed.com" + link
                        results.append({
                            "title": title,
                            "company": company or "Unknown",
                            "location": location,
                            "link": link,
                            "description": f"Internship: {title}",
                            "category": self.category,
                            "source": "Indeed",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Indeed scrape failed: {e}")
        return results

    def fetch_opportunities(self):
        opportunities = []

        opportunities.extend(self._scrape_internshala())
        opportunities.extend(self._scrape_linkedin())
        opportunities.extend(self._scrape_github())
        opportunities.extend(self._scrape_indeed())

        if not opportunities:
            self.logger.info("No live results, using fallback data.")
            opportunities = [
                {
                    "title": "AI Engineer Intern",
                    "company": "NVIDIA",
                    "location": "Remote",
                    "link": "https://nvidia.com/careers/intern-ai",
                    "description": "Work on LLM optimization and deployment.",
                    "category": self.category,
                    "source": "NVIDIA Careers"
                },
                {
                    "title": "Software Engineering Intern",
                    "company": "Google",
                    "location": "Mountain View, CA",
                    "link": "https://google.com/careers/intern-swe",
                    "description": "General software engineering internship.",
                    "category": self.category,
                    "source": "Google Careers"
                },
            ]

        return opportunities
