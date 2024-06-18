import streamlit as st
import pandas as pd
import streamlit_options_menu
from find-iv.py import *


# Create streamlit app
st.title  ('Options Volatility Ratios')

#Display Data
st.write('Delta 25 and Delta 50 Ratios')
st.write(data)

