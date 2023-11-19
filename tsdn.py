import streamlit as st
import numpy as np
import pandas as pd

# Baca data
df_viewing = pd.read_csv('All_ViewingActivity.csv')

# Konversi Durasi ke Detik
df_viewing['Duration_seconds'] = pd.to_timedelta(df_viewing['Duration']).dt.total_seconds()
# Mengubah kolom Start Time ke tipe datetime dan Mengurutkan berdasarkan waktu
df_viewing['Start Time'] = pd.to_datetime(df_viewing['Start Time'])
df_viewing = df_viewing.sort_values(by='Start Time')
df_viewing['Duration'] = pd.to_timedelta(df_viewing['Duration'])

# Corrected line: Convert 'Duration' to timedelta before adding to 'Start Time'
df_viewing['End Time'] = df_viewing['Start Time'] + df_viewing['Duration']

# Calculate device usage count for each user
device_usage_count = df_viewing.groupby('Profile Name')['Device Type'].nunique().reset_index()
device_usage_count.rename(columns={'Device Type': 'User_Device_Count'}, inplace=True)

# Calculate unique country count for each user
country_count = df_viewing.groupby('Profile Name')['Country'].nunique().reset_index()
country_count.rename(columns={'Country': 'User_Country_Count'}, inplace=True)

# Merge device and country counts back to the original DataFrame
df_viewing = pd.merge(df_viewing, device_usage_count, on='Profile Name', how='left')
df_viewing = pd.merge(df_viewing, country_count, on='Profile Name', how='left')

# Create a binary target variable 'is_sharing'
# You may need to adjust this based on your specific criteria
df_viewing['is_Possibly_Sharing'] = (df_viewing['User_Device_Count'] > 2) & (df_viewing['User_Country_Count'] > 1)

# Visualisasi interaktif dengan Streamlit
def interactive_visualization(df):
    st.title('User Viewing Activity Summary')

    # Sidebar untuk pemilihan opsi
    selected_profile = st.sidebar.selectbox('Select Profile Name:', df['Profile Name'].unique())
    selected_device = st.sidebar.selectbox('Select Device Type:', df['Device Type'].unique())

    # Filter data berdasarkan opsi yang dipilih
    filtered_df = df[(df['Profile Name'] == selected_profile) & (df['Device Type'] == selected_device)]

    # Display summary information in text format
    st.subheader('Summary Information:')
    st.text(f"Selected Profile: {selected_profile}")
    st.text(f"Selected Device Type: {selected_device}")
    st.text(f"Total Viewing Sessions: {len(filtered_df)}")
    st.text(f"Total Duration: {filtered_df['Duration_seconds'].sum()} seconds")

    # Display detailed information in table format
    st.subheader('Detailed Information:')
    st.table(filtered_df[['Start Time', 'Device Type', 'Country', 'Duration_seconds', 'is_Possibly_Sharing']])

# Panggil fungsi visualisasi interaktif
interactive_visualization(df_viewing)
