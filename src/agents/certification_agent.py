import requests
from bs4 import BeautifulSoup
from src.agents.base_agent import BaseAgent

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}

class CertificationAgent(BaseAgent):
    def __init__(self):
        super().__init__("certification_agent")
        self.category = "certification"

    def _scrape_coursera_pro_certs(self):
        results = []
        try:
            url = "https://www.coursera.org/professional-certificates/artificial-intelligence-machine-learning"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return results
            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select(".cds-ProductCard, .card, .certificate-card")[:8]:
                try:
                    title_el = card.select_one(".cds-ProductCard-title, h3, .card-title")
                    provider_el = card.select_one(".cds-ProductCard-partner, .partner-name, .provider")
                    link_el = card.select_one("a[href*='/professional-certificates/']")

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
                            "description": f"Professional certificate: {title}",
                            "category": self.category,
                            "source": "Coursera",
                        })
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Coursera cert scrape failed: {e}")
        return results

    def _scrape_aws_certs(self):
        results = []
        try:
            url = "https://aws.amazon.com/certification/certified-machine-learning-specialty/"
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.select_one("h1") or soup.select_one(".title, .headline")
                if title:
                    results.append({
                        "title": title.get_text(strip=True),
                        "company": "Amazon Web Services",
                        "location": "Online",
                        "link": url,
                        "description": "AWS Machine Learning certification for ML engineers.",
                        "category": self.category,
                        "source": "AWS",
                    })
        except Exception as e:
            self.logger.error(f"AWS cert scrape failed: {e}")
        return results

    def fetch_opportunities(self):
        opportunities = []
        opportunities.extend(self._scrape_coursera_pro_certs())
        opportunities.extend(self._scrape_aws_certs())

        if not opportunities:
            self.logger.info("No live results, using fallback data.")
            opportunities = [
                {
                    "title": "TensorFlow Developer Certificate",
                    "company": "Google",
                    "location": "Online",
                    "link": "https://www.tensorflow.org/certificate/",
                    "description": "Validate your TensorFlow skills with this official Google certification.",
                    "category": self.category,
                    "source": "Google"
                },
                {
                    "title": "AWS Certified Machine Learning Specialty",
                    "company": "Amazon Web Services",
                    "location": "Online",
                    "link": "https://aws.amazon.com/certification/certified-machine-learning-specialty/",
                    "description": "Demonstrate expertise in building ML models on AWS.",
                    "category": self.category,
                    "source": "AWS"
                },
                {
                    "title": "Microsoft Certified: Azure AI Engineer Associate",
                    "company": "Microsoft",
                    "location": "Online",
                    "link": "https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-engineer/",
                    "description": "Design and implement AI solutions using Azure services.",
                    "category": self.category,
                    "source": "Microsoft"
                },
            ]
        return opportunities
