"""
Assessment Model
SQLAlchemy model for storing user assessment data across all 3 stages.
"""
from datetime import datetime
from backend.extensions import db


class Assessment(db.Model):
    """Assessment model storing all stage data and results."""
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Stage 1: Clinical Data
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    education = db.Column(db.Integer)
    faq_score = db.Column(db.Float)
    ecog_mem = db.Column(db.Float)
    ecog_total = db.Column(db.Float)
    stage1_probability = db.Column(db.Float)
    stage1_risk = db.Column(db.String(20))
    stage1_completed = db.Column(db.Boolean, default=False)
    
    # Stage 2: Genetic Data
    apoe_genotype = db.Column(db.String(10))
    apoe4_count = db.Column(db.Integer)
    stage2_probability = db.Column(db.Float)
    stage2_risk = db.Column(db.String(20))
    stage2_completed = db.Column(db.Boolean, default=False)
    
    # Stage 3: Biomarker Data
    ptau217 = db.Column(db.Float)
    ab42 = db.Column(db.Float)
    ab40 = db.Column(db.Float)
    nfl = db.Column(db.Float)
    stage3_probability = db.Column(db.Float)
    stage3_risk = db.Column(db.String(20))
    stage3_completed = db.Column(db.Boolean, default=False)
    
    # Final Results
    final_risk_score = db.Column(db.Float)
    final_risk_category = db.Column(db.String(20))
    escalation_recommendation = db.Column(db.Text)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def update_stage1(self, data, probability, risk_level):
        """Update Stage 1 clinical data."""
        self.age = data.get('age')
        self.gender = data.get('gender')
        self.education = data.get('education')
        self.faq_score = data.get('faq')
        self.ecog_mem = data.get('ecogMem')
        self.ecog_total = data.get('ecogTotal')
        self.stage1_probability = probability
        self.stage1_risk = risk_level
        self.stage1_completed = True
    
    def update_stage2(self, data, probability, risk_level, apoe4_count):
        """Update Stage 2 genetic data."""
        self.apoe_genotype = data.get('genotype')
        self.apoe4_count = apoe4_count
        self.stage2_probability = probability
        self.stage2_risk = risk_level
        self.stage2_completed = True
    
    def update_stage3(self, data, probability, risk_level):
        """Update Stage 3 biomarker data."""
        self.ptau217 = data.get('ptau217')
        self.ab42 = data.get('ab42')
        self.ab40 = data.get('ab40')
        self.nfl = data.get('nfl')
        self.stage3_probability = probability
        self.stage3_risk = risk_level
        self.stage3_completed = True
    
    def update_final_results(self, final_score, category, recommendation):
        """Update final risk assessment."""
        self.final_risk_score = final_score
        self.final_risk_category = category
        self.escalation_recommendation = recommendation
        self.completed_at = datetime.utcnow()
    
    def to_dict(self):
        """Serialize assessment to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'stage1': {
                'completed': self.stage1_completed,
                'data': {
                    'age': self.age,
                    'gender': self.gender,
                    'education': self.education,
                    'faq': self.faq_score,
                    'ecogMem': self.ecog_mem,
                    'ecogTotal': self.ecog_total
                },
                'probability': self.stage1_probability,
                'risk': self.stage1_risk
            },
            'stage2': {
                'completed': self.stage2_completed,
                'data': {
                    'genotype': self.apoe_genotype,
                    'apoe4_count': self.apoe4_count
                },
                'probability': self.stage2_probability,
                'risk': self.stage2_risk
            },
            'stage3': {
                'completed': self.stage3_completed,
                'data': {
                    'ptau217': self.ptau217,
                    'ab42': self.ab42,
                    'ab40': self.ab40,
                    'nfl': self.nfl
                },
                'probability': self.stage3_probability,
                'risk': self.stage3_risk
            },
            'final': {
                'score': self.final_risk_score,
                'category': self.final_risk_category,
                'recommendation': self.escalation_recommendation
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<Assessment {self.id} for User {self.user_id}>'
