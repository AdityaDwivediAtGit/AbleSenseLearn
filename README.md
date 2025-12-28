# Able Sense AI Buddy

**Able Sense AI Buddy** is a comprehensive AI assistant designed to help people with disabilities in their daily lives.

## Features

- **👁️ Vision Assistant**: Describes surroundings and objects using phone camera or file upload.
- **🗣️ Voice Companion**: Hands-free voice interaction for commands and chat.
- **📚 Learning & Simplification**: Simplifies complex text and summarizes long articles.
- **⚙️ Adaptive Profile**: Customizes the usage experience based on Visual, Hearing, Motor, or Cognitive needs.
- **🆘 Emergency Mode**: Quick access to alert contacts.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/ablesense.git
    cd AbleSenseLearn
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment:**
    - Copy `.env.example` to `.env`
    - Add your `OPENAI_API_KEY`

4.  **Initialize Database:**
    ```bash
    python setup_database.py
    ```

5.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

## Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-3.5 (Text), YOLOv8 (Vision), SpeechRecognition & pyttsx3 (Voice)
- **Database**: SQLite (via SQLAlchemy)

## Architecture & Flow
For a detailed understanding of how the system works, including data flow diagrams and component breakdowns, please refer to the **[System Architecture & Flow](Flow.md)** documentation.

## Accessibility
Designed with WCAG principles, supporting screen readers and keyboard navigation.
