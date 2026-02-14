---
title: MirAI Alzheimer Screening 
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---

# MirAI - Alzheimer's Early Screening Platform

**MirAI** (未来 - "Future") is a production-grade, multi-stage Alzheimer's Disease early-screening platform using a 3-tier cascade AI model.

![MirAI](https://img.shields.io/badge/MirAI-v2.0-6366f1)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)

## 🧠 Overview

MirAI uses a **3-stage cascade architecture** where each stage's probability output feeds into the next:

| Stage | Input | Model | Output |
|-------|-------|-------|--------|
| **Stage 1** | Age, Gender, Education, FAQ, ECog | XGBoost | Stage1_Prob |
| **Stage 2** | Stage1_Prob + APOE4 Count | XGBoost | Stage2_Prob |
| **Stage 3** | Stage2_Prob + pTau-217, Aβ42, Aβ40, NfL | XGBoost | Final_Prob |

**Final Risk** = `0.40×Stage1 + 0.25×Stage2 + 0.35×Stage3`

## ✨ Features

- 🔐 **Authentication** - Registration, login, JWT sessions, bcrypt hashing
- 🗄️ **Database** - SQLite persistence for users and assessments
- 🧪 **ML Pipeline** - Real XGBoost inference with imputers and scalers
- 📊 **Risk Engine** - Weighted fusion with escalation recommendations
- 🎨 **Modern UI** - Responsive, animated, glassmorphism design
- 🚀 **Render Ready** - One-click deployment configuration

## 🚀 Quick Start

### 1. Clone & Install

```bash
cd d:\mirai_fnal_2.0
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

### 3. Test the Flow

1. Click **Register** to create an account
2. Start a new **Assessment**
3. Complete all 3 stages
4. View your **Risk Report**

## 📁 Project Structure

```
mirai_fnal_2.0/
├── app.py                  # Flask application entry
├── config.py               # Environment configuration
├── requirements.txt        # Python dependencies
├── render.yaml             # Render.com deployment
│
├── backend/
│   ├── extensions.py       # Flask extensions
│   ├── models/             # SQLAlchemy models
│   │   ├── user.py
│   │   └── assessment.py
│   ├── routes/             # API blueprints
│   │   ├── auth.py
│   │   ├── predict.py
│   │   └── results.py
│   ├── services/           # Business logic
│   │   ├── model_loader.py
│   │   ├── inference.py
│   │   └── risk_engine.py
│   └── ml_models/          # Trained XGBoost artifacts
│
└── templates/              # HTML pages
    ├── index.html
    ├── register.html
    ├── login.html
    ├── assessment.html
    └── results.html
```

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login (returns JWT) |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/me` | Current user |

### Prediction (requires JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict/stage1` | Clinical screening |
| POST | `/api/predict/stage2` | Genetic stratification |
| POST | `/api/predict/stage3` | Biomarker analysis |
| POST | `/api/predict/full` | All 3 stages at once |

### Results (requires JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/results` | List all assessments |
| GET | `/api/results/latest` | Most recent result |
| GET | `/api/results/<id>` | Specific assessment |

## 🌐 Deploy to Render

1. Push to GitHub:
```bash
git init
git add .
git commit -m "MirAI v2.0"
git remote add origin <your-repo-url>
git push -u origin main
```

2. Connect repo to Render.com
3. Render auto-detects `render.yaml` and deploys

**URL:** `https://mirai-alzheimer-api.onrender.com/`

## 🛠️ Tech Stack

- **Backend:** Flask, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-Bcrypt
- **ML:** XGBoost, scikit-learn, pandas, numpy
- **Frontend:** Bootstrap 5, Bootstrap Icons, AOS animations
- **Database:** SQLite
- **Deployment:** Gunicorn, Render.com

## ⚠️ Disclaimer

> MirAI is a **screening tool**, NOT a diagnostic instrument. Results indicate relative risk and do NOT constitute a medical diagnosis. Always consult a qualified healthcare provider for proper clinical evaluation.

## 📜 License

Research use only. © 2026 MirAI Project.
