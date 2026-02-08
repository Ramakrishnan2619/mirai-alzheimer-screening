---
description: How to run the MirAI Alzheimer's risk screening platform locally
---

# MirAI Local Development Workflow

## Prerequisites
- Python 3.10+
- pip (package manager)

## Setup Steps

// turbo-all

### 1. Install Dependencies
```bash
cd d:\mirai_fnal_2.0
pip install flask flask-cors flask-sqlalchemy flask-jwt-extended flask-bcrypt pandas numpy scikit-learn xgboost joblib python-dotenv
```

### 2. Start the Flask Server
```bash
python app.py
```

### 3. Access the Application
Open browser to: http://localhost:5000

## Application Flow

1. **Register** at `/register.html`
2. **Login** at `/login.html`  
3. **Take Assessment** at `/assessment.html`
   - Stage 1: Clinical screening (FAQ, EcogMem, EcogTotal)
   - Stage 2: Genetic (APOE genotype) - optional
   - Stage 3: Biomarkers (pTau-217, Ab42) - optional
4. **View Results** at `/results.html`

## Testing Stage-1 via API

```bash
python test_stage1.py
```

## Files Structure

- `app.py` - Flask application entry point
- `config.py` - Configuration settings
- `templates/` - HTML templates (MediLab UI)
- `static/assets/` - CSS, JS, images
- `backend/` - Python backend code
  - `routes/` - API endpoints
  - `services/` - ML inference
  - `models.py` - Database models
  - `ml_models/` - XGBoost model artifacts
