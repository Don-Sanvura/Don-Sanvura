import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Store conversation history
conversation_history = []

def initialize_system_message():
    """Initialize the system message for the chatbot"""
    return {
        "role": "system",
        "content": config['systemPrompt']
    }

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "botName": config['botName'],
        "version": config['version'],
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare messages for API call
        messages = [initialize_system_message()] + conversation_history[-20:]  # Keep last 20 messages
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=config['model'],
            messages=messages,
            temperature=config['temperature'],
            max_tokens=config['maxTokens']
        )
        
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return jsonify({
            "success": True,
            "message": assistant_message,
            "timestamp": datetime.now().isoformat(),
            "conversationLength": len(conversation_history)
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({
        "success": True,
        "message": "Conversation history reset",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get bot configuration"""
    return jsonify({
        "botName": config['botName'],
        "version": config['version'],
        "description": config['description']
    }), 200

@app.route('/api/portfolio-info', methods=['GET'])
def get_portfolio_info():
    """Get portfolio information"""
    portfolio_data = {
        "name": "Don Sanvura",
        "title": "Software Engineer | Aspiring Digital Assistant | Full-Stack Architect",
        "location": "BC (British Columbia)",
        "website": "https://don-sanvura.github.io/MrSanvura.github.io/",
        "email": "dwagsanvura@gmail.com",
        "linkedIn": "linkedin.com/in/don-sanvura",
        "instagram": "instagram.com/_auradon",
        "skills": {
            "languages": ["Python", "SQL", "JavaScript", "C#", "HTML/CSS"],
            "frontend": ["React", "JavaScript", "HTML/CSS"],
            "backend": ["Node.js", "Express", "Python"],
            "dataScience": ["Scikit-learn", "Pandas", "NumPy", "Seaborn", "Matplotlib"],
            "databases": ["SQL Server", "PostgreSQL", "Data Warehousing"],
            "tools": ["Power BI", "Tableau", "Jupyter", "Git", "CI/CD"]
        },
        "projects": [
            {
                "name": "BC WildWatch: Campus Safety Hub",
                "description": "Real-time campus safety platform for geolocation reporting of animal sightings",
                "technologies": ["React", "Node.js", "Express", "JavaScript"]
            },
            {
                "name": "Advanced Analytics & Data Visualization",
                "description": "Translating multidimensional data into actionable intelligence",
                "technologies": ["Python", "Pandas", "Jupyter", "Tableau", "R"]
            },
            {
                "name": "Sales Forecasting: Predictive Engine",
                "description": "ML pipeline transforming transactional data into time-series demand models",
                "technologies": ["Scikit-Learn", "Linear Regression", "NumPy", "Seaborn"]
            },
            {
                "name": "Comparative Financial Dashboard",
                "description": "BI interface parsing market trends and trading volume data",
                "technologies": ["Power BI", "DAX", "Financial Modeling"]
            },
            {
                "name": "Intelligent Vehicle Pricing Architecture",
                "description": "Deep learning script automating ETL, data sanitization, and model optimization",
                "technologies": ["Neural Networks", "Data Cleansing", "Model Training"]
            },
            {
                "name": "WeatherPredictor: Atmospheric Modeling",
                "description": "ML framework converting atmospheric readings into decision-making endpoints",
                "technologies": ["Scikit-Learn", "Classification", "Matplotlib", "Kaggle Datasets"]
            }
        ]
    }
    return jsonify(portfolio_data), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
