# Personal AI Career Operating System

This project aims to build a Personal AI Career Operating System that continuously monitors, collects, filters, summarizes, and notifies about career opportunities relevant to a B.Tech Computer Science student aspiring to become an AI/LLM Engineer.

## Features
- **Modular AI Agents**: Specialized agents for internships, jobs, courses, scholarships, certifications, hackathons, AI news, and GitHub repositories.
- **LLM-powered Filtering**: Utilizes Gemini Free Tier API to filter and rank opportunities based on personal preferences.
- **Notification System**: Delivers concise summaries via Telegram and Email, with options for instant alerts, daily, and weekly digests.
- **Production-Quality Code**: Follows clean software architecture, modular code organization, proper documentation, logging, configuration management, and version control.

## Tech Stack
- Python
- LangGraph
- Gemini Free Tier API
- SQLite
- BeautifulSoup
- Playwright (if needed)
- Feedparser
- Requests
- Python Telegram Bot
- GitHub Actions (for automation)
- Git
- GitHub
- VS Code

## Project Structure
```
.github/workflows/  # GitHub Actions workflows
config/             # Configuration files
database/           # Database schema and migration scripts
logs/               # Application logs
src/                # Main application source code
├── agents/         # Specialized AI agents
│   ├── __init__.py
│   ├── internship_agent.py
│   ├── job_agent.py
│   ├── course_agent.py
│   ├── scholarship_agent.py
│   ├── certification_agent.py
│   ├── hackathon_agent.py
│   ├── ai_news_agent.py
│   └── github_agent.py
├── core/           # Core functionalities (LLM summarizer, scheduler, notification service)
│   ├── __init__.py
│   ├── llm_summarizer.py
│   ├── scheduler.py
│   └── notification_service.py
├── utils/          # Utility functions
│   ├── __init__.py
│   └── data_parser.py
├── main.py         # Main application entry point
└── config_manager.py # Configuration manager
.env                # Environment variables
README.md           # Project README
requirements.txt    # Python dependencies
```

## Setup and Installation
(To be added)

## Usage
(To be added)

## Contributing
(To be added)

## License
(To be added)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your_username/ai_career_agent.git
    cd ai_career_agent
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure environment variables:**
    Copy the `.env.example` file to `.env` and fill in your API keys and credentials.
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file:
    -   `GEMINI_API_KEY`: Obtain from Google AI Studio.
    -   `TELEGRAM_BOT_TOKEN`: Create a new bot with BotFather on Telegram and get the token.
    -   `TELEGRAM_CHAT_ID`: Get your chat ID by messaging your bot and then visiting `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`.
    -   `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER`: Use your Gmail address and an App Password (generated from Google Account Security settings) for `EMAIL_PASSWORD`.

## Usage

To run the AI Career Operating System, execute the `main.py` script:

```bash
source venv/bin/activate
python src/main.py
```

The application will start monitoring opportunities based on the configured `CHECK_INTERVAL_MINUTES` in your `.env` file. Notifications will be sent to Telegram and/or Email for relevant opportunities.

## Extending Functionality

-   **Add new agents**: Create new classes inheriting from `BaseAgent` in `src/agents/` to monitor additional sources.
-   **Customize LLM prompts**: Modify `src/core/llm_summarizer.py` to refine how opportunities are analyzed.
-   **Adjust notification logic**: Update `src/core/notification_service.py` for different notification preferences.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add new feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
