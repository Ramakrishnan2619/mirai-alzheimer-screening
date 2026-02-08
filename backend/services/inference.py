"""
Inference Service
Stage-by-stage ML inference for the MirAI cascade model.
"""
import numpy as np
import pandas as pd
from .model_loader import model_loader


class InferenceService:
    """
    Handles ML inference for all 3 stages of the MirAI cascade.
    """
    
    # Feature definitions for each stage
    STAGE1_FEATURES = ['AGE', 'PTGENDER', 'PTEDUCAT', 'FAQ', 'EcogPtMem', 'EcogPtTotal']
    STAGE2_FEATURES = ['Stage1_Prob', 'APOE4_Count']
    STAGE3_FEATURES = ['Stage2_Prob', 'pT217_F', 'AB42_F', 'AB40_F', 'NfL_Q']
    
    @staticmethod
    def preprocess_gender(gender):
        """Convert gender string to numeric."""
        if isinstance(gender, str):
            return 1 if gender.lower() == 'male' else 0
        return gender
    
    @staticmethod
    def count_apoe4(genotype):
        """Count APOE4 alleles from genotype string (e.g., '3/4' -> 1)."""
        if not genotype:
            return 0
        return str(genotype).count('4')
    
    @staticmethod
    def get_risk_level(probability, thresholds=(0.3, 0.6)):
        """Determine risk level from probability."""
        if probability < thresholds[0]:
            return 'Low'
        elif probability < thresholds[1]:
            return 'Elevated'
        else:
            return 'High'
    
    @classmethod
    def predict_stage1(cls, data):
        """
        Stage 1: Clinical Screening
        
        Args:
            data: dict with keys: age, gender, education, faq, ecogMem, ecogTotal
            
        Returns:
            dict with probability, risk_level, and factors
        """
        try:
            # Prepare feature vector
            features = {
                'AGE': float(data.get('age', 65)),
                'PTGENDER': cls.preprocess_gender(data.get('gender', 'Male')),
                'PTEDUCAT': float(data.get('education', 16)),
                'FAQ': float(data.get('faq', 0)),
                'EcogPtMem': float(data.get('ecogMem', 1)),
                'EcogPtTotal': float(data.get('ecogTotal', 1))
            }
            
            # Create DataFrame
            X = pd.DataFrame([features])[cls.STAGE1_FEATURES]
            
            # Get model artifacts
            imputer = model_loader.get_imputer(1)
            scaler = model_loader.get_scaler(1)
            model = model_loader.get_model(1)
            
            # Transform and predict
            X_imputed = imputer.transform(X)
            X_scaled = scaler.transform(X_imputed)
            probability = float(model.predict_proba(X_scaled)[0, 1])
            
            # Determine risk level
            risk_level = cls.get_risk_level(probability)
            
            # Generate factors
            factors = []
            if features['FAQ'] >= 5:
                factors.append(f"FAQ score of {features['FAQ']:.0f} indicates functional difficulty")
            if features['EcogPtMem'] >= 2:
                factors.append(f"Memory self-rating ({features['EcogPtMem']:.1f}) suggests subjective concern")
            if features['AGE'] >= 75:
                factors.append(f"Age ({features['AGE']:.0f}) is a significant risk factor")
            if not factors:
                factors.append("No significant clinical risk factors identified")
            
            return {
                'success': True,
                'stage': 1,
                'probability': probability,
                'risk_level': risk_level,
                'factors': factors
            }
            
        except Exception as e:
            return {
                'success': False,
                'stage': 1,
                'error': str(e)
            }
    
    @classmethod
    def predict_stage2(cls, data, stage1_probability):
        """
        Stage 2: Genetic Stratification
        
        Args:
            data: dict with key: genotype (e.g., '3/4')
            stage1_probability: float from Stage 1 output
            
        Returns:
            dict with probability, risk_level, apoe4_count, and insight
        """
        try:
            # Parse APOE4 count
            genotype = data.get('genotype', '')
            apoe4_count = cls.count_apoe4(genotype)
            
            # Prepare feature vector
            features = {
                'Stage1_Prob': float(stage1_probability),
                'APOE4_Count': apoe4_count
            }
            
            # Create DataFrame
            X = pd.DataFrame([features])[cls.STAGE2_FEATURES]
            
            # Get model artifacts
            imputer = model_loader.get_imputer(2)
            scaler = model_loader.get_scaler(2)
            model = model_loader.get_model(2)
            
            # Transform and predict
            X_imputed = imputer.transform(X)
            X_scaled = scaler.transform(X_imputed)
            probability = float(model.predict_proba(X_scaled)[0, 1])
            
            # Determine risk level
            risk_level = cls.get_risk_level(probability)
            
            # Generate genetic insight
            if apoe4_count == 2:
                insight = "APOE4 Homozygous (ε4/ε4) - Two copies significantly increase risk"
            elif apoe4_count == 1:
                insight = "APOE4 Carrier (1 copy) - Moderately increases risk"
            elif genotype:
                insight = "No APOE4 alleles detected"
            else:
                insight = "Genetic data not provided"
            
            return {
                'success': True,
                'stage': 2,
                'probability': probability,
                'risk_level': risk_level,
                'apoe4_count': apoe4_count,
                'genetic_insight': insight
            }
            
        except Exception as e:
            return {
                'success': False,
                'stage': 2,
                'error': str(e)
            }
    
    @classmethod
    def predict_stage3(cls, data, stage2_probability):
        """
        Stage 3: Biomarker Analysis
        
        Args:
            data: dict with keys: ptau217, ab42, ab40, nfl
            stage2_probability: float from Stage 2 output
            
        Returns:
            dict with probability, risk_level, and biomarker_insight
        """
        try:
            # Prepare feature vector
            features = {
                'Stage2_Prob': float(stage2_probability),
                'pT217_F': float(data.get('ptau217') or 0),
                'AB42_F': float(data.get('ab42') or 0),
                'AB40_F': float(data.get('ab40') or 0),
                'NfL_Q': float(data.get('nfl') or 0)
            }
            
            # Create DataFrame
            X = pd.DataFrame([features])[cls.STAGE3_FEATURES]
            
            # Get model artifacts
            imputer = model_loader.get_imputer(3)
            scaler = model_loader.get_scaler(3)
            model = model_loader.get_model(3)
            
            # Transform and predict
            X_imputed = imputer.transform(X)
            X_scaled = scaler.transform(X_imputed)
            probability = float(model.predict_proba(X_scaled)[0, 1])
            
            # Determine risk level
            risk_level = cls.get_risk_level(probability, thresholds=(0.3, 0.7))
            
            # Generate biomarker insight
            ptau = features['pT217_F']
            if ptau > 0.6:
                insight = f"pTau-217 ({ptau:.2f} pg/mL) is elevated - suggests tau pathology"
            elif ptau > 0:
                insight = f"pTau-217 ({ptau:.2f} pg/mL) is within normal range"
            else:
                insight = "Biomarker data not provided"
            
            return {
                'success': True,
                'stage': 3,
                'probability': probability,
                'risk_level': risk_level,
                'biomarker_insight': insight
            }
            
        except Exception as e:
            return {
                'success': False,
                'stage': 3,
                'error': str(e)
            }
