import feedparser
from src.agents.base_agent import BaseAgent

class AINewsAgent(BaseAgent):
    def __init__(self):
        super().__init__("ai_news_agent")
        self.category = "ai_news"
        self.feeds = [
            "https://openai.com/news/rss.xml",
            "https://machinelearning.apple.com/rss.xml",
            "https://blog.google/technology/ai/rss/"
        ]

    def fetch_opportunities(self):
        opportunities = []
        for url in self.feeds:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]: # Limit to latest 5
                    opportunities.append({
                        "title": entry.title,
                        "company": entry.get("author", "Unknown"),
                        "location": "Online",
                        "link": entry.link,
                        "description": entry.summary if 'summary' in entry else entry.title,
                        "category": self.category,
                        "source": url
                    })
            except Exception as e:
                self.logger.error(f"Error parsing feed {url}: {e}")
        return opportunities
