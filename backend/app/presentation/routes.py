"""
API Routes - Presentation layer
HTTP endpoints following REST conventions
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from ..domain.entities import TextInput
from .serializers import PredictionSerializer
import logging

logger = logging.getLogger(__name__)


def create_routes(di_container):
    """Factory function to create routes with dependency injection"""
    bp = Blueprint("api", __name__)

    @bp.route("/generate", methods=["POST"])
    def generate():
        """
        Generate text based on input
        POST /api/v1/generate
        
        Request body:
        {
            "content": "Hello world",
            "max_tokens": 50
        }
        """
        try:
            data = request.get_json()
            
            if not data or "content" not in data:
                return jsonify({"error": "Missing 'content' field"}), 400
            
            max_tokens = data.get("max_tokens", 50)
            
            # Create domain entity
            text_input = TextInput(
                content=data["content"],
                language=data.get("language", "en"),
                max_length=data.get("max_length"),
            )
            
            # Execute use case
            use_case = di_container.get_generate_text_use_case()
            prediction, prediction_id = use_case.execute(text_input, max_tokens=max_tokens)
            
            # Serialize response
            serializer = PredictionSerializer()
            return jsonify({
                "success": True,
                "prediction_id": prediction_id,
                "data": serializer.to_dict(prediction),
            }), 201
            
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error in /generate: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @bp.route("/predictions/<prediction_id>", methods=["GET"])
    def get_prediction(prediction_id):
        """
        Get specific prediction
        GET /api/v1/predictions/<prediction_id>
        """
        try:
            use_case = di_container.get_get_prediction_use_case()
            prediction = use_case.execute(prediction_id)
            
            serializer = PredictionSerializer()
            return jsonify({
                "success": True,
                "prediction_id": prediction_id,
                "data": serializer.to_dict(prediction),
            }), 200
            
        except ValueError as e:
            logger.warning(f"Prediction not found: {prediction_id}")
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logger.error(f"Error in /predictions/<id>: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @bp.route("/predictions", methods=["GET"])
    def get_predictions():
        """
        Get prediction history
        GET /api/v1/predictions?limit=10
        """
        try:
            limit = int(request.args.get("limit", 10))
            
            use_case = di_container.get_get_prediction_history_use_case()
            predictions = use_case.execute(limit=limit)
            
            serializer = PredictionSerializer()
            return jsonify({
                "success": True,
                "count": len(predictions),
                "data": [serializer.to_dict(p) for p in predictions],
            }), 200
            
        except ValueError as e:
            logger.warning(f"Invalid limit parameter: {str(e)}")
            return jsonify({"error": "Invalid limit parameter"}), 400
        except Exception as e:
            logger.error(f"Error in /predictions: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @bp.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
        }), 200

    return bp
