import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Single Player Analysis",
    page_icon='data/JJGH.jpeg',
)

st.title('Welcome to the Glory Hole')
st.image('data/JJGH.jpeg', width=500)

st.sidebar.write("Brought to you by:")
st.sidebar.image('JJGH_Advanced/data/JJGH.jpeg', width=300)

st.write("All data provided by https://github.com/nflverse/nflverse-data/releases")
st.write("Brought to you by JJGH - There ain't no glory hole like a Jerry Jones Glory Hole!")