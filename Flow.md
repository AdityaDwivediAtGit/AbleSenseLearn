# System Architecture & Flow: Able Sense AI Buddy

## 1. High-Level Architecture

**Able Sense AI Buddy** is a modular, Streamlit-based web application designed for accessibility. It follows a service-oriented architecture where the frontend (Streamlit) interacts with specialized backend AI services (Vision, Voice, Text) via a unified configuration layer.

```mermaid
graph TD
    User((User)) <--> Frontend[Streamlit App (app.py)]
    
    subgraph "Frontend Layer"
        Frontend --> Sidebar[Sidebar Config & Nav]
        Frontend --> Pages[Dashboard, Vision, Voice, Learning, Settings]
    end

    subgraph "Service Layer"
        Frontend --> VisionService[VisionProcessor]
        Frontend --> VoiceService[VoiceAssistant]
        Frontend --> TextService[TextProcessor]
    end

    subgraph "AI Providers"
        VisionService --> YOLO[YOLOv8 Local Model]
        TextService --> OpenAI[OpenAI API]
        TextService --> DeepSeek[DeepSeek API]
        TextService --> HuggingFace[HuggingFace Local Pipeline]
        VoiceService --> gTTS[Google TTS (Cloud)]
        VoiceService --> PyTTSx3[pyttsx3 (Offline Fallback)]
    end

    subgraph "Data Layer"
        Frontend --> DB[(SQLite Database)]
        DB --> UserProfile[User Table]
        DB --> InteractionLog[Interaction Logs]
    end
```

---

## 2. Core Components & Technologies

### A. Frontend (`app.py`)
-   **Framework**: Streamlit. Chosen for rapid Python-only UI development and accessibility support via native widgets.
-   **State Management**: Uses `st.session_state` to persist user context (messages, selected page) across re-runs.
-   **Config**: `config.py` handles environment variables, API keys, and Feature Flags (`ENABLE_TEST_DATA`).

### B. AI Services
1.  **Vision Processor** (`ai_services/vision_processor.py`)
    -   **Engine**: `ultralytics` (YOLOv8).
    -   **Function**: Detects objects in images.
    -   **Flow**: User inputs image (Camera/Upload) -> Preprocessing -> YOLO Inference -> Object List -> Natural Language Description Generation.
    -   **Test Mode**: Returns randomized mock descriptions ("I see a red car...") to save compute/latency.

2.  **Voice Assistant** (`ai_services/voice_assistant.py`)
    -   **Input (STT)**: `SpeechRecognition` library (via Google Web Speech API).
    -   **Output (TTS)**:
        -   *Primary*: `gTTS` (Google Text-to-Speech). Generates MP3s -> Played via `st.audio`. Best for quality and cloud compatibility.
        -   *Secondary*: `pyttsx3`. Offline driver. Used as fallback if gTTS fails.
    -   **Flow**: User clicks "Speak" -> Audio Captured -> STT -> Text Command -> Processing -> TTS Generation -> Audio Playback.

3.  **Text Processor** (`ai_services/text_processor.py`)
    -   **Engine**: Dynamic switching between **DeepSeek** (Default), **OpenAI**, and **HuggingFace**.
    -   **Fallback**: If no API key is present, automatically falls back to local HuggingFace transformers (`flan-t5` for simplification, `distilbart` for summary).
    -   **Flow**: Input Text -> Provider Selection -> API Call (with specific Base URL) -> Result -> UI Display.

### C. Database (`models/`)
-   **ORM**: SQLAlchemy.
-   **Schema**:
    -   `User`: Stores profile, disability type, severity, and UI preferences (font size).
    -   `InteractionLog`: (Planned) For history tracking.
-   **Startup**: `Config.init_app()` ensures the DB file and tables exist on every launch, preventing "Table not found" errors.

---

## 3. User Scenarios & tailored Handling

We specifically cater to four main disability categories via the **Settings Profile**:

### 👁️ Blind / Low Vision
-   **Challenge**: Cannot see UI or surroundings.
-   **Solution**:
    -   **Voice-First**: "Voice Companion" page allows full interaction via speech.
    -   **Vision Assistant**: One-click "Describe" button uses Computer Vision to narrate the environment.
    -   **TTS Integration**: All AI outputs (Vision descriptions, Text summaries) have a "Read Aloud" button using `st.audio`.

### 👂 Deaf / Hard of Hearing
-   **Challenge**: Cannot hear audio alerts or voice assistants.
-   **Solution**:
    -   **Visual Feedback**: All Voice Assistant responses are printed as text in the Chat interface.
    -   **Toasts**: "Toast" notifications (popups) used for status updates instead of just beeps.

### 🧠 Cognitive Disabilities
-   **Challenge**: Complex text or interfaces can be overwhelming.
-   **Solution**:
    -   **Text Simplifier**: "Explain like I'm 5" mode in `TextProcessor` breaks down complex inputs using LLMs.
    -   **Simple UI**: Interface designed with large buttons and clear headers.

### ✋ Motor Disabilities
-   **Challenge**: Difficulty using mouse/keyboard.
-   **Solution**:
    -   **Tab Navigation**: Streamlit supports native tab-nav.
    -   **Voice Command**: The Voice Companion can theoretically drive the app (future scope: navigation via voice).

---

## 4. Application Flow Walkthrough

### 🚀 Startup
1.  **Init**: `app.py` loads. `Config.init_app()` creates `data/` dirs. `Base.metadata.create_all()` creates SQLite tables.
2.  **User Check**: Checks DB for users. Auto-creates `demo_user` if none exist.
3.  **Service Init**: `@st.cache_resource` initializes heavy AI models (YOLO, Transformers) only once to speed up re-runs.

### ⚙️ Configuration Flow
1.  **Sidebar**: User selects "AI Provider" (e.g., DeepSeek).
2.  **Key Input**: User pastes API Key in sidebar.
3.  **State Update**: `Config` object is updated in-memory.
4.  **Test Mode**: If `Enable Test Data` is checked, Services bypass API calls and return strings like `[TEST DATA] ...`.

### 🖼️ Vision Flow
1.  **Input**: User takes photo via `st.camera_input`.
2.  **Processing**: Image bytes sent to `VisionProcessor.describe_image()`.
3.  **Inference**: YOLO detects objects (e.g., `{'cup': 1, 'laptop': 1}`).
4.  **Formatting**: Converts counts to sentence: "I see 1 cup and 1 laptop."
5.  **Output**: Display text + "Read Aloud" button generates Audio which plays immediately.

### 🗣️ Voice/Chat Flow
1.  **Input**: User clicks "Click to Speak".
2.  **Listening**: `sr.Microphone` opens. browser records audio.
3.  **STT**: Google Speech API converts to text.
4.  **Logic**:
    -   If "time" in text -> Return Time.
    -   Else -> Return simple conversational echo (Phase 1 logic).
5.  **Output**: Response text added to Chat History (`st.session_state.messages`) and spoken via TTS.

---

## 5. Technical Edge Case Handling

| Edge Case | Handling Strategy |
| :--- | :--- |
| **No Internet** | App works locally. `HuggingFace` local pipelines used for text. `pyttsx3` used for voice (if drivers exist). |
| **Missing API Key** | `TextProcessor` detects missing key and automatically falls back to local HuggingFace models. |
| **Cloud Audio Drivers** | Streamlit Cloud lacks audio hardware. `pyttsx3` would crash. We wrapped it in `try/except` and use `gTTS` to file + `st.audio` for browser-based playback. |
| **Missing DB File** | Startup script auto-generates `ablesense.db` and tables. |
| **Slow Model Load** | `transformers` pipelines are lazy-loaded (only on first use) or cached via `st.cache_resource` to prevent UI freezing. |
