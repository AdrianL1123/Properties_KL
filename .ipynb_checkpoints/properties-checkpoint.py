import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


with open('GradientBoostingRegressor.pkl', 'rb') as file:
    pipeline = pickle.load(file)

st.title("Properties Monthly Rent Prediction")

scaler = StandardScaler()
scaler2 = MinMaxScaler()


property_type_mapping = {
    0: "Apartment",
    1: "Terraced House",
    2: "Semi-Detached House",
    3: "Bungalow",
    4: "Condominium"
}

yes_no_mapping = {
    "Yes": 1,
    "No": 0
}
region_mapping = {
    "Selangor": 0,
    "Kuala Lumpur": 1,
}

selected_property_type = st.selectbox("Property Type", options=list(property_type_mapping.values()))

selected_property_number = list(property_type_mapping.keys())[list(property_type_mapping.values()).index(selected_property_type)]

club_house = yes_no_mapping[st.selectbox("Club House", options=["Yes", "No"])]
gymnasium = yes_no_mapping[st.selectbox("Gymnasium", options=["Yes", "No"])]
jogging_track = yes_no_mapping[st.selectbox("Jogging Track", options=["Yes", "No"])]
lift = yes_no_mapping[st.selectbox("Lift", options=["Yes", "No"])]
minimart = yes_no_mapping[st.selectbox("Minimart", options=["Yes", "No"])]
multipurpose_hall = yes_no_mapping[st.selectbox("Multipurpose hall", options=["Yes", "No"])]
playground = yes_no_mapping[st.selectbox("Playground", options=["Yes", "No"])]
sauna = yes_no_mapping[st.selectbox("Sauna", options=["Yes", "No"])]
security = yes_no_mapping[st.selectbox("Security", options=["Yes", "No"])]
squash_court = yes_no_mapping[st.selectbox("Squash Court", options=["Yes", "No"])]
swimming_pool = yes_no_mapping[st.selectbox("Swimming Pool", options=["Yes", "No"])]
tennis_court = yes_no_mapping[st.selectbox("Tennis Court", options=["Yes", "No"])]
region = region_mapping[st.selectbox("Region", options=['Selangor', 'Kuala Lumpur'])]
input_data = {
    'Property Type': selected_property_number,
    'Rooms': st.number_input("Rooms", value=7.0, min_value=1.0, max_value=10.0),
    'Parking': st.number_input("Parking", value=2.0, min_value=1.0, max_value=10.0),
    'Bathroom': st.number_input("Bathroom", value=1.0, min_value=1.0, max_value=8.0),
    'Region': region,
    'Size': st.number_input("Size", value=100.0 , min_value=50.0, max_value=10000.0),
    'Club House': club_house,
    'Gymnasium': gymnasium,
    'Jogging Track': jogging_track,
    'Lift': lift,
    'Minimart': minimart,
    'Multipurpose hall': multipurpose_hall,
    'Playground': playground,
    'Sauna': sauna,
    'Security': security,
    'Squash Court': squash_court,
    'Swimming Pool': swimming_pool,
    'Tennis Court': tennis_court,
}

input_df = pd.DataFrame([input_data])
prediction = pipeline.predict(input_df)
# reshaped_prediction = prediction.reshape(-1, 1)
# fitted_prediction = scaler2.fit(reshaped_prediction)
# real_prediction = scaler2.inverse_transform(fitted_prediction).reshape(-1, 1)
# if st.button("Predict Rent"):
#     prediction = pipeline.predict(input_df)
#     st.write("The predicted monthly rent is: ", prediction)

# results = prediction[0] * (45000.0 - 100.0) + 100.0

# st.header(f"Predicted Monthly Rent (RM): {predictionzzz}")

st.header(f"Predicted Monthly Rent (RM): {prediction[0]}")

