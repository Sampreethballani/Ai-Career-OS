import requests
from src.agents.base_agent import BaseAgent

class GitHubAgent(BaseAgent):
    def __init__(self):
        super().__init__("github_agent")
        self.category = "github_repo"

    def fetch_opportunities(self):
        # Fetch trending AI repositories via GitHub API
        url = "https://api.github.com/search/repositories?q=topic:llm+topic:ai&sort=stars&order=desc"
        opportunities = []
        try:
            response = requests.get(url)
            if response.status_code == 200:
                repos = response.json().get('items', [])[:5]
                for repo in repos:
                    opportunities.append({
                        "title": repo['name'],
                        "company": repo['owner']['login'],
                        "location": "GitHub",
                        "link": repo['html_url'],
                        "description": repo['description'],
                        "category": self.category,
                        "source": "GitHub API"
                    })
        except Exception as e:
            self.logger.error(f"Error fetching GitHub repos: {e}")
        return opportunities
