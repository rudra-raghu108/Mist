# ✨ MIST AI - SRM Virtual Assistant

> **Your intelligent guide to SRM University powered by advanced AI**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0+-orange.svg)](https://mongodb.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://typescriptlang.org)

## 🎯 What is MIST AI?

**MIST AI** is an intelligent virtual assistant specifically designed for SRM University students, faculty, and prospective students. It provides instant, accurate answers about admissions, courses, campus life, fees, placements, and everything related to SRM University.

### ✨ Key Features

- **🤖 AI-Powered Responses**: Uses OpenAI GPT-4 for intelligent, contextual answers
- **📚 Comprehensive Knowledge**: Covers all aspects of SRM University
- **🌐 Web Scraping**: Automatically updates knowledge from official SRM websites
- **💬 Real-time Chat**: Interactive chat interface with instant responses
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **🎨 Beautiful UI**: Modern, intuitive interface with dark/light themes
- **🔍 Smart Search**: Find answers quickly with intelligent search
- **📊 Analytics**: Track usage and improve responses over time

## 🚀 Live Demo

**Try it now:** [Coming Soon - Deploy your own instance!]

## 🏗️ Architecture

```
Frontend (React + TypeScript) ←→ Backend (FastAPI + Python) ←→ MongoDB + OpenAI
```

- **Frontend**: Modern React app with TypeScript, Tailwind CSS, and shadcn/ui
- **Backend**: FastAPI server with async MongoDB operations
- **Database**: MongoDB for flexible, scalable data storage
- **AI**: OpenAI GPT-4 for intelligent responses
- **Scraping**: Automated web scraping for up-to-date information

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** - [Download Python](https://python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **MongoDB 7.0+** - [Download MongoDB](https://mongodb.com/try/download/community)
- **Git** - [Download Git](https://git-scm.com/)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/srm-guide-bot.git
cd srm-guide-bot
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements-mongodb.txt

# Copy environment file
copy env-mongodb.txt .env

# Edit .env with your API keys
notepad .env
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd ..

# Install dependencies
npm install
```

### 4. Environment Configuration

Edit the `.env` file in the backend directory:

```env
# Required - Add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Required - Generate a secure JWT secret
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# MongoDB (already configured)
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=srm_guide_bot
```

## 🚀 Quick Start

### 1. Start MongoDB

```bash
# Start MongoDB service (Windows)
net start MongoDB

# Or start manually
mongod
```

### 2. Start Backend

```bash
cd backend
python main.py
```

Your backend will be running at: `http://localhost:8000`

### 3. Start Frontend

```bash
# From project root
npm run dev
# or
yarn dev
```

Your frontend will be running at: `http://localhost:3000`

### 4. Access the Application

Open your browser and go to: `http://localhost:3000`

## 🎓 Training Your AI

### Interactive Training

```bash
cd backend
python train_ai_custom.py
```

**Features:**
- Add custom knowledge manually
- Edit existing knowledge
- View all knowledge items
- Quality validation
- Export training data

### Bulk Import

```bash
cd backend
python bulk_import_knowledge.py
```

**Features:**
- Import sample SRM knowledge (10 Q&A pairs)
- Import from custom JSON files
- Export templates
- Batch processing

### Sample Training Data

```json
{
  "category": "admissions",
  "question": "What are the admission requirements for B.Tech?",
  "answer": "For B.Tech admission, you need: 1) 10+2 with Physics, Chemistry, and Mathematics with minimum 60% aggregate, 2) Valid JEE Main score or SRMJEEE score, 3) Age should be between 17-25 years as of December 31st of the admission year.",
  "tags": ["admissions", "btech", "requirements", "eligibility"],
  "confidence_score": 0.95
}
```

## 📁 Project Structure

```
srm-guide-bot/
├── backend/                 # Python FastAPI backend
│   ├── app/                # Application code
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core configuration
│   │   ├── models/        # Database models
│   │   ├── services/      # Business logic
│   │   └── schemas/       # Data validation
│   ├── requirements-mongodb.txt  # Python dependencies
│   ├── env-mongodb.txt    # Environment template
│   ├── main.py            # Application entry point
│   └── setup-mongodb.ps1  # MongoDB setup script
├── src/                    # React frontend
│   ├── components/        # React components
│   ├── pages/            # Page components
│   ├── hooks/            # Custom React hooks
│   └── lib/              # Utility functions
├── public/                # Static assets
├── package.json           # Node.js dependencies
└── README.md              # This file
```

## 🔧 Configuration

### Backend Configuration

The backend uses environment variables for configuration. Key settings:

- **Database**: MongoDB connection and settings
- **AI**: OpenAI API key and model configuration
- **Security**: JWT secrets and authentication
- **Scraping**: Website URLs and scraping settings

### Frontend Configuration

The frontend is configured through:

- **Environment Variables**: API endpoints and configuration
- **Tailwind CSS**: Styling and theming
- **shadcn/ui**: Component library configuration

## 🌐 API Endpoints

### Core Endpoints

- `POST /api/chat` - Send message and get AI response
- `GET /api/chat/history` - Get chat history
- `POST /api/scraping/start` - Start web scraping
- `GET /api/analytics` - Get usage analytics

### AI Training Endpoints

- `POST /api/ai-training/knowledge` - Add custom knowledge
- `GET /api/ai-training/dataset` - Get training dataset
- `PUT /api/ai-training/knowledge/{id}` - Update knowledge
- `DELETE /api/ai-training/knowledge/{id}` - Delete knowledge

## 🎨 Customization

### Adding New Categories

1. **Backend**: Add new category to knowledge database
2. **Frontend**: Update UI components and navigation
3. **Training**: Add sample Q&A pairs for the category

### Custom Knowledge

```python
# Add custom knowledge programmatically
await trainer.add_custom_knowledge(
    category="new_category",
    question="Your question?",
    answer="Your detailed answer",
    tags=["tag1", "tag2"]
)
```

### UI Theming

The frontend uses Tailwind CSS with custom CSS variables for theming:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
}
```

## 🚀 Deployment

### Backend Deployment

```bash
# Using Docker
docker build -t mist-ai-backend .
docker run -p 8000:8000 mist-ai-backend

# Using Python directly
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment

```bash
# Build for production
npm run build

# Deploy to Vercel, Netlify, or any static hosting
```

### Environment Variables for Production

```env
NODE_ENV=production
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
OPENAI_API_KEY=your-production-openai-key
JWT_SECRET=your-production-jwt-secret
```

## 🧪 Testing

### Backend Testing

```bash
cd backend
pytest
```

### Frontend Testing

```bash
npm test
```

## 📊 Monitoring & Analytics

The application includes built-in monitoring:

- **Performance Metrics**: Response times, error rates
- **Usage Analytics**: Popular questions, user behavior
- **AI Performance**: Response quality, confidence scores
- **System Health**: Database status, API health

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow the existing code style
- Add tests for new features
- Update documentation
- Ensure all tests pass

## 🐛 Troubleshooting

### Common Issues

#### MongoDB Connection Failed
```bash
# Check if MongoDB is running
net start MongoDB

# Test connection
mongosh
use srm_guide_bot
db.admin.command('ping')
```

#### OpenAI API Errors
```bash
# Check your API key
echo $OPENAI_API_KEY

# Verify in .env file
cat .env | grep OPENAI_API_KEY
```

#### Frontend Build Errors
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Getting Help

- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Documentation**: Check this README and code comments

## 📚 Learning Resources

- **FastAPI**: [Official Documentation](https://fastapi.tiangolo.com/)
- **React**: [Official Documentation](https://reactjs.org/docs/)
- **MongoDB**: [Official Documentation](https://docs.mongodb.com/)
- **OpenAI**: [API Documentation](https://platform.openai.com/docs/)
- **Tailwind CSS**: [Official Documentation](https://tailwindcss.com/docs/)

## 🎉 Acknowledgments

- **SRM University** for inspiration
- **OpenAI** for powerful AI capabilities
- **FastAPI** team for excellent backend framework
- **React** team for amazing frontend library
- **MongoDB** for flexible database solution

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Project Link**: [https://github.com/yourusername/srm-guide-bot](https://github.com/yourusername/srm-guide-bot)
- **Issues**: [GitHub Issues](https://github.com/yourusername/srm-guide-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/srm-guide-bot/discussions)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/srm-guide-bot&type=Date)](https://star-history.com/#yourusername/srm-guide-bot&Date)

---

**Made with ❤️ for the SRM Community**

*If you find this project helpful, please give it a ⭐ star!*

