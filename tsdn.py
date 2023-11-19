import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    st.title('Visualization User Viewing Activity')

    # Sidebar untuk pemilihan opsi
    selected_profile = st.sidebar.selectbox('Select Profile Name:', df['Profile Name'].unique())
    selected_device = st.sidebar.selectbox('Select Device Type:', df['Device Type'].unique())

    # Filter data berdasarkan opsi yang dipilih
    filtered_df = df[(df['Profile Name'] == selected_profile) & (df['Device Type'] == selected_device)]

    # Reset Pandas options to default
    with pd.option_context('mode.use_inf_as_null', False):
        # Visualisasi Scatter Plot
        st.subheader('Device Type by Profile Name with Start Time')
        fig, ax = plt.subplots(figsize=(16, 10))
        sns.scatterplot(x='Start Time', y='Profile Name', hue='Device Type', data=filtered_df, palette='viridis', ax=ax)
        plt.title('Device Type by Profile Name with Start Time')
        st.pyplot(fig)

        # Line chart for Duration_seconds
        st.subheader('Duration Over Time')
        fig_line, ax_line = plt.subplots(figsize=(12, 8))
        sns.lineplot(x='Start Time', y='Duration_seconds', data=filtered_df, ax=ax_line)
        ax_line.set_xlabel('Start Time')
        ax_line.set_ylabel('Duration (seconds)')
        ax_line.set_title('Duration Over Time')
        st.pyplot(fig_line)

        # Area chart for User_Device_Count
        st.subheader('User Device Count Over Time')
        fig_area, ax_area = plt.subplots(figsize=(12, 8))
        sns.lineplot(x='Start Time', y='User_Device_Count', data=filtered_df, ax=ax_area)
        ax_area.set_xlabel('Start Time')
        ax_area.set_ylabel('User Device Count')
        ax_area.set_title('User Device Count Over Time')
        st.pyplot(fig_area)

        # Pie chart for is_Possibly_Sharing
        st.subheader('Possibly Sharing Status')
        fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
        filtered_df['is_Possibly_Sharing'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax_pie)
        ax_pie.set_title('Possibly Sharing Status')
        st.pyplot(fig_pie)

# Panggil fungsi visualisasi interaktif
interactive_visualization(df_viewing)
