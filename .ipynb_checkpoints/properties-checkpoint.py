import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


with open('DecisionTreeRegressor.pkl', 'rb') as file:
    pipeline = pickle.load(file)



st.title("Properties Monthly Rent Prediction")

selected_property_type = st.selectbox("Property Type", options=['Service Residence', 'Apartment', 'Condominium', 'Studio', 'Townhouse Condo', 'Flat', 'Duplex', 'Others'])
selected_rooms = st.number_input("Rooms", value=3.0, min_value=1.0, max_value=10.0)
selected_parking = st.number_input("Parking", value=1.0, min_value=0.0, max_value=10.0)
selected_bathroom = st.number_input("Bathroom", value=1.0, min_value=1.0, max_value=8.0)
selected_size = st.number_input("Size", value=100.0, min_value=50.0, max_value=10000.0)
selected_region = st.selectbox("Region", options=['Kuala Lumpur','Selangor'])

gymnasium = st.selectbox("Gymnasium", options=["Yes", "No"])
lift = st.selectbox("Lift", options=["Yes", "No"])
minimart = st.selectbox("Minimart", options=["Yes", "No"])
sauna = st.selectbox("Sauna", options=["Yes", "No"])
security = st.selectbox("Security", options=["Yes", "No"])
swimming_pool = st.selectbox("Swimming Pool", options=["Yes", "No"])

input_data = {
    'property_type': selected_property_type,
    'rooms': selected_rooms,
    'parking': selected_parking,
    'bathroom': selected_bathroom,
    'size': selected_size,
    'region': selected_region,
    'Gymnasium': 1 if gymnasium == "Yes" else 0,
    'Lift': 1 if lift == "Yes" else 0,
    'Minimart': 1 if minimart == "Yes" else 0,
    'Sauna': 1 if sauna == "Yes" else 0,
    'Security': 1 if security == "Yes" else 0,
    'Swimming Pool': 1 if swimming_pool == "Yes" else 0
}

input_df = pd.DataFrame([input_data])
# Make prediction
prediction = pipeline.predict(input_df)*(4500- 200)+200
# Display prediction

st.header(f"Predicted Monthly Rent (RM): {prediction[0]:,.2f}")





