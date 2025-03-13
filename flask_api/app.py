from flask import Flask, request, jsonify
from transformers import pipeline
import joblib
from werkzeug.security import check_password_hash
from functools import wraps

app = Flask(__name__)

# Authentication details
USERNAME = "admin"
PASSWORD = "password"

# Load NER model
ner_pipeline = pipeline("ner", model="./bert-ner-f", tokenizer="./bert-ner-f")

# Mapping labels to meaningful entities
label_map = {
    "LABEL_0": "Other",
    "LABEL_1": "Person",
    "LABEL_2": "Person",
    "LABEL_3": "Organization",
    "LABEL_4": "Organization",
    "LABEL_5": "Location",
    "LABEL_6": "Location",
    "LABEL_7": "Miscellaneous",
    "LABEL_8": "Miscellaneous"
}

# Function to merge entities
def merge_entities(results):
    merged = []
    current_entity = None
    current_word = ""
    current_score = 0.0
    count = 0

    for ent in results:
        if ent['label'] != "Other":
            if current_entity == ent['label']:
                current_word += ent['text'].replace("##", "")
                current_score += ent['score']
                count += 1
            else:
                if current_entity:
                    merged.append({
                        "text": current_word,
                        "label": current_entity,
                        "score": round(current_score / count, 4)
                    })
                current_word = ent['text'].replace("##", "")
                current_entity = ent['label']
                current_score = ent['score']
                count = 1
        else:
            if current_entity:
                merged.append({
                    "text": current_word,
                    "label": current_entity,
                    "score": round(current_score / count, 4)
                })
            merged.append(ent)
            current_entity = None
            current_word = ""
            current_score = 0.0
            count = 0

    if current_entity:
        merged.append({
            "text": current_word,
            "label": current_entity,
            "score": round(current_score / count, 4)
        })

    return merged

# Authentication decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/predict', methods=['POST'])
@requires_auth
def predict():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Run NER pipeline and map labels
    results = [
        {
            "text": ent['word'],
            "label": label_map.get(ent['entity'], "Unknown"),
            "score": float(ent['score'])  # Convert numpy.float32 to float
        }
        for ent in ner_pipeline(text)
    ]

    # Merge subword tokens into full entities
    merged_results = merge_entities(results)

    return jsonify({"entities": merged_results})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
