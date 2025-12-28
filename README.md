# **AbleSense Learn – Inclusive Education Platform**

## **Project Overview**

AbleSense Learn is an AI-powered adaptive learning platform designed to adjust educational content to the unique needs of students with disabilities. The platform uses machine learning to simplify text, generate multimodal content, and personalize learning pathways.

---

## **Features**

* **Dynamic Text Adaptation** – AI-powered simplification & summarization
* **Multimodal Content** – Alt-text generation, audio descriptions, tactile diagrams
* **Personalized Learning** – Adaptive pathways based on learning profiles
* **Accessibility-First Design** – WCAG 2.2 AA–compliant interface with multiple accessibility themes
* **Engagement Monitoring** – AI-based frustration detection and learning pattern analysis

---

## **Tech Stack**

* **Backend:** Python Flask
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **AI/ML:** Transformers, OpenCV, NLTK
* **Database:** SQLite (dev) / PostgreSQL (prod)
* **APIs:** Hugging Face, Google TTS (optional)

---

## **Quick Start**

### **Prerequisites**

* Python **3.8+**
* `pip` package manager

---

## **Installation**

### 1. **Clone the repository**

```bash
git clone https://github.com/yourusername/able-sense-learn.git
cd able-sense-learn
```

### 2. **Create a virtual environment**

```bash
python -m venv venv
```

Activate it:

**macOS/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. **Install dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Set up environment variables**

```bash
cp .env.example .env
```

Edit `.env` with your configuration.

### 5. **Initialize the database**

```bash
python setup_database.py
```

### 6. **Run the application**

```bash
python app.py
```

Open your browser and go to:

👉 [http://localhost:5000](http://localhost:5000)

---

## **Project Structure**

```
app.py                 # Main Flask application
ai_services/           # AI and ML services
api/                   # API endpoints
static/                # CSS, JS, images
templates/             # HTML templates
models/                # Database models
utils/                 # Utility functions
```

---

## **Configuration**

Create a `.env` file with:

```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///ablelearn.db
HUGGINGFACE_TOKEN=your-huggingface-token
GOOGLE_API_KEY=your-google-api-key
```

---

## **Testing**

### Run the full test suite:

```bash
python -m pytest tests/
```

### Run accessibility tests only:

```bash
python -m pytest tests/test_accessibility.py
```

---

## **API Documentation**

See **docs/api_documentation.md** for detailed API reference.

---

## **Accessibility Features**

* Keyboard navigation
* Screen reader compatibility
* Multiple color themes
* Adjustable text size and spacing
* Voice command interface
* Alternative content formats

---
