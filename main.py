from contextlib import asynccontextmanager

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# ----------------------------------
# STEP 1: Model files load karna
# ----------------------------------

model = None
best_threshold = None


@asynccontextmanager
async def lifespan(app: FastAPI):

    global model, best_threshold

    model = joblib.load("loan_default_model.pkl")

    best_threshold = float(
        joblib.load("best_threshold.pkl")
    )

    print("Loan Default Model Loaded Successfully!")

    yield


# ----------------------------------
# STEP 2: FastAPI application
# ----------------------------------

app = FastAPI(
    title="Loan Default Prediction API",
    description="Predict loan default probability",
    version="1.0",
    lifespan=lifespan
)


# ----------------------------------
# STEP 3: Input data structure
# ----------------------------------

class LoanInput(BaseModel):

    person_age: int = Field(ge=18, le=100)

    person_income: float = Field(gt=0)

    person_home_ownership: str

    person_emp_length: float | None = Field(
        default=None,
        ge=0
    )

    loan_intent: str

    loan_grade: str

    loan_amnt: float = Field(gt=0)

    loan_int_rate: float | None = Field(
        default=None,
        ge=0
    )

    loan_percent_income: float = Field(ge=0)

    cb_person_default_on_file: str

    cb_person_cred_hist_length: int = Field(ge=0)


# ----------------------------------
# STEP 4: Home route
# ----------------------------------

@app.get("/")
def home():

    return {
        "message": "Loan Default Prediction API is running"
    }


# ----------------------------------
# STEP 5: Prediction endpoint
# ----------------------------------

@app.post("/predict")
def predict_loan(data: LoanInput):

    if model is None or best_threshold is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded"
        )

    try:

        # Input ko dictionary mein convert karna
        input_data = data.model_dump()

        # Dictionary ko DataFrame mein convert karna
        input_df = pd.DataFrame([input_data])

        # Default hone ki probability
        default_probability = float(
            model.predict_proba(input_df)[0, 1]
        )

        # Best threshold apply karna
        prediction = int(
            default_probability >= best_threshold
        )

        # Result banana
        if prediction == 1:

            result = " Loan Default"

        else:

            result = "Loan Not Default"

        return {

            "prediction": prediction,

            "result": result,

            "default_probability": round(
                default_probability, 4
            ),

            "default_probability_percent": round(
                default_probability * 100, 2
            ),

            "threshold": round(
                best_threshold, 4
            )

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )