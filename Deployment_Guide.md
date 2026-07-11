# AI Career Operating System: Deployment Guide

This guide provides step-by-step instructions to set up and run your Personal AI Career Operating System locally, and how to manage its codebase using GitHub, including continuous integration with GitHub Actions.

## 1. Local Setup and Execution

### 1.1. Prerequisites
Before you begin, ensure your system meets the following requirements:

*   **Python 3.10 or higher**: Download and install from [python.org](https://www.python.org/downloads/).
*   **Git**: Install Git from [git-scm.com](https://git-scm.com/downloads).
*   **API Keys and Credentials**:
    *   **Gemini API Key**: Obtain a free API key from [Google AI Studio](https://aistudio.google.com/).
    *   **Telegram Bot Token**: Create a new bot by chatting with [@BotFather](https://t.me/botfather) on Telegram. It will provide you with a token.
    *   **Telegram Chat ID**: After creating your bot, send a message to it. Then, visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` (replace `<YOUR_BOT_TOKEN>` with your actual bot token) in your web browser to find your `chat_id`.
    *   **Email Credentials**: If you wish to receive email notifications, you'll need your Gmail address (`EMAIL_SENDER`, `EMAIL_RECEIVER`) and an [App Password](https://support.google.com/accounts/answer/185833) for `EMAIL_PASSWORD` [1]. Regular Gmail passwords will not work for programmatic access.

### 1.2. Installation Steps

1.  **Download and Extract the Project**:
    *   Download the `ai_career_agent.zip` file provided.
    *   Extract its contents to a directory of your choice (e.g., `~/ai_career_agent`).

2.  **Navigate to the Project Directory**:
    Open your terminal or command prompt and change to the extracted project directory:
    ```bash
    cd /path/to/your/ai_career_agent
    ```

3.  **Create a Python Virtual Environment** (Recommended):
    A virtual environment isolates your project's dependencies from other Python projects.
    ```bash
    python3 -m venv venv
    ```

4.  **Activate the Virtual Environment**:
    *   **On macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows**:
        ```bash
        .\venv\Scripts\activate
        ```

5.  **Install Dependencies**:
    Install all required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

6.  **Configure Environment Variables**:
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Open the newly created `.env` file in a text editor and fill in your API keys and credentials obtained in the prerequisites step:
        ```ini
        # LLM Configuration
        GEMINI_API_KEY=your_gemini_api_key_here

        # Telegram Configuration
        TELEGRAM_BOT_TOKEN=your_bot_token_here
        TELEGRAM_CHAT_ID=your_chat_id_here

        # Email Configuration
        EMAIL_SENDER=your_email@gmail.com
        EMAIL_PASSWORD=your_app_password
        EMAIL_RECEIVER=your_email@gmail.com

        # App Configuration
        CHECK_INTERVAL_MINUTES=60
        LOG_LEVEL=INFO
        DATABASE_URL=sqlite:///database/career_agent.db
        ```
    *   **Important**: The `.env` file is ignored by Git (due to `.gitignore`) to prevent accidental exposure of your sensitive information.

### 1.3. Running the Application

With the virtual environment activated and `.env` configured, you can run the AI Career Operating System:

```bash
python src/main.py
```

The application will start, perform an initial scan for opportunities, and then continue to run in the background, checking for new opportunities at the interval specified in `CHECK_INTERVAL_MINUTES` in your `.env` file. Notifications for relevant opportunities will be sent via Telegram and/or Email.

To stop the application, press `Ctrl+C` in the terminal where it's running.

## 2. GitHub Repository Management

To maintain your project, track changes, and potentially collaborate, it's highly recommended to use a Git repository hosted on GitHub.

### 2.1. Create a New GitHub Repository

1.  Go to [GitHub](https://github.com/) and log in to your account.
2.  Click the `+` sign in the top right corner and select `New repository`.
3.  Give your repository a name (e.g., `ai-career-agent`).
4.  Choose `Private` to keep your code private (recommended for personal projects with API keys).
5.  **Do NOT** initialize the repository with a README, `.gitignore`, or license, as these are already included in your project files.
6.  Click `Create repository`.

### 2.2. Push Your Local Project to GitHub

1.  **Initialize Git in Your Local Project**:
    If you haven't already, navigate to your project directory in the terminal and initialize Git:
    ```bash
    cd /path/to/your/ai_career_agent
    git init
    ```

2.  **Add `.gitignore`**: The `.gitignore` file is already included in your project. It ensures that sensitive files like `.env` and generated logs/database files are not committed to your public repository.

3.  **Add Your Files to Git**:
    ```bash
    git add .
    ```

4.  **Commit Your Changes**:
    ```bash
    git commit -m "Initial commit of AI Career Operating System"
    ```

5.  **Link to Your GitHub Repository**:
    Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub username and the name of the repository you created.
    ```bash
    git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
    git branch -M main
    ```

6.  **Push to GitHub**:
    ```bash
    git push -u origin main
    ```
    You may be prompted to enter your GitHub username and Personal Access Token (PAT). If you don't have a PAT, you'll need to create one in your GitHub settings.

### 2.3. GitHub Actions for Continuous Integration

Your project includes a basic GitHub Actions workflow (`.github/workflows/ci.yml`) that will automatically run tests whenever you push changes to the `main` branch or open a pull request. This helps ensure your code remains functional.

To enable this:

1.  **Ensure `ci.yml` is pushed**: The `ci.yml` file should have been included in your initial push to GitHub.
2.  **Monitor Actions**: Go to your GitHub repository, click on the `Actions` tab, and you will see the workflow runs. Any push to `main` or pull request will trigger this workflow.

### 2.4. Managing Secrets in GitHub Actions (Optional for Advanced Use)

If you ever decide to run parts of your agent directly on GitHub Actions (e.g., for automated daily checks without your laptop running), you would need to store your API keys as GitHub Secrets. **For this project, running locally is the primary method, so this step is optional.**

1.  Go to your GitHub repository.
2.  Click on `Settings` > `Secrets and variables` > `Actions`.
3.  Click `New repository secret`.
4.  Add secrets for `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `EMAIL_SENDER`, `EMAIL_PASSWORD`, and `EMAIL_RECEIVER` with their respective values.

---

## References

[1] Google Account Help. "Sign in with App Passwords." [https://support.google.com/accounts/answer/185833](https://support.google.com/accounts/answer/185833)
