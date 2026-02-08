"""
Results Routes
Endpoints for retrieving user assessment history.
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Assessment

results_bp = Blueprint('results', __name__, url_prefix='/api/results')


@results_bp.route('', methods=['GET'])
@jwt_required()
def get_all_results():
    """
    Get all assessments for the current user.
    """
    try:
        user_id = int(get_jwt_identity())
        
        assessments = Assessment.query.filter_by(user_id=user_id).order_by(
            Assessment.created_at.desc()
        ).all()
        
        return jsonify({
            'success': True,
            'count': len(assessments),
            'assessments': [a.to_dict() for a in assessments]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@results_bp.route('/<int:assessment_id>', methods=['GET'])
@jwt_required()
def get_result(assessment_id):
    """
    Get a specific assessment by ID.
    """
    try:
        user_id = int(get_jwt_identity())
        
        assessment = Assessment.query.filter_by(
            id=assessment_id,
            user_id=user_id
        ).first()
        
        if not assessment:
            return jsonify({'success': False, 'error': 'Assessment not found'}), 404
        
        return jsonify({
            'success': True,
            'assessment': assessment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@results_bp.route('/latest', methods=['GET'])
@jwt_required()
def get_latest_result():
    """
    Get the most recent completed assessment.
    """
    try:
        user_id = int(get_jwt_identity())
        
        assessment = Assessment.query.filter_by(user_id=user_id).filter(
            Assessment.completed_at.isnot(None)
        ).order_by(Assessment.completed_at.desc()).first()
        
        if not assessment:
            return jsonify({'success': False, 'error': 'No completed assessments found'}), 404
        
        return jsonify({
            'success': True,
            'assessment': assessment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@results_bp.route('/in-progress', methods=['GET'])
@jwt_required()
def get_in_progress():
    """
    Get any incomplete assessment (for resuming).
    """
    try:
        user_id = int(get_jwt_identity())
        
        assessment = Assessment.query.filter_by(user_id=user_id).filter(
            Assessment.completed_at.is_(None)
        ).order_by(Assessment.created_at.desc()).first()
        
        if not assessment:
            return jsonify({
                'success': True,
                'assessment': None,
                'message': 'No in-progress assessments'
            }), 200
        
        return jsonify({
            'success': True,
            'assessment': assessment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
