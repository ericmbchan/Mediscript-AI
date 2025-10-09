import os
from flask import Flask, jsonify, request
from flask_cors import CORS
try:
    from openai import OpenAI
    _OPENAI_V1_AVAILABLE = True
except Exception:
    _OPENAI_V1_AVAILABLE = False

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({"status": "ok"}), 200

@app.route('/api/generate', methods=['POST'])
def generate():
    payload = request.get_json(silent=True) or {}
    prompt = payload.get('prompt', '').strip()

    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    openai_api_key = app.config.get('OPENAI_API_KEY')
    if not openai_api_key:
        return jsonify({
            "error": "OpenAI API key not configured"
        }), 500

    try:
        system_prompt = """You are a medical documentation assistant. Transform raw medical notes into professional, structured clinical documentation.

Guidelines:
1. Use proper medical terminology and formatting
2. Structure with clear sections (Chief Complaint, History, Physical Exam, Assessment, Plan)
3. Maintain patient confidentiality and professionalism
4. Ensure accuracy and completeness

Output format:
**CHIEF COMPLAINT:**
[Patient's main concern]

**HISTORY OF PRESENT ILLNESS:**
[Detailed description of symptoms, onset, duration, severity]

**REVIEW OF SYSTEMS:**
[Relevant system review]

**PHYSICAL EXAMINATION:**
[Detailed physical findings organized by system]

**ASSESSMENT AND PLAN:**
[Diagnosis and treatment plan]

**MEDICATIONS:**
[Current medications if mentioned]

**FOLLOW-UP:**
[Follow-up instructions]"""

        if _OPENAI_V1_AVAILABLE:
            client = OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please convert these medical notes into professional clinical documentation:\n\n{prompt}"}
                ],
                max_tokens=2000,
                temperature=0.3,
                top_p=0.9,
            )
            generated_content = response.choices[0].message.content.strip()
            tokens_used = getattr(getattr(response, 'usage', None), 'total_tokens', None)
            model_used = "gpt-4o-mini"
        else:
            import openai as openai_legacy
            openai_legacy.api_key = openai_api_key
            completion = openai_legacy.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please convert these medical notes into professional clinical documentation:\n\n{prompt}"}
                ],
                max_tokens=2000,
                temperature=0.3,
                top_p=0.9,
            )
            generated_content = completion.choices[0].message["content"].strip()
            tokens_used = getattr(getattr(completion, 'usage', None), 'total_tokens', None)
            model_used = "gpt-3.5-turbo"

        return jsonify({
            "ok": True,
            "message": generated_content,
            "model": model_used,
            "tokens_used": tokens_used,
        }), 200

    except Exception as e:
        app.logger.error(f"OpenAI API error: {str(e)}")
        return jsonify({
            "error": f"Failed to generate documentation: {str(e)}"
        }), 500

@app.route('/')
def index():
    return jsonify({
        'message': 'Mediscript API is running',
        'endpoints': ['/health', '/api/health', '/api/generate']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
