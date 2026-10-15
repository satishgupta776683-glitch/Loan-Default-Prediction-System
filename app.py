import requests
import streamlit as st

# ----------------------------------
# Config
# ----------------------------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Loan Default Prediction",
    page_icon="🏦",
    layout="centered",
)

st.title("🏦 Loan Default Prediction")
st.caption("Fill in the applicant details to estimate the probability of loan default.")

# Sidebar: API settings + health check
with st.sidebar:
    st.header("⚙️ Settings")
    api_url = st.text_input("API URL", value=API_URL)

    if st.button("Check API status"):
        try:
            r = requests.get(f"{api_url}/", timeout=5)
            if r.status_code == 200:
                st.success(r.json().get("message", "API is running"))
            else:
                st.error(f"API returned status {r.status_code}")
        except requests.exceptions.RequestException:
            st.error("Cannot reach the API. Is FastAPI running?")

# ----------------------------------
# Input form
# ----------------------------------
with st.form("loan_form"):

    st.subheader("👤 Applicant Information")
    col1, col2 = st.columns(2)

    with col1:
        person_age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
        person_income = st.number_input("Annual Income", min_value=1.0, value=50000.0, step=1000.0)
        person_home_ownership = st.selectbox(
            "Home Ownership", ["RENT", "OWN", "MORTGAGE", "OTHER"]
        )

    with col2:
        cb_person_cred_hist_length = st.number_input(
            "Credit History Length (years)", min_value=0, value=5, step=1
        )
        cb_person_default_on_file = st.selectbox(
            "Previous Default on File?", ["N", "Y"],
            format_func=lambda x: "Yes" if x == "Y" else "No",
        )
        emp_known = st.checkbox("Employment length known", value=True)
        person_emp_length = st.number_input(
            "Employment Length (years)", min_value=0.0, value=3.0, step=0.5,
            disabled=not emp_known,
        )

    st.subheader("💰 Loan Information")
    col3, col4 = st.columns(2)

    with col3:
        loan_intent = st.selectbox(
            "Loan Purpose",
            ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"],
        )
        loan_grade = st.selectbox("Loan Grade", ["A", "B", "C", "D", "E", "F", "G"])
        loan_amnt = st.number_input("Loan Amount", min_value=1.0, value=10000.0, step=500.0)

    with col4:
        rate_known = st.checkbox("Interest rate known", value=True)
        loan_int_rate = st.number_input(
            "Interest Rate (%)", min_value=0.0, value=11.0, step=0.1,
            disabled=not rate_known,
        )
        # Auto-calculated, shown for reference
        loan_percent_income = loan_amnt / person_income if person_income > 0 else 0.0
        st.number_input(
            "Loan % of Income (auto)", value=round(loan_percent_income, 4),
            disabled=True, format="%.4f",
        )

    submitted = st.form_submit_button("🔍 Predict", use_container_width=True)

# ----------------------------------
# Call API & show result
# ----------------------------------
if submitted:
    payload = {
        "person_age": int(person_age),
        "person_income": float(person_income),
        "person_home_ownership": person_home_ownership,
        "person_emp_length": float(person_emp_length) if emp_known else None,
        "loan_intent": loan_intent,
        "loan_grade": loan_grade,
        "loan_amnt": float(loan_amnt),
        "loan_int_rate": float(loan_int_rate) if rate_known else None,
        "loan_percent_income": float(loan_percent_income),
        "cb_person_default_on_file": cb_person_default_on_file,
        "cb_person_cred_hist_length": int(cb_person_cred_hist_length),
    }

    try:
        with st.spinner("Predicting..."):
            response = requests.post(f"{api_url}/predict", json=payload, timeout=15)

        if response.status_code == 200:
            res = response.json()
            prob = res["default_probability"]
            prob_pct = res["default_probability_percent"]

            st.divider()
            st.subheader("📊 Result")

            if res["prediction"] == 1:
                st.error(f"⚠️ {res['result'].strip()} (High Risk)")
            else:
                st.success(f"✅ {res['result'].strip()} (Low Risk)")

            m1, m2 = st.columns(2)
            m1.metric("Default Probability", f"{prob_pct}%")
            m2.metric("Decision Threshold", f"{res['threshold'] * 100:.2f}%")

            st.progress(min(max(prob, 0.0), 1.0))
            st.caption(
                "A loan is flagged as default when the probability is "
                "greater than or equal to the threshold."
            )

            with st.expander("View request / response JSON"):
                st.json({"request": payload, "response": res})

        elif response.status_code == 422:
            st.error("Validation error: please check your inputs.")
            st.json(response.json())
        else:
            st.error(f"API error ({response.status_code}): {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the API. Make sure FastAPI is running.")
    except requests.exceptions.Timeout:
        st.error("⏱️ The request timed out. Please try again.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")