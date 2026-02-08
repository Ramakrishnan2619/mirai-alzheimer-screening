# 🚀 How MirAI Deploys Machine Learning Models on Render

This guide explains how the specific ML models (XGBoost classifiers, imputers, scalers) make their way from your local machine to the Render.com cloud server.

## 1. The Model files
Your project has a folder structure like this:
```
backend/
└── ml_models/
    ├── stage1/
    │   ├── stage1_model.pkl      (The Brains: XGBoost Classifier)
    │   ├── stage1_imputer.pkl    (The Cleaner: Handles missing data)
    │   └── stage1_scaler.pkl     (The Normalizer: Scales numbers)
    ├── stage2/
    │   └── ...
    └── stage3/
        └── ...
```

## 2. GitHub as the Transport 🚚
When we run:
```bash
git add .
git commit -m "..."
git push
```
We are uploading these binary `.pkl` (pickle) files to GitHub. 

> **Note:** GitHub allows files up to 100MB. Our models are small (<1MB), so they upload easily without needing special tools like Git LFS.

## 3. Render's Cloning Process ☁️
1. **Trigger:** When code hits GitHub, Render sees the new commit.
2. **Clone:** Render runs `git clone ...` on its server, pulling down your **entire repository**, including the `backend/ml_models` folder.
3. **Build:** Render runs `pip install -r requirements.txt` to install libraries (scikit-learn, xgboost) needed to *read* these files.

## 4. The Loading Logic 🧠
In `app.py`, we have this code:

```python
# Load ML models
with app.app_context():
    model_loader.load_all()
```

When the app starts on Render:
1. It looks inside `backend/ml_models/`.
2. It uses `joblib.load()` to read the `.pkl` files into memory.
3. The models are now "live" in the RAM of the Render server, ready to predict!

## ⚠️ Common Pitfalls
- **Missing Files:** If you add `backend/ml_models/` to `.gitignore`, they won't go to GitHub, and Render will fail.
- **Python Version Mismatch:** If you train on Python 3.10 but deploy on 3.13, models might break. relying on `runtime: python` in `render.yaml` helps control this.
- **Large Files:** If a model grows >100MB, you cannot push it to standard GitHub. You would need to use Git LFS or download it from an external URL (S3/Google Drive) during the build command.
