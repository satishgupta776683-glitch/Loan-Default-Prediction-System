🏦 Loan Default Prediction System

An end-to-end Machine Learning web application that estimates the probability of loan default from applicant and loan details. It uses a trained Scikit-learn model, a FastAPI backend, and a Streamlit interface.

Disclaimer: This project is for educational and demonstration purposes only. Its predictions should not be the sole basis for real lending decisions.

✨ Features
Classifies an application as Default or No Default.

Displays estimated default probability and the decision threshold.

Loads a trained model and selected threshold from .pkl files.

Provides a FastAPI REST API for predictions.

Provides a Streamlit interface for entering applicant and loan details.

Includes an API health check in the Streamlit sidebar.

🧰 Tech Stack
Python

Pandas and NumPy

Scikit-learn

Joblib

FastAPI and Uvicorn

Requests

Streamlit

Render (deployment)

🗂️ Project Structure
Loan-Default-Prediction-System/
├── main.py                     # FastAPI backend
├── app.py                      # Streamlit frontend
├── requirements.txt            # Python dependencies
├── loan_default_model.pkl      # Trained ML model
└── best_threshold.pkl          # Selected decision threshold
Keep any additional deployment files (for example, runtime.txt) if your Render setup uses them.

⚙️ Model Inputs
The application collects these fields:

Field	Description
person_age	Applicant age
person_income	Annual income
person_home_ownership	Home ownership category
person_emp_length	Employment length in years
loan_intent	Purpose of the loan
loan_grade	Loan grade
loan_amnt	Requested loan amount
loan_int_rate	Loan interest rate
loan_percent_income	Loan amount divided by annual income
cb_person_default_on_file	Previous default record indicator
cb_person_cred_hist_length	Credit history length in years
The categories offered in the interface should match those used to train the model.

🚦 Prediction Interpretation
0 means No Default.

1 means Default.

The decision threshold is loaded from best_threshold.pkl.

The application classifies a case as Default when the estimated default probability is greater than or equal to the threshold.

The probability is a model estimate, not a guarantee of a future outcome.

💻 Run Locally
1. Clone the repository
git clone https://github.com/satishgupta776683-glitch/Loan-Default-Prediction-System.git
cd Loan-Default-Prediction-System
2. Create and activate a virtual environment
Windows PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1
If PowerShell blocks activation, use Command Prompt:

venv\Scripts\activate.bat
3. Install dependencies
Make sure the dependency file is named exactly requirements.txt.

python -m pip install -r requirements.txt
Recommended dependency list (keep versions consistent with the environment used to train and save the model):

fastapi
uvicorn
pandas
numpy
scikit-learn==1.6.1
joblib
requests
streamlit
4. Start the FastAPI backend
In the project directory, run:

python -m uvicorn main:app --reload
The local API base URL is http://127.0.0.1:8000, and interactive documentation is available at http://127.0.0.1:8000/docs.

Keep this terminal running.

5. Start the Streamlit frontend
Open a second terminal in the project directory, activate the virtual environment, and run:

python -m streamlit run app.py
Open the local URL shown in the terminal (usually http://localhost:8501).

6. Configure the API URL
For local development, app.py can use:

API_URL = "http://127.0.0.1:8000"
For deployment, change it to your actual public FastAPI backend URL, without a trailing slash:

API_URL = "https://your-backend-name.onrender.com"
Replace the example URL with your deployed backend URL.

☁️ Deploy on Render
Deploy the FastAPI backend and Streamlit frontend as separate web services.

FastAPI backend
Build Command

pip install -r requirements.txt
Start Command

uvicorn main:app --host 0.0.0.0 --port $PORT
Streamlit frontend
Build Command

pip install -r requirements.txt
Start Command

streamlit run app.py --server.port $PORT --server.address 0.0.0.0
Configure the frontend's API_URL to point to the actual FastAPI backend URL. Alternatively, define an API_URL environment variable in the frontend service and read it in app.py using os.getenv.

For compatibility with the saved model, this project specifies scikit-learn==1.6.1. Keep the dependency aligned with the version used to save the model unless the model is retrained and re-exported.

🔌 API Endpoints
The backend is expected to expose:

GET / — root/health response.

POST /predict — receives applicant details and returns a prediction.

The exact request and response schema is defined in main.py. You can test the API at /docs on your running backend.

🛠️ Troubleshooting
requirements.txt not found: Check the spelling, ensure the file is committed and pushed to GitHub, and confirm Render's Root Directory points to the folder containing it.

Streamlit cannot connect to the API: Confirm the backend is deployed and healthy, and use its public Render URL instead of 127.0.0.1.

Model loading error: Ensure both .pkl files are included in the backend deployment and that the Scikit-learn version matches the version used to save the model.

Validation error: Check that request field names and data types match the input schema in main.py.

🔒 Responsible Use
Loan default prediction can affect access to financial services. Real-world use requires rigorous testing, fairness evaluation, privacy safeguards, and compliance with applicable laws and regulations.

👤 Author
Satish Gupta

📄 License
No license has been specified. Add a LICENSE file if you intend to publish this project for reuse.


<img width="714" height="723" alt="image" src="https://github.com/user-attachments/assets/a2fdb9e9-13ce-4b8e-b154-fbe272f0b6d6" />
<img width="736" height="456" alt="image" src="https://github.com/user-attachments/assets/4eb11ad2-fa73-4b72-928d-0de4cd7f0de2" />

Loan Default Prediction System | Python, Scikit-learn, FastAPI, Streamlit



Developed an end-to-end Machine Learning application to predict loan default risk using a trained classification model. Built a REST API using FastAPI and an interactive web interface using Streamlit. Implemented probability-based predictions with an optimized decision threshold and deployed the application on Render.


