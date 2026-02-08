"""
Prediction Routes
Stage-by-stage ML prediction endpoints.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models import Assessment
from backend.services import InferenceService, RiskEngine

predict_bp = Blueprint('predict', __name__, url_prefix='/api/predict')


@predict_bp.route('/stage1', methods=['POST'])
@jwt_required()
def predict_stage1():
    """
    Stage 1: Clinical Screening
    
    Request Body:
        {
            "age": 72,
            "gender": "Female",
            "education": 16,
            "faq": 5,
            "ecogMem": 2.5,
            "ecogTotal": 2.0,
            "assessment_id": 123 (optional, to continue existing assessment)
        }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Run inference
        result = InferenceService.predict_stage1(data)
        
        if not result['success']:
            return jsonify(result), 500
        
        # Create or update assessment
        assessment_id = data.get('assessment_id')
        if assessment_id:
            assessment = Assessment.query.filter_by(id=assessment_id, user_id=user_id).first()
        else:
            assessment = None
        
        if not assessment:
            assessment = Assessment(user_id=user_id)
            db.session.add(assessment)
        
        # Update Stage 1 data
        assessment.update_stage1(
            data=data,
            probability=result['probability'],
            risk_level=result['risk_level']
        )
        db.session.commit()
        
        # Add assessment ID to result
        result['assessment_id'] = assessment.id
        result['message'] = 'Stage 1 complete. Proceed to Stage 2 for genetic analysis.'
        
        return jsonify(result), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@predict_bp.route('/stage2', methods=['POST'])
@jwt_required()
def predict_stage2():
    """
    Stage 2: Genetic Stratification
    
    Request Body:
        {
            "assessment_id": 123,
            "genotype": "3/4"
        }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Get assessment
        assessment_id = data.get('assessment_id')
        if not assessment_id:
            return jsonify({'success': False, 'error': 'assessment_id is required'}), 400
        
        assessment = Assessment.query.filter_by(id=assessment_id, user_id=user_id).first()
        if not assessment:
            return jsonify({'success': False, 'error': 'Assessment not found'}), 404
        
        if not assessment.stage1_completed:
            return jsonify({'success': False, 'error': 'Stage 1 must be completed first'}), 400
        
        # Run inference with Stage 1 probability
        result = InferenceService.predict_stage2(data, assessment.stage1_probability)
        
        if not result['success']:
            return jsonify(result), 500
        
        # Update Stage 2 data
        assessment.update_stage2(
            data=data,
            probability=result['probability'],
            risk_level=result['risk_level'],
            apoe4_count=result['apoe4_count']
        )
        db.session.commit()
        
        # Add context to result
        result['assessment_id'] = assessment.id
        result['stage1_probability'] = assessment.stage1_probability
        result['message'] = 'Stage 2 complete. Proceed to Stage 3 for biomarker analysis.'
        
        return jsonify(result), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@predict_bp.route('/stage3', methods=['POST'])
@jwt_required()
def predict_stage3():
    """
    Stage 3: Biomarker Analysis
    
    Request Body:
        {
            "assessment_id": 123,
            "ptau217": 0.5,
            "ab42": 15.2,
            "ab40": 180.5,
            "nfl": 22.0
        }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Get assessment
        assessment_id = data.get('assessment_id')
        if not assessment_id:
            return jsonify({'success': False, 'error': 'assessment_id is required'}), 400
        
        assessment = Assessment.query.filter_by(id=assessment_id, user_id=user_id).first()
        if not assessment:
            return jsonify({'success': False, 'error': 'Assessment not found'}), 404
        
        if not assessment.stage2_completed:
            return jsonify({'success': False, 'error': 'Stage 2 must be completed first'}), 400
        
        # Run inference with Stage 2 probability
        result = InferenceService.predict_stage3(data, assessment.stage2_probability)
        
        if not result['success']:
            return jsonify(result), 500
        
        # Update Stage 3 data
        assessment.update_stage3(
            data=data,
            probability=result['probability'],
            risk_level=result['risk_level']
        )
        
        # Calculate final risk using Risk Engine
        final_assessment = RiskEngine.generate_full_assessment(
            assessment.stage1_probability,
            assessment.stage2_probability,
            result['probability']
        )
        
        # Update final results
        assessment.update_final_results(
            final_score=final_assessment['final_risk_probability'],
            category=final_assessment['risk_category'],
            recommendation=final_assessment['escalation_recommendation']
        )
        db.session.commit()
        
        # Combine results
        result['assessment_id'] = assessment.id
        result['final_assessment'] = final_assessment
        result['message'] = 'Assessment complete. View your full risk report.'
        
        return jsonify(result), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@predict_bp.route('/full', methods=['POST'])
@jwt_required()
def predict_full():
    """
    Run all 3 stages in one request.
    
    Request Body:
        {
            "age": 72,
            "gender": "Female",
            "education": 16,
            "faq": 5,
            "ecogMem": 2.5,
            "ecogTotal": 2.0,
            "genotype": "3/4",
            "ptau217": 0.5,
            "ab42": 15.2,
            "ab40": 180.5,
            "nfl": 22.0
        }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Stage 1
        stage1_result = InferenceService.predict_stage1(data)
        if not stage1_result['success']:
            return jsonify(stage1_result), 500
        
        # Stage 2
        stage2_result = InferenceService.predict_stage2(data, stage1_result['probability'])
        if not stage2_result['success']:
            return jsonify(stage2_result), 500
        
        # Stage 3
        stage3_result = InferenceService.predict_stage3(data, stage2_result['probability'])
        if not stage3_result['success']:
            return jsonify(stage3_result), 500
        
        # Final Assessment
        final_assessment = RiskEngine.generate_full_assessment(
            stage1_result['probability'],
            stage2_result['probability'],
            stage3_result['probability']
        )
        
        # Create and save assessment
        assessment = Assessment(user_id=user_id)
        db.session.add(assessment)
        
        assessment.update_stage1(data, stage1_result['probability'], stage1_result['risk_level'])
        assessment.update_stage2(data, stage2_result['probability'], stage2_result['risk_level'], stage2_result['apoe4_count'])
        assessment.update_stage3(data, stage3_result['probability'], stage3_result['risk_level'])
        assessment.update_final_results(
            final_assessment['final_risk_probability'],
            final_assessment['risk_category'],
            final_assessment['escalation_recommendation']
        )
        db.session.commit()
        
        return jsonify({
            'success': True,
            'assessment_id': assessment.id,
            'stage1': stage1_result,
            'stage2': stage2_result,
            'stage3': stage3_result,
            'final_assessment': final_assessment
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
