import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from scipy.stats import zscore
import seaborn as sns

# Baca data
df_viewing = pd.read_csv('All_ViewingActivity.csv')

# Konversi Durasi ke Detik
df_viewing['Duration_seconds'] = pd.to_timedelta(df_viewing['Duration']).dt.total_seconds()
# Mengubah kolom Start Time ke tipe datetime dan Mengurutkan berdasarkan waktu
df_viewing['Start Time'] = pd.to_datetime(df_viewing['Start Time'])
df_viewing = df_viewing.sort_values(by='Start Time')
df_viewing['Duration'] = pd.to_timedelta(df_viewing['Duration'])
df_viewing['End Time'] = df_viewing['Start Time'] + df_viewing['Duration']

# Visualisasi interaktif dengan Streamlit
def interactive_visualization(df):
    st.title('Visualization User Viewing Activity')

    # Sidebar untuk pemilihan opsi
    selected_profile = st.sidebar.selectbox('Select Profile Name:', df['Profile Name'].unique())
    selected_device = st.sidebar.selectbox('Select Device Type:', df['Device Type'].unique())

    # Filter data berdasarkan opsi yang dipilih
    filtered_df = df[(df['Profile Name'] == selected_profile) & (df['Device Type'] == selected_device)]

    # Visualisasi Scatter Plot
    st.subheader('Device Type by Profile Name with Start Time')
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x='Start Time', y='Profile Name', hue='Device Type', data=filtered_df, palette='viridis', ax=ax)
    plt.title('Device Type by Profile Name with Start Time')
    st.pyplot(fig)

# Panggil fungsi visualisasi interaktif
interactive_visualization(df_viewing)
