# Email Guardian

Email Guardian is a machine learning-powered application for classifying emails (e.g., spam, phishing, safe) and retraining the model with new data. It features a FastAPI backend and a React frontend.

## Features
- Classify email text or files as spam, phishing, or safe
- Retrain the model with new labeled data
- REST API endpoints for integration
- User-friendly React frontend

## Project Structure
```
Email_Guardian/
  backend_model.py         # ML model logic (predict, retrain)
  main.py                 # FastAPI backend
  frontend/               # React frontend
  data/                   # Training data
  email_guardian_data.csv # Main dataset
  models/                 # Saved models
```

## Backend Setup (FastAPI)
1. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```sh
   pip install fastapi uvicorn pandas scikit-learn
   ```
3. Run the backend server:
   ```sh
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

## Frontend Setup (React)
1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the React development server:
   ```sh
   npm start
   ```
   The app will be available at `http://localhost:3000`.

## API Endpoints
- `POST /classify` — Classify email text
- `POST /classify_file` — Classify email from uploaded file
- `POST /retrain` — Retrain model with new data

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is open source and available under the [MIT License](LICENSE). 