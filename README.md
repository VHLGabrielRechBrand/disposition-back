# Disposition Backend

The backend of **Disposition**, a document processing platform that uses OCR and AI to convert images and PDFs into structured data. This service is built with FastAPI and integrates tools like Tesseract, OpenAI, and Google OAuth for robust document scanning and AI-enhanced extraction.

## 🧠 Features

- OCR support for scanned documents (images, PDFs)
- AI-assisted data extraction with OpenAI
- Google OAuth2 authentication
- MongoDB integration for data persistence
- Dockerized for easy deployment

## 📁 Project Structure

```
.
├── src/
│   ├── api/              # FastAPI routes
│   ├── dependencies/     # Dependency injection modules
│   ├── enumeration/      # Enums used throughout the app
│   ├── services/         # Core business logic (OCR, AI)
│   ├── utils/            # Utility functions
├── tests/                # Pytest test suite
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker build configuration
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/VHLGabrielRechBrand/disposition-back.git
cd disposition-back
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file in the root with the following (example):

```env
MONGO_URI=mongodb://localhost:27017
OPENAI_API_KEY=your_openai_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### 5. Run the application

```bash
uvicorn src.main:app --reload --port 10000
```

Visit: [http://localhost:10000/docs](http://localhost:10000/docs) to see the interactive API docs.

## 🐳 Using Docker

To build and run the app in Docker:

```bash
docker build -t disposition-backend .
docker run -p 10000:10000 --env-file .env disposition-backend
```

## 🧪 Running Tests

```bash
pytest
```

## 🧠 Tech Stack

- **FastAPI** – Modern web framework for APIs
- **Tesseract OCR** – Optical character recognition
- **PDF2Image** – PDF to image conversion
- **OpenAI** – AI-powered data extraction
- **Google OAuth** – Authentication layer
- **MongoDB** – NoSQL document database
