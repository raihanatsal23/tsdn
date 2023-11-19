import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from scipy.stats import zscore
import seaborn as sns

# Load data
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

# Streamlit App
st.title('Interactive Visualization of Viewing Data')

# Scatter plot
st.subheader('Scatter Plot of Device Type by Profile Name with Start Time')

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Plot scatter plot
scatter = ax.scatter(df_viewing['Start Time'], df_viewing['Profile Name'], c=df_viewing['Device Type'],
                     cmap='viridis', s=50)

# Add legend
legend = ax.legend(*scatter.legend_elements(), title='Device Type')
ax.add_artist(legend)

# Set labels and title
ax.set_xlabel('Start Time')
ax.set_ylabel('Profile Name')
ax.set_title('Device Type by Profile Name with Start Time')

# Display the plot using Streamlit
st.pyplot(fig)

# Bar chart for User_Device_Count
st.subheader('User Device Count')

# Create a figure and axis
fig1, ax1 = plt.subplots(figsize=(12, 8))

# Plot bar chart
ax1.bar(device_usage_count['Profile Name'], device_usage_count['User_Device_Count'])

# Set labels and title
ax1.set_xlabel('Profile Name')
ax1.set_ylabel('User Device Count')
ax1.set_title('User Device Count')

# Display the plot using Streamlit
st.pyplot(fig1)

# Bar chart for User_Country_Count
st.subheader('User Country Count')

# Create a figure and axis
fig2, ax2 = plt.subplots(figsize=(12, 8))

# Plot bar chart
ax2.bar(country_count['Profile Name'], country_count['User_Country_Count'])

# Set labels and title
ax2.set_xlabel('Profile Name')
ax2.set_ylabel('User Country Count')
ax2.set_title('User Country Count')

# Display the plot using Streamlit
st.pyplot(fig2)

# Pie chart for is_Possibly_Sharing
st.subheader('Possibly Sharing Status')

# Create a figure and axis
fig3, ax3 = plt.subplots(figsize=(8, 8))

# Plot pie chart
df_viewing['is_Possibly_Sharing'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax3)

# Set title
ax3.set_title('Possibly Sharing Status')

# Display the plot using Streamlit
st.pyplot(fig3)
