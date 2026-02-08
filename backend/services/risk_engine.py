"""
Risk Engine
Weighted fusion of 3-stage probabilities and escalation recommendations.
"""


class RiskEngine:
    """
    Calculates final risk score using weighted fusion and provides
    escalation recommendations based on risk category.
    """
    
    # Fusion weights emphasizing genetic and biomarker stages
    STAGE1_WEIGHT = 0.40  # Clinical baseline
    STAGE2_WEIGHT = 0.25  # Genetic refinement (APOE4)
    STAGE3_WEIGHT = 0.35  # Biomarker confirmation (pTau217)
    
    # Risk thresholds
    LOW_THRESHOLD = 0.30
    HIGH_THRESHOLD = 0.70
    
    @classmethod
    def calculate_final_risk(cls, stage1_prob, stage2_prob, stage3_prob):
        """
        Calculate weighted fusion of all 3 stage probabilities.
        
        Args:
            stage1_prob: Clinical screening probability (0-1)
            stage2_prob: Genetic stratification probability (0-1)
            stage3_prob: Biomarker analysis probability (0-1)
            
        Returns:
            Final risk score (0-1)
        """
        final_risk = (
            cls.STAGE1_WEIGHT * stage1_prob +
            cls.STAGE2_WEIGHT * stage2_prob +
            cls.STAGE3_WEIGHT * stage3_prob
        )
        return min(max(final_risk, 0.0), 1.0)  # Clamp to [0, 1]
    
    @classmethod
    def get_risk_category(cls, final_risk):
        """
        Determine risk category from final risk score.
        
        Args:
            final_risk: Final risk score (0-1)
            
        Returns:
            Risk category string
        """
        if final_risk < cls.LOW_THRESHOLD:
            return 'Low'
        elif final_risk < cls.HIGH_THRESHOLD:
            return 'Moderate'
        else:
            return 'High'
    
    @classmethod
    def get_escalation_recommendation(cls, risk_category):
        """
        Generate escalation recommendation based on risk category.
        
        Args:
            risk_category: 'Low', 'Moderate', or 'High'
            
        Returns:
            Recommendation text
        """
        recommendations = {
            'Low': (
                "Routine monitoring recommended. "
                "Consider rescreening in 2-3 years or if new symptoms develop. "
                "Maintain cognitive health through regular exercise, social engagement, "
                "and heart-healthy diet."
            ),
            'Moderate': (
                "Annual biomarker testing recommended. "
                "Consider consultation with a neurologist for baseline cognitive assessment. "
                "Monitor for any changes in memory, thinking, or daily function. "
                "Lifestyle modifications may help reduce risk."
            ),
            'High': (
                "Neurologist referral strongly recommended. "
                "Consider confirmatory imaging (MRI/PET) and comprehensive cognitive evaluation. "
                "Early intervention and clinical trial eligibility should be discussed. "
                "Family support and care planning may be appropriate."
            )
        }
        return recommendations.get(risk_category, recommendations['Low'])
    
    @classmethod
    def generate_full_assessment(cls, stage1_prob, stage2_prob, stage3_prob):
        """
        Generate complete risk assessment with all outputs.
        
        Args:
            stage1_prob: Clinical screening probability
            stage2_prob: Genetic stratification probability
            stage3_prob: Biomarker analysis probability
            
        Returns:
            dict with final_score, category, recommendation, and breakdown
        """
        # Calculate final risk
        final_risk = cls.calculate_final_risk(stage1_prob, stage2_prob, stage3_prob)
        
        # Get category and recommendation
        category = cls.get_risk_category(final_risk)
        recommendation = cls.get_escalation_recommendation(category)
        
        return {
            'final_risk_score': round(final_risk * 100, 1),  # Percentage
            'final_risk_probability': final_risk,
            'risk_category': category,
            'escalation_recommendation': recommendation,
            'pipeline_breakdown': {
                'stage1': {
                    'probability': round(stage1_prob * 100, 1),
                    'weight': f"{cls.STAGE1_WEIGHT * 100:.0f}%",
                    'contribution': round(cls.STAGE1_WEIGHT * stage1_prob * 100, 1)
                },
                'stage2': {
                    'probability': round(stage2_prob * 100, 1),
                    'weight': f"{cls.STAGE2_WEIGHT * 100:.0f}%",
                    'contribution': round(cls.STAGE2_WEIGHT * stage2_prob * 100, 1)
                },
                'stage3': {
                    'probability': round(stage3_prob * 100, 1),
                    'weight': f"{cls.STAGE3_WEIGHT * 100:.0f}%",
                    'contribution': round(cls.STAGE3_WEIGHT * stage3_prob * 100, 1)
                }
            },
            'disclaimer': (
                "IMPORTANT: This screening result is NOT a diagnosis. "
                "It indicates relative risk based on the provided inputs. "
                "Please consult a qualified healthcare provider for proper clinical evaluation."
            )
        }
