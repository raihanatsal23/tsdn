import numpy as np
import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Legend
from bokeh.palettes import Viridis
from datetime import datetime

# Load your data
df_clickstream = pd.read_csv('All_Clickstream.csv')
df_device = pd.read_csv('All_Devices.csv')
df_profiles = pd.read_csv('All_Profiles.csv')
df_search = pd.read_csv('All_SearchHistory.csv')
df_viewing = pd.read_csv('All_ViewingActivity.csv')

# Convert Start Time to datetime
df_viewing['Start Time'] = pd.to_datetime(df_viewing['Start Time'])

# Handling NaN values
df_viewing = df_viewing.dropna(subset=['Start Time'])

# Create Bokeh plot
def create_interactive_plot(df):
    p = figure(plot_width=800, plot_height=500, title='Device Type by Profile Name with Start Time',
               x_axis_label='Start Time', y_axis_label='Profile Name')

    # Get unique Profile Names
    profile_names = df['Profile Name'].unique()

    # Assign a color to each unique Device Type using Viridis color palette
    colors = Viridis[len(df['Device Type'].unique())]

    legend_items = []

    for i, device_type in enumerate(df['Device Type'].unique()):
        source = ColumnDataSource(df[df['Device Type'] == device_type])

        # Scatter plot
        scatter = p.scatter(x='Start Time', y='Profile Name', source=source,
                            color=colors[i], size=8, legend_label=device_type)

        # Add HoverTool
        hover = HoverTool()
        hover.tooltips = [('Profile Name', '@{Profile Name}'),
                          ('Device Type', device_type),
                          ('Start Time', '@{Start Time{%Y-%m-%d %H:%M:%S}}')]
        hover.renderers = [scatter]
        p.add_tools(hover)

        # Box plot
        box = p.circle(x='Start Time', y='Profile Name', source=source, size=10, color=colors[i], legend_label=device_type)

        # Add legend items
        legend_items.append((device_type, [scatter, box]))

    # Add legend
    legend = Legend(items=legend_items, location=(0, 0))
    p.add_layout(legend, 'right')

    return p

# Streamlit app
def main():
    st.title('Interactive Visualization with Bokeh and Streamlit')

    # Filter data
    start_time = st.date_input('Select start date', min_value=df_viewing['Start Time'].min().date(), max_value=df_viewing['Start Time'].max().date())
    end_time = st.date_input('Select end date', min_value=start_time, max_value=df_viewing['Start Time'].max().date())

    # Filter data based on date range
    filtered_df = df_viewing[(df_viewing['Start Time'] >= start_time) & (df_viewing['Start Time'] <= end_time)]

    # Create Bokeh plot
    bokeh_plot = create_interactive_plot(filtered_df)

    # Display Bokeh plot using st.bokeh_chart
    st.bokeh_chart(bokeh_plot)

if __name__ == '__main__':
    main()
