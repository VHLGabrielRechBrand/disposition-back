# 🧾 Disposition

Disposition is an intelligent document scanning API that extracts text from images, uses AI to classify and structure the content, and stores the result in a MongoDB database. It’s built using FastAPI, Tesseract OCR, OpenAI, and MongoDB.

---

## 📦 Features

- Upload image files (`.jpg`, `.jpeg`, `.png`)
- Extract text using Tesseract OCR
- Classify and structure content using OpenAI (GPT)
- Store documents by type in MongoDB
- Retrieve collections and documents
- Delete documents by ID

---

## 🛠️ Tech Stack

- **FastAPI** – Web framework
- **Tesseract OCR** – Text recognition from images
- **OpenAI API** – AI-powered document classification and parsing
- **MongoDB** – NoSQL database for storing structured data
- **Pillow** – Image handling
- **Dotenv** – Environment variable management

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/VHLGabrielRechBrand/disposition-backend.git
cd disposition-backend
