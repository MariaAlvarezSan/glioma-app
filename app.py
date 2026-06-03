# LIBRERÍAS NECESARIAS PARA HACER LA APP
import streamlit as st
import pandas as pd
import joblib

# TÍTULO
st.title("Glioma Grade Prediction App")

st.write(
    """
    This application is for educational and research purposes only.
    It is not intended for real clinical use or medical decision-making.
    """
)

# CONTROL DE ERRORES AL CARGAR EL MODELO
model_option = st.selectbox("Select prediction model", ["clinical_only", "clinical_molecular_top_genes", "clinical_molecular_selected_genes"])

try:
 if model_option == "clinical_only": 
  model = joblib.load("clinical_only_model.pkl")
  
 elif model_option == "clinical_molecular_top_genes":
  model = joblib.load("clinical_molecular_top_genes_model.pkl")
 
 elif model_option == "clinical_molecular_selected_genes":
  model = joblib.load("clinical_molecular_selected_genes_model.pkl")

except FileNotFoundError:
    st.error("Model file not found. Please check that the .pkl files exist.")
    st.stop()

# VARIABLES CLÍNICAS
# Edad del paciente
age = st.number_input(
 "Age at diagnosis", 
 min_value = 1, 
 max_value = 100,
 value = 50
)

st.caption("Expected age range based on training data: approximately 14–87 years.")

if age < 14 or age > 87:
    st.warning("The entered age is outside the typical range observed in the training dataset.")

# 1. Gender
gender_word = st.selectbox("Gender", ["Male", "Female"])
# 0 = hombre, 1 = mujer
gender_num = 1 if gender_word == "Female" else 0

# 2. Race
race_word = st.selectbox("Race", ["White", "Black", "Asian", "Other"])
# 0 = White, 1 = Black, 2 = Asian, 3 = Other
race_dict = {"White": 0, "Black": 1, "Asian": 2, "Other": 3}
race_num = race_dict[race_word]


# FEATURES SEGÚN EL MODELO

# 1. Solo clínico
if model_option == "clinical_only": 
 features = {
  "Age_at_diagnosis": age, 
  "Gender": gender_num,
  "Race": race_num
 }

# 2. 3 genes + clínico
elif model_option == "clinical_molecular_top_genes": 
 idh1 = st.selectbox("IDH1 mutation", ["No", "Yes"])
 tp53 = st.selectbox("TP53 mutation", ["No", "Yes"])
 atrx = st.selectbox("ATRX mutation", ["No", "Yes"])
 features = {
  "IDH1": 1 if idh1 == "Yes" else 0,
  "TP53": 1 if tp53 == "Yes" else 0,
  "ATRX": 1 if atrx == "Yes" else 0,
  "Age_at_diagnosis": age,
  "Gender": gender_num,
  "Race": race_num
 }

# 3. 5 genes + clínico
elif model_option == "clinical_molecular_selected_genes":
 idh1 = st.selectbox("IDH1 mutation", ["No", "Yes"])
 tp53 = st.selectbox("TP53 mutation", ["No", "Yes"])
 atrx = st.selectbox("ATRX mutation", ["No", "Yes"])
 pten = st.selectbox("PTEN mutation", ["No", "Yes"]) 
 egfr = st.selectbox("EGFR mutation", ["No", "Yes"])
 features = {
  "IDH1": 1 if idh1 == "Yes" else 0,
  "TP53": 1 if tp53 == "Yes" else 0,
  "ATRX": 1 if atrx == "Yes" else 0,
  "PTEN": 1 if pten == "Yes" else 0,
  "EGFR": 1 if egfr == "Yes" else 0,
  "Age_at_diagnosis": age,
  "Gender": gender_num,
  "Race": race_num
 }

# DATAFRAME
input_data = pd.DataFrame([features])

# PREDICCIÓN
if st.button("Predict Glioma Grade"): 
 prediction = model.predict(input_data)[0]
 prob_lgg = model.predict_proba(input_data)[0][0]
 prob_gbm = model.predict_proba(input_data)[0][1] 
 if prediction == 0:
  st.success("Predicted class: LGG")
 else: 
  st.error("Predicted class: GBM")
  
 # Mostrar las probabilidades estimadas para cada clase del gliomas
 st.metric(label = "Probability of LGG", value = f"{prob_lgg:.1%}")
 st.metric(label = "Probability of GBM", value = f"{prob_gbm:.1%}")

 # Nivel de confianza
 confidence = max(prob_lgg, prob_gbm)
 
 if confidence > 0.85:
     st.success("High confidence prediction")
 
 elif confidence >= 0.65:
     st.info("Moderate confidence prediction")
 
 else:
     st.warning("Uncertain prediction")
 