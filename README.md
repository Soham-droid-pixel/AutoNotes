# AutoNotes 2.0 🚀

An AI-powered text summarization and topic extraction tool built with React, Node.js, and Python machine learning. Transform long texts into concise summaries and extract key topics instantly.

![AutoNotes Demo](https://img.shields.io/badge/Status-Active-brightgreen)
![React](https://img.shields.io/badge/React-18.0+-blue)
![Node.js](https://img.shields.io/badge/Node.js-16.0+-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![License](https://img.shields.io/badge/License-MIT-red)

## ✨ Features

- **Smart Summarization**: Generate concise 3-sentence summaries from lengthy texts
- **Topic Extraction**: Automatically identify and extract key topics and keywords
- **Real-time Processing**: Fast AI-powered analysis with instant results
- **Modern UI**: Beautiful, responsive interface built with Tailwind CSS
- **Multi-format Support**: Works with articles, lecture notes, transcripts, and more
- **Microservice Architecture**: Scalable backend with separate ML service

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests

### Backend
- **Node.js** - Server runtime
- **Express.js** - Web application framework
- **Flask** - Python microservice for ML operations
- **CORS** - Cross-origin resource sharing

### Machine Learning
- **NLTK** - Natural language processing
- **Sumy** - Text summarization library
- **Scikit-learn** - Machine learning algorithms
- **NumPy** - Numerical computing

## 🚀 Quick Start

### Prerequisites
- Node.js 16.0 or higher
- Python 3.8 or higher
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AutoNotes2.0.git
   cd AutoNotes2.0
   ```

2. **Set up the Flask ML Service**
   ```bash
   cd flask_ml
   pip install -r requirements.txt
   python app.py
   ```
   The ML service will run on `http://localhost:5001`

3. **Set up the Node.js Backend**
   ```bash
   cd server
   npm install
   node server.js
   ```
   The backend will run on `http://localhost:5000`

4. **Set up the React Frontend**
   ```bash
   cd frontend/my-project
   npm install
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`

### Environment Variables

Create a `.env` file in the `server` directory:

```env
PORT=5000
FLASK_ML_URL=http://localhost:5001
```

## 📁 Project Structure

```
AutoNotes2.0/
├── frontend/
│   └── my-project/
│       ├── src/
│       │   ├── App.jsx
│       │   └── main.jsx
│       ├── index.html
│       ├── package.json
│       ├── tailwind.config.js
│       └── vite.config.js
├── server/
│   ├── server.js
│   ├── package.json
│   └── .env
├── flask_ml/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## 🔧 Usage

1. **Start all services** (Flask ML, Node.js backend, React frontend)
2. **Open your browser** to `http://localhost:5173`
3. **Paste your text** into the input field (minimum 50 characters)
4. **Click "Summarize & Extract Topics"**
5. **View results** - get a concise summary and key topics

### Example Input
```
Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models that computer systems use to perform tasks without explicit instructions. It relies on patterns and inference instead. Machine learning algorithms build a model based on sample data, known as training data, to make predictions or decisions without being explicitly programmed to do so.
```

### Example Output
- **Summary**: Machine learning is a subset of artificial intelligence focusing on algorithms that enable computers to perform tasks without explicit programming. It uses patterns and inference from training data to build models. These models can then make predictions or decisions autonomously.
- **Topics**: `machine learning`, `artificial intelligence`, `algorithms`, `training data`, `predictions`

## 🌐 API Endpoints

### Backend (Node.js)
- `GET /health` - Health check
- `POST /api/summarize` - Main summarization endpoint
- `GET /api/ml-health` - ML service health check

### ML Service (Flask)
- `GET /health` - Health check
- `POST /summarize` - Text processing endpoint

## 🔍 How It Works

1. **Text Input**: User submits text through the React frontend
2. **Validation**: Node.js backend validates input (length, format, etc.)
3. **ML Processing**: Request forwarded to Flask ML service
4. **NLP Analysis**: 
   - Text cleaning and preprocessing
   - LSA (Latent Semantic Analysis) for summarization
   - TF-IDF and NMF for topic extraction
5. **Response**: Summary and topics returned to frontend

## 🛡️ Error Handling

- **Input validation** for text length and format
- **Service availability** checks
- **Graceful degradation** with fallback mechanisms
- **Comprehensive error messages** for debugging

## 🔄 Development

### Running in Development Mode

1. **Flask ML Service** (Terminal 1):
   ```bash
   cd flask_ml
   python app.py
   ```

2. **Node.js Backend** (Terminal 2):
   ```bash
   cd server
   npm run dev  # or nodemon server.js
   ```

3. **React Frontend** (Terminal 3):
   ```bash
   cd frontend/my-project
   npm run dev
   ```

### Building for Production

```bash
# Build frontend
cd frontend/my-project
npm run build

# The backend and ML service can be deployed as-is
```

## 📦 Dependencies

### Frontend Dependencies
```json
{
  "react": "^18.0.0",
  "axios": "^1.0.0",
  "tailwindcss": "^3.0.0",
  "vite": "^4.0.0"
}
```

### Backend Dependencies
```json
{
  "express": "^4.18.0",
  "cors": "^2.8.5",
  "axios": "^1.0.0",
  "dotenv": "^16.0.0"
}
```

### ML Service Dependencies
```txt
flask==3.1.1
flask-cors==6.0.1
sumy==0.11.0
scikit-learn==1.7.0
nltk==3.9.1
numpy==2.3.1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NLTK** for natural language processing capabilities
- **Sumy** for text summarization algorithms
- **Scikit-learn** for machine learning tools
- **React** and **Tailwind CSS** for the beautiful UI
- **Flask** and **Express.js** for robust backend services

## 📧 Contact

Your Name - [@yourusername](https://github.com/Soham-droid-pixel)

Project Link: [https://github.com/yourusername/AutoNotes2.0](https://github.com/Soham-droid-pixel/AutoNotes)

---

⭐ **Star this repository if you found it helpful!** ⭐
