import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import seaborn as sns

# Baca data
df_viewing = pd.read_csv('All_ViewingActivity.csv')

# Konversi Durasi ke Detik
df_viewing['Duration_seconds'] = pd.to_timedelta(df_viewing['Duration']).dt.total_seconds()

# Mengubah kolom Start Time ke tipe datetime dan Mengurutkan berdasarkan waktu
df_viewing['Start Time'] = pd.to_datetime(df_viewing['Start Time'])
df_viewing = df_viewing.sort_values(by='Start Time')
df_viewing['End Time'] = df_viewing['Start Time'] + df_viewing['Duration']

# Konversi Duration ke string untuk memudahkan penanganan di Streamlit
df_viewing['Duration_str'] = df_viewing['Duration'].astype(str)

# Visualisasi interaktif dengan Streamlit
def interactive_visualization(df):
    st.title('Interactive Visualization with Streamlit')

    # Sidebar untuk pemilihan opsi
    selected_profile = st.sidebar.selectbox('Select Profile Name:', df['Profile Name'].unique())
    selected_device = st.sidebar.selectbox('Select Device Type:', df['Device Type'].unique())

    # Filter data berdasarkan opsi yang dipilih
    filtered_df = df[(df['Profile Name'] == selected_profile) & (df['Device Type'] == selected_device)]

    # Visualisasi Scatter Plot
    st.subheader('Device Type by Profile Name with Start Time')
    fig, ax = plt.subplots(figsize=(16, 10))  # Ubah ukuran plot di sini
    sns.scatterplot(x='Start Time', y='Profile Name', hue='Device Type', data=filtered_df, palette='viridis', ax=ax)
    plt.title('Device Type by Profile Name with Start Time')
    st.pyplot(fig)

    # Deteksi Anomali
    st.subheader('Anomaly Detection')

    # Debugging: Tampilkan jenis data dan nilai unik dari kolom "Duration"
    st.write("Data Types:", df_viewing.dtypes)
    st.write("Unique Durations:", df_viewing['Duration_str'].unique())

    features = ['Duration_seconds']
    isolation_forest = IsolationForest(contamination=0.05)  # Ubah tingkat kontaminasi sesuai kebutuhan
    filtered_df['Anomaly'] = isolation_forest.fit_predict(filtered_df[features])

    # Tampilkan data anomali
    st.write("Anomalous Data:")
    st.write(filtered_df[filtered_df['Anomaly'] == -1])

# Panggil fungsi visualisasi interaktif
interactive_visualization(df_viewing)
