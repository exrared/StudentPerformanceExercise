
import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Student Performance Prediction",
    page_icon="🎓",
    layout="centered"
)

API_URL = "http://127.0.0.1:5000/predict"

# Dashboard heading
st.title("🎓 Student Performance Prediction")
st.write(
    "Enter the student's information below "
    "to predict their academic performance."
)

st.divider()

# Student input form
with st.form("prediction_form"):
    st.subheader("Student Information")

    study_hours = st.number_input(
        "Study Hours per Day",
        min_value=0.0,
        max_value=24.0,
        value=5.0,
        step=0.5
    )

    attendance = st.number_input(
        "Attendance Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=90.0,
        step=1.0
    )

    submitted = st.form_submit_button(
        "Predict Student Performance",
        use_container_width=True
    )

# Send inputs to Flask API
if submitted:
    payload = {
        "study_hours": study_hours,
        "attendance_percentage": attendance
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=10
        )

        if response.ok:
            result = response.json()

            st.subheader("Prediction Result")

            if result["prediction"] == "Pass":
                st.success("Prediction: PASS")
            else:
                st.error("Prediction: FAIL")

            col1, col2 = st.columns(2)

            col1.metric(
                "Study Hours",
                f'{result["study_hours"]:.1f} hours'
            )

            col2.metric(
                "Attendance",
                f'{result["attendance_percentage"]:.1f}%'
            )

            st.info(result.get("note", ""))

        else:
            try:
                error_message = response.json().get(
                    "error", "The API returned an error."
                )
            except ValueError:
                error_message = "The API returned an unexpected response."

            st.error(f"Prediction failed: {error_message}")

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to the Flask API. "
            "Please make sure app.py is running on port 5000."
        )

    except requests.exceptions.Timeout:
        st.error("The API took too long to respond. Please try again.")

    except requests.exceptions.RequestException as exc:
        st.error(f"Request failed: {exc}")

st.divider()

st.caption(
    "Note: Predictions are based on study hours only. "
    "Attendance does not currently affect the trained model."
)
