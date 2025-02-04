import os

from flask import Flask, request, jsonify
from fastapi import HTTPException
from prompt_template import generate_prompt
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key! Please set it in the environment variable")

app = Flask(__name__)


client = OpenAI(
    api_key=OPENAI_API_KEY
)


@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    try:

        patient_data = request.get_json()

        if not patient_data:
            raise HTTPException(status_code=400, detail=jsonify({"error": "Invalid or missing JSON data"}))

        # generate prompt
        prompt = generate_prompt(patient_data)

        # call openai api
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly, patient-focused medical assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        patient_message = response.choices[0].message.content
        return patient_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    app.run(debug=True)
