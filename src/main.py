import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config_manager import config_manager
from src.utils.db import init_db, Opportunity
from src.utils.logger import setup_logger
from src.core.llm_summarizer import llm_summarizer
from src.core.notification_service import notification_service

from src.agents.internship_agent import InternshipAgent
from src.agents.job_agent import JobAgent
from src.agents.course_agent import CourseAgent
from src.agents.scholarship_agent import ScholarshipAgent
from src.agents.certification_agent import CertificationAgent
from src.agents.hackathon_agent import HackathonAgent
from src.agents.ai_news_agent import AINewsAgent
from src.agents.github_agent import GitHubAgent

logger = setup_logger('main', 'logs/main.log')

REQUIRED_KEYS = ['title', 'link', 'source', 'category', 'company']

def validate_item(item):
    for key in REQUIRED_KEYS:
        if key not in item or not item[key]:
            logger.warning(f"Skipping item missing '{key}': {item.get('title', 'unknown')}")
            return False
    return True

class CareerAgentApp:
    def __init__(self):
        self.Session = init_db(config_manager.get("DATABASE_URL"))
        self.agents = [
            InternshipAgent(),
            JobAgent(),
            CourseAgent(),
            ScholarshipAgent(),
            CertificationAgent(),
            HackathonAgent(),
            AINewsAgent(),
            GitHubAgent(),
        ]

    def process_opportunities(self):
        logger.info("Starting opportunity processing cycle...")
        session = self.Session()

        for agent in self.agents:
            new_items = agent.run()
            for item in new_items:
                if not validate_item(item):
                    continue
                try:
                    exists = session.query(Opportunity).filter_by(link=item['link']).first()
                    if not exists:
                        logger.info(f"New opportunity: {item['title']} from {item['source']}")

                        score, summary = llm_summarizer.analyze_opportunity(item)

                        opportunity = Opportunity(
                            source=item['source'],
                            category=item['category'],
                            title=item['title'],
                            company=item['company'],
                            location=item.get('location', 'N/A') or 'N/A',
                            link=item['link'],
                            description=item.get('description', '') or '',
                            relevance_score=score,
                            summary=summary
                        )

                        session.add(opportunity)
                        session.commit()

                        if score >= 70:
                            notification_service.notify(opportunity)
                            opportunity.is_notified = True
                            session.commit()
                        else:
                            logger.info(f"Skipping notification for low score: {score}")
                except Exception as e:
                    logger.error(f"Error processing item '{item.get('title', 'unknown')}': {e}")
                    session.rollback()

        session.close()
        logger.info("Processing cycle complete.")

    def run(self):
        logger.info("AI Career Operating System started.")
        self.process_opportunities()
        logger.info("Run complete. Exiting.")

if __name__ == "__main__":
    app = CareerAgentApp()
    app.run()
