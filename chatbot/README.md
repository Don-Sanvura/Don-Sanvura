# Don's Recruiter Chatbot 🤖

An AI-powered chatbot assistant that helps recruiters and professionals learn about Don Sanvura's professional background, technical skills, and completed projects.

## Features

✨ **Smart Conversation**: Natural language processing powered by OpenAI GPT
✅ **Real-time Chat**: Interactive web-based interface with instant responses
📊 **Portfolio Information**: Comprehensive data about skills and projects
🔄 **Conversation Management**: Reset and manage chat history
🌐 **REST API**: Complete API endpoints for integration
📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js (optional, for serving frontend)
- OpenAI API Key

### Installation

1. **Clone and navigate to the chatbot directory**
   ```bash
   git clone https://github.com/Don-Sanvura/Don-Sanvura.git
   cd Don-Sanvura/chatbot
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

5. **Run the Flask server**
   ```bash
   python app.py
   ```
   
   Server will start at `http://localhost:5000`

6. **Open the chatbot**
   - Open `index.html` in your browser, or
   - Use a local server: `python -m http.server 8000` and visit `http://localhost:8000/index.html`

## API Endpoints

### Health Check
```bash
GET /api/health
```
Checks if the bot service is running.

**Response:**
```json
{
  "status": "healthy",
  "botName": "Don's Recruiter Assistant",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Chat
```bash
POST /api/chat
```
Send a message and get a response from the bot.

**Request:**
```json
{
  "message": "What are your main technical skills?"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Don has expertise in multiple areas...",
  "timestamp": "2024-01-15T10:30:00",
  "conversationLength": 2
}
```

### Reset Conversation
```bash
POST /api/reset
```
Clear conversation history.

**Response:**
```json
{
  "success": true,
  "message": "Conversation history reset",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Get Configuration
```bash
GET /api/config
```
Retrieve bot configuration details.

### Get Portfolio Information
```bash
GET /api/portfolio-info
```
Fetch comprehensive portfolio data including skills and projects.

## Configuration

Edit `config.json` to customize:
- Bot name and version
- OpenAI model and settings
- System prompt and behavior

## Example Questions

The chatbot can answer questions like:

- "What are Don's main technical skills?"
- "Tell me about the BC WildWatch project"
- "What experience does Don have with machine learning?"
- "How can I contact Don?"
- "What frontend technologies does Don use?"
- "Describe Don's experience with data engineering"
- "What's Don's focus in AI development?"

## Deployment

### Heroku
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### Docker
```bash
docker build -t recruiter-chatbot .
docker run -e OPENAI_API_KEY=your_key -p 5000:5000 recruiter-chatbot
```

## Troubleshooting

**Bot not responding:**
- Verify OpenAI API key is set correctly
- Check Flask server is running on port 5000
- Check browser console for errors

**CORS errors:**
- Ensure FLASK_ENV is set properly
- Check CORS origins in Flask app configuration

**API errors:**
- Check `.env` file for proper API key
- Verify OpenAI API account is active
- Check network connectivity

## Technologies Used

- **Backend**: Flask, Python
- **AI/ML**: OpenAI GPT API
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: REST
- **Deployment**: Gunicorn, Docker-ready

## License

Free to use and modify for Don Sanvura's portfolio.

## Support

For issues or questions:
- Email: dwagsanvura@gmail.com
- LinkedIn: linkedin.com/in/don-sanvura
- Portfolio: https://don-sanvura.github.io/MrSanvura.github.io/
