from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health() -> tuple:
    return jsonify({"status": "ok"}), 200


@api_bp.route('/generate', methods=['POST'])
def generate() -> tuple:
    payload = request.get_json(silent=True) or {}
    prompt = payload.get('prompt', '').strip()

    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    # Placeholder response; integrate OpenAI later using OPENAI_API_KEY
    return jsonify({
        "ok": True,
        "message": f"You asked: {prompt}",
        "model": "placeholder",
    }), 200


