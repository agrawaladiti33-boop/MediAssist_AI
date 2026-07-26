from google import genai
from google import genai
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from pdf_generators import generate_pdf
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

#Page Configuration 
st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🩺",
    layout="wide"
)

#Load Dataset 
train_df = pd.read_csv("Training.csv")
description_df = pd.read_csv("symptom_Description.csv")
precaution_df = pd.read_csv("symptom_precaution.csv")
home_df = pd.read_csv("home_remedies.csv")
foods_df = pd.read_csv("foods_to_avoid.csv")
medical_df = pd.read_csv("medical_tests.csv")

#Title 
st.title("🩺 MediAssist AI")
st.markdown("""
### AI-Powered Healthcare Diagnosis Assistant

Welcome to **MediAssist AI**.

Select one or more symptoms below and let the AI predict the most likely disease.

⚠️ **This project is for educational purposes only and should not replace professional medical advice.**
""")
st.divider()

#Patient Information
st.header("👤 Patient Information")
add_patient_info = st.checkbox("👤 Add Patient Information (Optional)")
if add_patient_info:
    st.info(
        "The information below is optional. It will only be used in your diagnosis report."
    )
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("👤 Full Name")
        age = st.number_input(
            "🎂 Age",
            min_value=0,
            max_value=120,
            value=20
        )
        gender = st.selectbox(
            "⚧ Gender",
            ["Male", "Female", "Other"]
        )
        weight = st.number_input(
            "⚖ Weight (kg)",
            min_value=1.0,
            max_value=250.0,
            value=60.0
        )
    with col2:
        height = st.number_input(
            "📏 Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=170.0
        )
        blood_group = st.selectbox(
            "🩸 Blood Group",
            [
                "Unknown",
                "A+",
                "A-",
                "B+",
                "B-",
                "AB+",
                "AB-",
                "O+",
                "O-",
            ],
        )
        existing_disease = st.text_input(
            "🩺 Existing Diseases (Optional)"
        )
        allergies = st.text_input(
            "🤧 Known Allergies (Optional)"
        )

    #BMI Calculator

    if height > 0:
        bmi = weight / ((height / 100) ** 2)
        st.subheader("📊 Body Mass Index (BMI)")
        st.metric(
            label="Your BMI",
            value=f"{bmi:.1f}"
        )
        if bmi < 18.5:
            st.warning("⚠ Underweight")
        elif bmi < 25:
            st.success("✅ Normal Weight")
        elif bmi < 30:
            st.warning("🟠 Overweight")
        else:
            st.error("🔴 Obese")
st.divider()

#Train Model 
X = train_df.drop("prognosis", axis=1)
y = train_df["prognosis"]
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

#Sidebar 
st.sidebar.title("🩺 MediAssist AI")
st.sidebar.markdown("---")
st.sidebar.header("📌 Project Information")
st.sidebar.write("""
This application predicts diseases using Machine Learning.
**Technologies Used**
- Python
- Pandas
- Scikit-learn
- Streamlit
- Random Forest
""")
st.sidebar.markdown("---")
st.sidebar.header("📊 Dataset")
st.sidebar.write(f"📁 Records : {train_df.shape[0]}")
st.sidebar.write(f"🩺 Symptoms : {len(X.columns)}")
st.sidebar.write(f"🦠 Diseases : {train_df['prognosis'].nunique()}")
st.sidebar.markdown("---")
st.sidebar.markdown("""
## 👩‍💻 Developer

**Name:** Aditi Agrawal

**Institute:** Inderprastha Engineering College

**Course:** IBM NASSCOM GenAI

**Machine Learning Algorithm:** Random Forest Classifier

**Model Accuracy:** 100%
""")
st.sidebar.markdown("---")
st.sidebar.caption("Version 1.0")
st.sidebar.caption("Last Updated: July 2026")
st.sidebar.caption("Made with ❤️ using Streamlit")

#Symptom Selection 
st.header("🩺 Select Symptoms")

#Get all symptom names (exclude prognosis column)
symptom_list = list(X.columns)

#Convert underscores to spaces for display
display_symptoms = [symptom.replace("_", " ") for symptom in symptom_list]

#User selects symptoms
selected_display = st.multiselect(
    "Choose one or more symptoms:",
    options=display_symptoms
)

#Convert selected symptoms back to original format
selected_symptoms = [symptom.replace(" ", "_") for symptom in selected_display]

#Prediction 
if st.button("🔍 Predict Disease"):
    if len(selected_symptoms) == 0:
        st.warning("Please select at least one symptom.")
        st.stop()

    #Create input vector
    input_data = [0] * len(symptom_list)
    
    #Mark selected symptoms
    for symptom in selected_symptoms:
        if symptom in symptom_list:
            index = symptom_list.index(symptom)
            input_data[index] = 1
        
    #Predict disease
    prediction = model.predict([input_data])
    probabilities = model.predict_proba([input_data])
    confidence = probabilities.max() * 100

    #Convert prediction back to disease name
    predicted_disease = label_encoder.inverse_transform(prediction)[0]
    confidence = round(confidence, 2)
    st.success(f"🩺 Predicted Disease: {predicted_disease}")
    st.progress(confidence / 100)
    st.info(f"🎯 Prediction Confidence: {confidence}%")
    st.divider()
    st.header("📋 Diagnosis Report")
    st.caption("Prediction generated using a trained Random Forest Machine Learning model.")
        
    #Display result
    st.success("✅ Prediction Completed Successfully!")
    st.metric("🎯 Prediction Confidence", f"{confidence:.2f}%")
    st.progress(float(confidence) / 100)   
    st.subheader("🩺 Selected Symptoms")
    st.write(", ".join(selected_symptoms))
    st.markdown("## 🩺 Predicted Disease")
    st.success(predicted_disease)

    #Disease Description 
    description = description_df.loc[
        description_df["Disease"] == predicted_disease,
        "Description"
    ]
    if not description.empty:
        st.info("📖 Disease Description")
        st.write(description.values[0])

    #Precautions 
    precautions = precaution_df.loc[
        precaution_df["Disease"] == predicted_disease
    ]
    if not precautions.empty:
        st.success("💊 Recommended Precautions")
        for i in range(1, 5):
            precaution = precautions[f"Precaution_{i}"].values[0]
            if pd.notna(precaution):
                st.write(f"✔ {precaution}")

    #Recommended Doctor 
    doctor_dict = {
        "Fungal infection": "Dermatologist",
        "Allergy": "Dermatologist",
        "GERD": "Gastroenterologist",
        "Chronic cholestasis": "Hepatologist",
        "Drug Reaction": "General Physician",
        "Peptic ulcer diseae": "Gastroenterologist",
        "Diabetes ": "Endocrinologist",
        "Hypertension ": "Cardiologist",
        "Migraine": "Neurologist",
        "Heart attack": "Cardiologist",
        "Pneumonia": "Pulmonologist",
        "Tuberculosis": "Pulmonologist"
    }
    doctor = doctor_dict.get(predicted_disease, "General Physician")
    st.warning(f"👨‍⚕️ Recommended Doctor: **{doctor}**")
    st.divider()

    #AI Health Explanation
    st.subheader("🤖 AI Health Explanation")
    prompt = f"""
    The user selected these symptoms:
    {', '.join(selected_symptoms)}

    The machine learning model predicted:

    {predicted_disease}

    Provide an educational explanation in simple English.

    Include:
    1. What this disease is.
    2. Why these symptoms may be associated with it.
    3. General lifestyle precautions.
    4. Which medical specialist is appropriate.
    Keep the response under 150 words.

    Do not provide a diagnosis or prescribe medications.
    Clearly state that this is not a substitute for professional medical advice.
    """
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    st.info(response.text)

    #Home Remedies
    home = home_df.loc[
        home_df["Disease"] == predicted_disease
    ]
    if not home.empty:
        st.subheader("🏠 Home Remedies")
        for i in range(1, 5):
            remedy = home[f"Home_Remedy_{i}"].values[0]
            if pd.notna(remedy):
                st.write(f"🏡 {remedy}")

   
    #Foods To Avoid
    foods = foods_df.loc[
        foods_df["Disease"] == predicted_disease
    ]
    if not foods.empty:
        st.subheader("🚫 Foods To Avoid")
        for i in range(1, 5):
            food = foods[f"Food_{i}"].values[0]
            if pd.notna(food):
                st.write(f"❌ {food}")

    #Suggested Medical Tests
    tests = medical_df.loc[
        medical_df["Disease"] == predicted_disease
    ]
    if not tests.empty:
        st.subheader("🧪 Suggested Medical Tests")
        st.info(
            "These are commonly recommended diagnostic tests. "
            "A healthcare professional will decide which tests are appropriate."
        )
        for i in range(1, 5):
            test = tests[f"Test_{i}"].values[0]
            if pd.notna(test):
                st.write(f"🧪 {test}")

    #Download PDF Report
    
    #Convert dataframe rows into lists
    precaution_list = []
    if not precautions.empty:
        for i in range(1, 5):
            value = precautions[f"Precaution_{i}"].values[0]
            if pd.notna(value):
                precaution_list.append(value)
    remedy_list = []
    if not home.empty:
        for i in range(1, 5):
            value = home[f"Home_Remedy_{i}"].values[0]
            if pd.notna(value):
                remedy_list.append(value)
    food_list = []
    if not foods.empty:
        for i in range(1, 5):
            value = foods[f"Food_{i}"].values[0]
            if pd.notna(value):
                food_list.append(value)
    test_list = []
    if not tests.empty:
        for i in range(1, 5):
            value = tests[f"Test_{i}"].values[0]
            if pd.notna(value):
                test_list.append(value)
    pdf = generate_pdf(
    name=patient_name if add_patient_info else "Not Provided",
    age=age if add_patient_info else "Not Provided",
    gender=gender if add_patient_info else "Not Provided",
    disease=predicted_disease,
    doctor=doctor,
    description=description.values[0] if not description.empty else "Not Available",
    precautions=precaution_list,
    remedies=remedy_list,
    foods=food_list,
    tests=test_list,
    symptoms=selected_display,
    confidence=confidence,
    bmi=bmi if add_patient_info else None,
    blood_group=blood_group if add_patient_info else None,
    height=height if add_patient_info else None,
    weight=weight if add_patient_info else None,
    existing_disease=existing_disease if add_patient_info else None,
    allergies=allergies if add_patient_info else None
)
    st.download_button(
        label="📄 Download Diagnosis Report",
        data=pdf,
        file_name="MediAssist_Report.pdf",
        mime="application/pdf"
    )
st.divider()
st.caption("© 2026 MediAssist AI | Developed by Aditi Agrawal | IBM NASSCOM GenAI Project")
