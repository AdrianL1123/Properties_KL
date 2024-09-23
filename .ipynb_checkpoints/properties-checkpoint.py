import streamlit as st
import pickle
import pandas as pd
import io
import plotly.express as px

def intro():
    st.title("Analyzing Monthly Rent Trends in KL and Selangor")
    st.subheader('By AdrianL.')
    st.image("empty_wallet.jpeg")

def problemStatement():
    st.title('Problem Statement')
    st.subheader('Why?')
    st.write('Since many people are working with limited budgets, finding great value properties in KL/Selangor is essential for affordable rentals.')
    st.subheader('Context')
    st.write("Selangor's property market is diverse, with varying price             points, locations, and features.")
    st.subheader('Issue')
    st.write('Struggle to identify properties that balance affordability with long-term satisfaction.')
    st.subheader('Impact')
    st.write('This difficulty can lead people to make poor financial and regrettable choices')
    st.subheader('Vision')
    st.write('Let people make good decisions when choosing a property to rent with no regrets.')
   
def dataset():
    st.header('Dataset Before:')
    df2 = pd.read_csv("mudah-apartment-kl-selangor.csv")  
    st.write(df2) 

    st.header('Dataset After:')
    df = pd.read_csv("featured_data.csv")  
    st.write(df) 
    
    st.subheader("Description of dataset:")
    st.write(df.describe())
    
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.subheader("Each Columns's Type:")
    st.text(s)
    



def eda():
    df = pd.read_csv("featured_data.csv")  
    with st.expander('Data Visualization'):
        choose = st.selectbox('Choose a plot to view', ['Property_type', 'Region', 'Facilities', 'Rooms', 'Property_type and Region'])
        if choose == 'Property_type':
            AveragePropertyType = df.groupby('property_type')['monthly_rent(RM)'].mean().sort_values(ascending=False).reset_index()
            fig = px.bar(
            AveragePropertyType.round(), 
            y='monthly_rent(RM)',  
            x='property_type', 
            title='Distribution of Average Price Based on Property type', 
            labels={'monthly_rent(RM)': 'Rent', 'property_type': 'Property Type'},
             width=600, height=400, 
            )
            st.write(fig)
        elif choose == 'Region':
            AveragePrice = df.groupby(['region'])['monthly_rent(RM)'].mean().reset_index()
            fig = px.bar(
            AveragePrice, 
            x='region',  
            y='monthly_rent(RM)', 
            title='Distribution of Average Price Based on Region', 
            labels={'region': 'Region', 'monthly_rent(RM)': 'Average Monthly Rent (RM)'}
            )
            st.write(fig)
        elif choose == 'Facilities':
            df_facilities = df[['Gymnasium', 'Lift', 'Minimart', 'Sauna', 'Security', 'Swimming Pool']].sum()
            fig = px.bar(df_facilities, title='Facilities Availability Across Properties')
            st.write(fig)
        elif choose == 'Rooms':
            AverageRooms = df.groupby('rooms')['monthly_rent(RM)'].mean().sort_values(ascending=False).reset_index()
            fig = px.bar(
            AverageRooms.round(), 
            y='monthly_rent(RM)',  
            x='rooms', 
            title='Distribution of Average Price Based on Rooms', 
            labels={'monthly_rent(RM)': 'Rent', 'rooms': 'Rooms'}
        )
            st.write(fig)
        elif choose == 'Property_type and Region':
            region_property_type = df.groupby(['property_type', 'region'])['monthly_rent(RM)'].mean().reset_index()
            fig = px.bar(
            region_property_type, 
            x='property_type', 
            y='monthly_rent(RM)',  
            title='Distribution of Average Price Based on Property Type and Region', 
            labels={'monthly_rent(RM)': 'Rent (RM)', 'property_type': 'Property Type', 'region': 'Region'},
            hover_data=['region'],
            color='region',
            width=650, height=400, 
        )
            st.write(fig)

    with st.expander('Data Visualazation Part 2'):
        choose = st.selectbox('Choosse a plot to view', ['Security vs Price', 'Apartment + Rooms vs Rent', 'Apartment + Parking vs Rent', 'Apartment + Size vs Rent'])
        if choose == 'Security vs Price':
            apartment = df[df['property_type']=='Apartment']
            AverageWithSecurity = apartment.groupby('Security')['monthly_rent(RM)'].mean().reset_index()
            fig = px.bar(
                AverageWithSecurity,  
                y='monthly_rent(RM)',  
                x='Security', 
                title='Distribution of Average Price Based on Security', 
                labels={'monthly_rent(RM)': 'Rent', 'Security': 'Security'}
            )
            st.write(fig)
        elif choose == 'Apartment + Rooms vs Rent':
            apartments_only = df[df['property_type'] == 'Apartment']
            apartments_avg_rent = apartments_only.groupby(['rooms'])['monthly_rent(RM)'].mean().sort_values(ascending=False).reset_index()
            fig = px.bar(
                apartments_avg_rent, 
                x='rooms', 
                y='monthly_rent(RM)',  
                title='Distribution of Average Rent for Apartments Based on Rooms', 
                labels={'monthly_rent(RM)': 'Rent (RM)', 'rooms': 'Number of Rooms'},
                width=650, height=400, 
            )
            st.write(fig)
        elif choose == 'Apartment + Parking vs Rent':
            apartment = df[df['property_type']=='Apartment']
            parking = apartment.groupby('parking')['monthly_rent(RM)'].mean().round().reset_index()
            st.write(px.bar(parking, x='parking', y='monthly_rent(RM)',  
            title='Average Rent Based on Parking Space', hover_data=['parking'], 
            labels={'monthly_rent(RM)': 'Average Rent (RM)'}, width=650, height=400,)) 
        elif choose == 'Apartment + Size vs Rent':
            apartment = df[df['property_type']=='Apartment']
            size = apartment.groupby('size')['monthly_rent(RM)'].mean().round().reset_index()
            st.write(px.scatter(size, x='size', y='monthly_rent(RM)',  
            title='Average Rent Based on Size', hover_data=['size'], 
            labels={'monthly_rent(RM)': 'Average Rent (RM)'}, width=650, height=400,))
            
    
def demo():
    with open('DecisionTreeRegressor.pkl', 'rb') as file:
        pipeline = pickle.load(file)

    st.title("Properties Monthly Rent Prediction")
    
    selected_property_type = st.selectbox("Property Type", options=['Service Residence', 'Apartment', 'Condominium', 'Studio', 'Townhouse Condo', 'Flat', 'Duplex', 'Others'])
    selected_rooms = st.slider("Rooms", 1, 10)
    selected_parking = st.slider("Parking", 1, 10)
    selected_bathroom = st.slider("Bathroom", 1, 8)
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
    prediction = pipeline.predict(input_df)
    st.header(f"Predicted Monthly Rent (RM): {prediction[0]:,.2f}")

pages = {
    "Intro": intro,
    "Dataset": dataset,
    'Demo': demo
}
page = st.sidebar.radio("Naviagate to", ["Intro", "Problem Statement","Dataset", "EDA","Demo"])
if page == "Intro":
    intro()
elif page == "Dataset":
    dataset()
elif page == "Demo":
    demo()
elif page == "EDA":
    eda()
elif page == "Problem Statement":
    problemStatement()





