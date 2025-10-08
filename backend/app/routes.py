import os
from flask import Blueprint, jsonify, request, current_app
try:
    # Preferred: OpenAI SDK v1.x
    from openai import OpenAI  # type: ignore
    _OPENAI_V1_AVAILABLE = True
except Exception:  # pragma: no cover - fall back gracefully
    _OPENAI_V1_AVAILABLE = False

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

    # Check if OpenAI API key is configured
    openai_api_key = current_app.config.get('OPENAI_API_KEY')
    if not openai_api_key:
        return jsonify({
            "error": "OpenAI API key not configured. Please set OPENAI_API_KEY in your environment variables."
        }), 500

    try:
        # Create a comprehensive medical documentation prompt
        system_prompt = """You are a medical documentation assistant. Your task is to transform raw medical notes into professional, structured clinical documentation.

Guidelines:
1. Use proper medical terminology and formatting
2. Structure the output with clear sections (Chief Complaint, History, Physical Exam, Assessment, Plan)
3. Maintain patient confidentiality and professionalism
4. Ensure accuracy and completeness
5. Use standard medical abbreviations where appropriate
6. Format as a proper clinical note

Output format:
**CHIEF COMPLAINT:**
[Patient's main concern]

**HISTORY OF PRESENT ILLNESS:**
[Detailed description of symptoms, onset, duration, severity, associated symptoms]

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

        # Generate the clinical documentation using available SDK
        if _OPENAI_V1_AVAILABLE:
            try:
                # v1.x client path
                client = OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Please convert these medical notes into professional clinical documentation:\n\n{prompt}"}
                    ],
                    max_tokens=1200,
                    temperature=0.3,
                    top_p=0.9,
                )
                generated_content = response.choices[0].message.content.strip()
                tokens_used = getattr(getattr(response, 'usage', None), 'total_tokens', None)
                model_used = "gpt-4o-mini"
            except TypeError as te:
                # Some older v1 builds may raise unexpected kw errors (e.g., 'proxies')
                if 'unexpected keyword argument' in str(te) or 'proxies' in str(te):
                    # Fall back to legacy SDK path
                    import openai as openai_legacy  # type: ignore
                    openai_legacy.api_key = openai_api_key
                    completion = openai_legacy.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Please convert these medical notes into professional clinical documentation:\n\n{prompt}"}
                        ],
                        max_tokens=1200,
                        temperature=0.3,
                        top_p=0.9,
                    )
                    generated_content = completion.choices[0].message["content"].strip()
                    tokens_used = getattr(getattr(completion, 'usage', None), 'total_tokens', None)
                    model_used = "gpt-3.5-turbo"
                else:
                    raise
        else:
            # Legacy 0.x fallback
            import openai as openai_legacy  # type: ignore
            openai_legacy.api_key = openai_api_key
            completion = openai_legacy.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please convert these medical notes into professional clinical documentation:\n\n{prompt}"}
                ],
                max_tokens=1200,
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
        current_app.logger.error(f"OpenAI API error: {str(e)}")
        return jsonify({
            "error": f"Failed to generate documentation: {str(e)}"
        }), 500


