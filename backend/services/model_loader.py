"""
Model Loader Service
Loads XGBoost models, imputers, and scalers for all 3 stages.
"""
import os
import joblib
import xgboost as xgb


class ModelLoader:
    """
    Singleton model loader that loads and caches all ML artifacts.
    """
    _instance = None
    _models = {}
    _imputers = {}
    _scalers = {}
    _loaded = False
    
    def __new__(cls, models_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, models_path=None):
        if models_path:
            self.models_path = models_path
        elif not hasattr(self, 'models_path'):
            # Default path relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.models_path = os.path.join(base_dir, 'ml_models')
    
    def load_all(self):
        """Load all artifacts for all 3 stages."""
        if self._loaded:
            return True
        
        try:
            for stage in [1, 2, 3]:
                self._load_stage(stage)
            self._loaded = True
            print("✅ MirAI ML models loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return False
    
    def _load_stage(self, stage):
        """Load artifacts for a specific stage."""
        stage_path = os.path.join(self.models_path, f'stage{stage}')
        
        # Load XGBoost model
        model_file = os.path.join(stage_path, f'stage{stage}_model.json')
        if os.path.exists(model_file):
            model = xgb.XGBClassifier()
            model.load_model(model_file)
            self._models[stage] = model
        else:
            raise FileNotFoundError(f"Model not found: {model_file}")
        
        # Load Imputer
        imputer_file = os.path.join(stage_path, f'stage{stage}_imputer.pkl')
        if os.path.exists(imputer_file):
            self._imputers[stage] = joblib.load(imputer_file)
        else:
            raise FileNotFoundError(f"Imputer not found: {imputer_file}")
        
        # Load Scaler
        scaler_file = os.path.join(stage_path, f'stage{stage}_scaler.pkl')
        if os.path.exists(scaler_file):
            self._scalers[stage] = joblib.load(scaler_file)
        else:
            raise FileNotFoundError(f"Scaler not found: {scaler_file}")
    
    def get_model(self, stage):
        """Get XGBoost model for a stage."""
        if not self._loaded:
            self.load_all()
        return self._models.get(stage)
    
    def get_imputer(self, stage):
        """Get imputer for a stage."""
        if not self._loaded:
            self.load_all()
        return self._imputers.get(stage)
    
    def get_scaler(self, stage):
        """Get scaler for a stage."""
        if not self._loaded:
            self.load_all()
        return self._scalers.get(stage)
    
    def is_loaded(self):
        """Check if models are loaded."""
        return self._loaded


# Global singleton instance
model_loader = ModelLoader()
