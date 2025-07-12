# 📟 Bansos Assistant

An AI-powered public service prototype developed for the **Bank Indonesia & OJK Hackathon 2025** under the theme:

> *"Financial Innovation & Public Services: Enhancing Digital Financial Literacy and Inclusion."*

This tool simulates how AI and rule-based automation can improve the transparency, accessibility, and personalization of **social assistance (Bansos)** services in Indonesia.

---

## 🚀 Features

### 1. 🤖 Bansos Chatbot (Gemini LLM-powered)

* Ask anything about PKH, BPNT, BLT, DTKS, and more.
* Trained prompt for accurate, friendly responses in Bahasa Indonesia.
* Powered by Google Gemini 1.5 Pro via API.

### 2. 📷 Simulasi Cek Registrasi dari Foto KTP

* Upload a KTP photo (simulated OCR extraction).
* Extracted: Name, NIK, Province, City, District, Village.
* Mocked API lookup for DTKS registration.
* Next-step guidance for unregistered users.

### 3. 📊 Cek Kelayakan Penerima Bansos

* User inputs household data (income, dependents, etc.).
* Rule-based logic determines potential eligibility.
* Gemini LLM explains eligibility in simple terms.

---

## 🪖 Tech Stack

* `Python` + `Streamlit`
* `Google Generative AI (Gemini 1.5 Pro)`
* Simulated OCR & mock DTKS validation
* Ready for deployment on Streamlit Cloud

---

## 📚 Use Cases

* Educate and empower citizens on Bansos programs
* Support pre-screening and triaging in Bansos registration
* Showcase responsible use of AI in public service delivery

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/bansos-assistant.git
cd bansos-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API Key

Create a `.env` file or edit directly:

```python
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
```

### 4. Run the app

```bash
streamlit run bansos_assistant.py
```

---

## 🌟 Credits

Built by [Putranegara Riauwindu](https://github.com/PRiauwindu), a Certified Financial Planner and Senior Analyst with a mission to scale digital inclusion through AI-powered tools.

---

## 🌍 License

MIT License — Free to use, modify, and distribute for non-commercial purposes with attribution.
