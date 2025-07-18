# College Exam Registration System

## Project Structure
```
frontend/       # React.js application
backend/        # Flask API server
```

## Setup
1. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

2. **Backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/students` | POST | Register student |
| `/api/students` | GET | List all students |

## Deployment
1. **Frontend**: [![Vercel](https://vercel.com/button)](https://vercel.com/new)
2. **Backend**: Set MongoDB URI in environment variables
