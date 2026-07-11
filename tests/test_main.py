import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.utils.db import Base, Opportunity
from src.main import CareerAgentApp

@pytest.fixture
def app():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with patch("src.main.init_db", return_value=sessionmaker(bind=engine)):
        app = CareerAgentApp()
        app.agents = []
        yield app, engine

def test_new_opportunity_flow(app):
    app_obj, engine = app
    mock_agent = MagicMock()
    mock_agent.run.return_value = [
        {"title": "AI Intern", "company": "TestCo", "location": "Remote", "link": "http://test.com/ai", "description": "AI role", "source": "TestSource", "category": "internship"}
    ]
    app_obj.agents = [mock_agent]

    with (
        patch("src.core.llm_summarizer.llm_summarizer.analyze_opportunity", return_value=(85, "Great fit for AI engineer.")),
        patch("src.core.notification_service.notification_service.notify") as mock_notify
    ):
        app_obj.process_opportunities()

    TestSession = sessionmaker(bind=engine)
    with TestSession() as session:
        opp = session.query(Opportunity).filter_by(link="http://test.com/ai").first()
        assert opp is not None
        assert opp.title == "AI Intern"
        assert opp.relevance_score == 85
        assert opp.is_notified == True

    mock_notify.assert_called_once()

def test_existing_opportunity_skipped(app):
    app_obj, engine = app
    TestSession = sessionmaker(bind=engine)
    with TestSession() as session:
        session.add(Opportunity(source="TestSource", category="internship", title="AI Intern", company="TestCo", location="Remote", link="http://test.com/ai", description="AI role", relevance_score=90, summary="Existing.", is_notified=True))
        session.commit()

    mock_agent = MagicMock()
    mock_agent.run.return_value = [
        {"title": "AI Intern", "company": "TestCo", "location": "Remote", "link": "http://test.com/ai", "description": "AI role", "source": "TestSource", "category": "internship"}
    ]
    app_obj.agents = [mock_agent]

    with (
        patch("src.core.llm_summarizer.llm_summarizer.analyze_opportunity", return_value=(85, "Great fit.")),
        patch("src.core.notification_service.notification_service.notify") as mock_notify
    ):
        app_obj.process_opportunities()

    with TestSession() as session:
        assert session.query(Opportunity).filter_by(link="http://test.com/ai").count() == 1

    mock_notify.assert_not_called()

def test_low_score_no_notification(app):
    app_obj, engine = app
    mock_agent = MagicMock()
    mock_agent.run.return_value = [
        {"title": "General Intern", "company": "OtherCo", "location": "Onsite", "link": "http://test.com/general", "description": "General role", "source": "OtherSource", "category": "internship"}
    ]
    app_obj.agents = [mock_agent]

    with (
        patch("src.core.llm_summarizer.llm_summarizer.analyze_opportunity", return_value=(40, "Not relevant.")),
        patch("src.core.notification_service.notification_service.notify") as mock_notify
    ):
        app_obj.process_opportunities()

    TestSession = sessionmaker(bind=engine)
    with TestSession() as session:
        opp = session.query(Opportunity).filter_by(link="http://test.com/general").first()
        assert opp is not None
        assert opp.relevance_score == 40
        assert opp.is_notified == False

    mock_notify.assert_not_called()
