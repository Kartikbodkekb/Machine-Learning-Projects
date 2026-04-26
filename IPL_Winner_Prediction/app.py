import streamlit as st
import pickle
import numpy as np

# st.write('Hello')
# Load model and encoders
with open('model/rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

# Title
st.title('🏏 IPL Match Winner Predictor')

# Get list of teams and venues from encoders
teams = list(label_encoders['team1'].classes_)
venues = list(label_encoders['venue'].classes_)

# Input widgets
team1 = st.selectbox('Select Team 1', teams)
team2 = st.selectbox('Select Team 2', teams)
toss_winner = st.selectbox('Toss Winner', teams)
toss_decision = st.selectbox('Toss Decision', ['bat', 'field'])
venue = st.selectbox('Venue', venues)
season = st.slider('Season', min_value=2007, max_value=2026, value=2024)

# Predict button
if st.button('Predict Winner'):

    # Encode inputs
    t1 = label_encoders['team1'].transform([team1])[0]
    t2 = label_encoders['team2'].transform([team2])[0]
    tw = label_encoders['toss_winner'].transform([toss_winner])[0]
    td = label_encoders['toss_decision'].transform([toss_decision])[0]
    v = label_encoders['venue'].transform([venue])[0]

    # Make prediction
    input_data = np.array([[v, season, tw, td, t1, t2]])
    prediction = model.predict(input_data)[0]

    # Decode prediction
    winner = label_encoders['match_won_by'].classes_[prediction]

    st.success(f'🏆 Predicted Winner: {winner}')