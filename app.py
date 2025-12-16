import os
import json
import asyncio
import google.generativeai as genai
from google.cloud import secretmanager
from flask import Flask, render_template, jsonify, request
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport

app = Flask(__name__)

# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()

# Build the resource name of the secret version.
name = "projects/396631018769/secrets/optics-app-gemini/versions/latest"

# Access the secret version.
response = client.access_secret_version(request={"name": name})

# Extract the payload.
secret_string = response.payload.data.decode("UTF-8")


genai.configure(api_key=secret_string)

# List of available models
AVAILABLE_MODELS = [
    "gemini-3-pro-preview",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemma-3-27b-it",
    "gpt-oss-120b-maas",
    "meta/llama-4-maverick-17b-128e-instruct-maas"
]

prompt = "Tell me a 2-3 sentence historical joke or fun fact about Tiger Woods. MAXIMUM 2 SENTENCES!"

@app.route('/')
def index():
    return render_template('index.html')

async def fetch_weather():
    async with Client(StreamableHttpTransport(url="http://127.0.0.1:8000/mcp")) as client:
        return await client.call_tool("get_weather", arguments={"location": "San Diego, CA"})

@app.route('/get_air_quality')
def get_air_quality():
    try:
        result = asyncio.run(fetch_weather())
        
        # Check for structured_content first (available in newer FastMCP/MCP versions)
        if hasattr(result, 'structured_content') and result.structured_content:
             return jsonify(result.structured_content)

        # Fallback to parsing text content
        if hasattr(result, 'content') and result.content:
            for content in result.content:
                if content.type == 'text':
                    try:
                        data = json.loads(content.text)
                        return jsonify(data)
                    except json.JSONDecodeError:
                        return jsonify({'result': content.text})
        
        return jsonify({'error': 'No content returned from MCP tool'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_models')
def get_models():
    return jsonify(AVAILABLE_MODELS)

@app.route('/generate_fact')
def generate_fact():
    model_name = request.args.get('model')
    if not model_name:
        return jsonify({'error': 'No model selected'})
    
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return jsonify({'fact': response.text})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
