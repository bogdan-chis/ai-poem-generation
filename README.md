# 🖋️📜 Transformer-Based Poetry Generation Inspired by Nichita Stănescu's Work

This repository contains a complete system for **Romanian poetry generation** based on a fine-tuned **RoGPT-2 medium** language model, inspired by the poetry of **Nichita Stănescu**.

It includes:
- 📓 a **training + evaluation pipeline** implemented in Python notebooks  
- ⚡ a **FastAPI backend** that serves the model for inference  
- 🖥️ a **React (Vite) web interface** for interactive poem generation  

---

## ✨ What the repo does

The project explores **creative text generation** using a Transformer model fine-tuned on a domain-specific corpus of Romanian poetry.  
Users can provide a poem title as a prompt and adjust sampling controls to observe how generation behavior changes.

The web app supports:
- entering a **poem title prompt**
- adjusting **generation hyperparameters**:
  - `max_new_tokens`
  - `temperature`
  - `top_p`
- generating and viewing the poem output in real time
- a manuscript-inspired UI theme (parchment + ink)

---

## 🧠 Model & training details

- Base model: **RoGPT-2 medium** (Hugging Face / ReaderBench ecosystem)
- Task: **Causal Language Modeling (CLM)**
- Corpus: **139 poems**, tokenized to ~**20k tokens**
- Block size (sequence length): **256**
- Approx. sequences: `20000 / 256 ≈ 82`
- Training configuration:
  - `per_device_train_batch_size = 2`
  - `gradient_accumulation_steps = 4`
  - Effective batch size: `2 * 4 = 8`
  - Optimization steps / epoch: `ceil(82 / 8) = 11`
  - Epochs: **50**
  - Total update steps: `11 * 50 = 550`

---


## 🚀 How to run the project

### 1) Start the backend (FastAPI)

#### Requirements
- Python **3.9+**
- `pip`

#### Install dependencies
```
cd backend
pip install -r requirements.txt
```
Run the API
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
Backend will run at:
http://localhost:8000

### 2) Start the frontend (React + Vite)
Requirements
Node.js 18+
npm

Install dependencies
```
cd frontend
npm install
```
Run the dev server

```
npm run dev
```
Frontend will run at: http://localhost:5173

The frontend expects the backend at http://localhost:8000 (configured in frontend/src/api.ts).

## 🔌 API Summary

The backend exposes a text generation endpoint used by the React frontend.

**Typical request fields:**
- `title` *(string)* — poem title used as prompt
- `max_new_tokens` *(int)* — maximum number of generated tokens
- `temperature` *(float)* — sampling temperature
- `top_p` *(float)* — nucleus sampling probability

---

## 🧪 Notebooks

- **`dataset.ipynb`** — data loading, cleaning, tokenization, and dataset construction  
- **`model-fine-tuning.ipynb`** — fine-tuning the RoGPT-2 model using the Hugging Face `Trainer` API  
- **`evaluation.ipynb`** — automatic evaluation and qualitative generation examples  

---

## 🛠️ Tech Stack

- **Python**, **PyTorch**
- **Hugging Face Transformers**
- **FastAPI**
- **React + Vite + TypeScript**
- **HTML / CSS**

---

## 🎓 Academic Context

This project was developed as part of an academic assignment focused on:
- Natural Language Processing (NLP)
- Transformer-based language models
- Fine-tuning and domain adaptation
- Creative text generation
- Building an interactive web-based demonstration
