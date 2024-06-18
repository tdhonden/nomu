import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Title of the App
st.title('Simple CSV Data Chart with pathlib')

#Define the path to the CSV file using pathlib

data_file_path = Path(__file__).parent / 'data/delta50.csv'

#Load data

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

data = load_data(data_file_path)

#display data
st.write('## Data')
st.write(data)

#create a simple chart

st.write('##chart')
fig, ax = plt.subplots()
ax.bar(data['Date'], data['Delta_1m'])
ax.set_xlabel('Date')
ax.set_ylabel('Delta_1m')

st.pyplot(fig)
