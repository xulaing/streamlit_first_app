import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
sns.set_theme()


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🤪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Streamlit dashboard 👩‍💻')
st.caption('Céline KHAUV 20180417')


def get_dom(dt):
    return dt.day


def get_weekday(dt):
    return dt.weekday()


def get_hours(dt):
    return dt.hour


def count_rows(rows):
    return len(rows)


# Innitialisation de toutes les variables à afficher pour uber-raw-data.csv
df = pd.read_csv("uber-raw-data-apr14.csv")
dt = pd.to_datetime(df['Date/Time'], format='%m/%d/%Y %H:%M:%S')
dt_frame = dt.to_frame()
dt_frame = pd.concat([dt_frame, df[['Lat', 'Lon']]], axis=1)
dt_frame['dom'] = dt_frame['Date/Time'].map(get_dom)
dt_frame['weekday'] = dt_frame['Date/Time'].map(get_weekday)
dt_frame['hour'] = dt_frame['Date/Time'].map(get_hours)
dt_frame_sorted = dt_frame.sort_values(by='Date/Time')
dt_grouped = dt_frame.groupby(['weekday', 'hour']).apply(
    count_rows).unstack(level=0)
dt_map = dt_frame[['Lat', 'Lon']].copy()
dt_map.rename(columns={'Lat': 'lat', 'Lon': 'lon'}, inplace=True)

# Innitialisation de toutes les variables à afficher pour ny-trips-data.csv
dt_trips = pd.read_csv("ny-trips-data.csv")
dt_trips[['tpep_pickup_datetime', 'tpep_dropoff_datetime']] = dt_trips[[
    'tpep_pickup_datetime', 'tpep_dropoff_datetime']].apply(pd.to_datetime)
dt_trips['dom_pickup'] = dt_trips['tpep_pickup_datetime'].map(get_dom)
dt_trips['dom_dropoff'] = dt_trips['tpep_dropoff_datetime'].map(get_dom)
dt_trips['weekday_pickup'] = dt_trips['tpep_pickup_datetime'].map(get_weekday)
dt_trips['weekday_dropoff'] = dt_trips['tpep_dropoff_datetime'].map(
    get_weekday)
dt_trips['hour_pickup'] = dt_trips['tpep_pickup_datetime'].map(get_hours)
dt_trips['hour_dropoff'] = dt_trips['tpep_dropoff_datetime'].map(get_hours)
dt_trips_grouped = dt_trips.groupby(['weekday_pickup', 'hour_pickup']).apply(
    count_rows).unstack(level=0)
dt_trips_grouped = dt_trips.groupby(['weekday_dropoff', 'hour_dropoff']).apply(
    count_rows).unstack(level=0)
dt_map_trips1 = dt_trips[['pickup_latitude', 'pickup_longitude']].copy()
dt_map_trips1.rename(
    columns={'pickup_latitude': 'lat', 'pickup_longitude': 'lon'}, inplace=True)
dt_map_trips2 = dt_trips[['dropoff_latitude', 'dropoff_longitude']].copy()
dt_map_trips2.rename(
    columns={'dropoff_latitude': 'lat', 'dropoff_longitude': 'lon'}, inplace=True)

# sidebar to select which dataset to display
option = st.sidebar.selectbox(
    'Which dataset do you want to display ?',
    ('Uber', 'Trips'))

if option == 'Uber':
    # uber-raw-data
    st.write("Uber Raw Data - Apr 2014")

    # display the dataset
    expander = st.expander("Dataset")
    expander.write(dt_frame)

    # display an histogram of the frequency by dom
    expander = st.expander("Frequency by date of month")
    fig_dom, ax_dom = plt.subplots()
    ax_dom.hist(dt_frame["dom"], bins=30, rwidth=0.8, range=(0.5, 30.5))
    plt.xlabel('Date of the month')
    plt.ylabel('Frequency')
    plt.title('Frequency by DoM - Uber - April 2014')
    expander.pyplot(fig_dom)

    # display an histogram of the frequency by hour
    expander = st.expander("Frequency by hour")
    fig_hour, ax_hour = plt.subplots()
    ax_hour.hist(dt_frame["hour"], bins=24, range=(0.5, 24))
    plt.xlabel('Hour of the day')
    plt.ylabel('Frequency')
    plt.title('Frequency by hour - Uber - April 2014')
    expander.pyplot(fig_hour)

    # display an histogram of the frequency by weekday
    expander = st.expander("Frequency by week")
    fig_week, ax_week = plt.subplots()
    ax_week.hist(dt_frame["weekday"], bins=7, rwidth=0.8, range=(-0.5, 6.5))
    plt.xlabel('Weekday')
    plt.ylabel('Frequency')
    plt.title('Frequency by weekday - Uber - April 2014')
    plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Mon', 'Tue',
                                       'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    expander.pyplot(fig_week)

    # display a heatmap of the frequency by hour
    expander = st.expander("Frequency by hour in a week")
    fig, ax = plt.subplots()
    ax = sns.heatmap(dt_grouped)
    plt.title('Frequency by hour in a week - Uber - April 2014')
    expander.pyplot(fig)

    st.title("Map of Uber")
    st.map(dt_map)
elif option == 'Trips':
    # ny-trips-data
    st.write("NY Trips Data - Jan 2015")

    # display the dataset
    expander = st.expander("Dataset")
    expander.write(dt_trips)

    # display an histogram of the frequency by dom
    expander = st.expander("Frequency by date of month")
    fig_dom, ax_dom = plt.subplots()
    ax_dom.hist(dt_trips["dom_pickup"], bins=30, rwidth=0.8, range=(15, 16))
    ax_dom.hist(dt_trips["dom_dropoff"], bins=30, rwidth=0.8, range=(15, 16))
    plt.xlabel('Date of the month')
    plt.ylabel('Frequency')
    plt.title('Frequency by DoM - Trips - January 2015')
    expander.pyplot(fig_dom)

    # display an histogram of the frequency by hour
    expander = st.expander("Frequency by hour")
    fig_hour, ax_hour = plt.subplots()
    ax_hour.hist(dt_trips["hour_pickup"], bins=24, range=(0.5, 24))
    ax_hour.hist(dt_trips["hour_dropoff"], bins=24, range=(0.5, 24))
    plt.xlabel('Hour of the day')
    plt.ylabel('Frequency')
    plt.title('Frequency by hour - Trips - January 2015')
    expander.pyplot(fig_hour)

    # display an histogram of the frequency by weekday
    expander = st.expander("Frequency by week")
    fig_week, ax_week = plt.subplots()
    ax_week.hist(dt_trips["weekday_pickup"], bins=2,
                 range=(2.5, 4.5), rwidth=0.8)
    ax_week.hist(dt_trips["weekday_dropoff"], bins=2,
                 range=(2.5, 4.5), rwidth=0.8)
    plt.xlabel('Weekday')
    plt.ylabel('Frequency')
    plt.title('Frequency by weekday - Trips - January 2015')
    plt.xticks([2, 3, 4], ['Wed', 'Thu', 'Fri'])
    expander.pyplot(fig_week)

    # display an heatmap of the frequency by hour
    expander = st.expander("Frequency by hour in a week")
    fig, ax = plt.subplots()
    ax = sns.heatmap(dt_trips_grouped)
    plt.title('Frequency by hour in a week - Trips - Jan 2015')
    expander.pyplot(fig)

    st.title("Map of Ubers - Pickup")
    st.map(dt_map_trips1)
    st.title("Map of Ubers - Dropoff")
    st.map(dt_map_trips2)
