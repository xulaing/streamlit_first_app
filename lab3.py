import altair as alt
import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import os
import matplotlib
import seaborn as sns
import datetime
import streamlit.components.v1 as components
sns.set_theme()


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🤪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Streamlit dashboard 👩‍💻')
st.caption('Céline KHAUV 20180417')


# log execution time
@st.cache(suppress_st_warning=True)
def log(func):
    def wrapper(*args, **kwargs):
        with open("logs.txt", "a") as f:
            f.write("Called function with " + " ".join(
                [str(arg) for arg in args]) + " at " + str(datetime.datetime.now()) + "\n")
        val = func(*args, **kwargs)
        return val
    return wrapper


def my_component(name, key=None):
    component_value = _component_func(name=name, key=key, default=0)
    return component_value


def get_dom(dt):
    return dt.day


def get_weekday(dt):
    return dt.weekday()


def get_hours(dt):
    return dt.hour


def count_rows(rows):
    return len(rows)


# Initialisation de toutes les variables à afficher pour uber-raw-data.csv
@st.cache(suppress_st_warning=True)
def load_data14():
    return pd.read_csv("uber-raw-data-apr14.csv")


@st.cache(suppress_st_warning=True)
def analyse_data14(df):
    dt = pd.to_datetime(df['Date/Time'], format='%m/%d/%Y %H:%M:%S')
    dt_frame = dt.to_frame()
    dt_frame = pd.concat([dt_frame, df[['Lat', 'Lon']]], axis=1)
    dt_frame['dom'] = dt_frame['Date/Time'].map(get_dom)
    dt_frame['weekday'] = dt_frame['Date/Time'].map(get_weekday)
    dt_frame['hour'] = dt_frame['Date/Time'].map(get_hours)
    return dt_frame


def sort_data(dt_frame):
    return dt_frame.sort_values(by='Date/Time')


def count_rows_data14(dt_frame):
    return dt_frame.groupby(['weekday', 'hour']).apply(
        count_rows).unstack(level=0)


def coor_data14(dt_frame):
    dt_map = dt_frame[['Lat', 'Lon']].copy()
    dt_map.rename(columns={'Lat': 'lat', 'Lon': 'lon'}, inplace=True)
    return dt_map

# Innitialisation de toutes les variables à afficher pour ny-trips-data.csv


@st.cache(suppress_st_warning=True)
def load_data15():
    return pd.read_csv("ny-trips-data.csv")


@st.cache(suppress_st_warning=True)
def analyse_data15(dt_trips):
    dt_trips[['tpep_pickup_datetime', 'tpep_dropoff_datetime']] = dt_trips[[
        'tpep_pickup_datetime', 'tpep_dropoff_datetime']].apply(pd.to_datetime)
    dt_trips['dom_pickup'] = dt_trips['tpep_pickup_datetime'].map(get_dom)
    dt_trips['dom_dropoff'] = dt_trips['tpep_dropoff_datetime'].map(get_dom)
    dt_trips['weekday_pickup'] = dt_trips['tpep_pickup_datetime'].map(
        get_weekday)
    dt_trips['weekday_dropoff'] = dt_trips['tpep_dropoff_datetime'].map(
        get_weekday)
    dt_trips['hour_pickup'] = dt_trips['tpep_pickup_datetime'].map(get_hours)
    dt_trips['hour_dropoff'] = dt_trips['tpep_dropoff_datetime'].map(get_hours)
    return dt_trips


def count_rows_data15(dt_trips):
    dt_trips_grouped = dt_trips.groupby(['weekday_pickup', 'hour_pickup']).apply(
        count_rows).unstack(level=0)
    dt_trips_grouped = dt_trips.groupby(['weekday_dropoff', 'hour_dropoff']).apply(
        count_rows).unstack(level=0)
    return dt_trips_grouped


def coor_data15(dt_trips):
    dt_map_trips1 = dt_trips[['pickup_latitude', 'pickup_longitude']].copy()
    dt_map_trips1.rename(
        columns={'pickup_latitude': 'lat', 'pickup_longitude': 'lon'}, inplace=True)
    dt_map_trips2 = dt_trips[['dropoff_latitude', 'dropoff_longitude']].copy()
    dt_map_trips2.rename(
        columns={'dropoff_latitude': 'lat', 'dropoff_longitude': 'lon'}, inplace=True)
    return dt_map_trips1, dt_map_trips2


def map_dom_data14(dt_frame):
    fig_dom, ax_dom = plt.subplots()
    ax_dom.hist(dt_frame["dom"], bins=30, rwidth=0.8, range=(0.5, 30.5))
    plt.xlabel('Date of the month')
    plt.ylabel('Frequency')
    plt.title('Frequency by DoM - Uber - April 2014')
    return fig_dom


def map_hour_data14(dt_frame):
    fig_hour, ax_hour = plt.subplots()
    ax_hour.hist(dt_frame["hour"], bins=24, range=(0.5, 24))
    plt.xlabel('Hour of the day')
    plt.ylabel('Frequency')
    plt.title('Frequency by hour - Uber - April 2014')
    return fig_hour


@log
def map_week_data14(dt_frame):
    fig_week, ax_week = plt.subplots()
    ax_week.hist(dt_frame["weekday"], bins=7, rwidth=0.8, range=(-0.5, 6.5))
    plt.xlabel('Weekday')
    plt.ylabel('Frequency')
    plt.title('Frequency by weekday - Uber - April 2014')
    plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Mon', 'Tue',
                                       'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    return fig_week


@log
def heatmap_data14(dt_frame):
    fig, ax = plt.subplots()
    ax = sns.heatmap(count_rows_data14(dt_frame))
    plt.title('Frequency by hour in a week - Uber - April 2014')
    return fig


def map_dom_data15(dt_trips):
    fig_dom, ax_dom = plt.subplots()
    ax_dom.hist(dt_trips["dom_pickup"], bins=30, rwidth=0.8, range=(15, 16))
    ax_dom.hist(dt_trips["dom_dropoff"], bins=30, rwidth=0.8, range=(15, 16))
    plt.xlabel('Date of the month')
    plt.ylabel('Frequency')
    plt.title('Frequency by DoM - Trips - January 2015')
    return fig_dom


def map_hour_data15(dt_trips):
    fig_hour, ax_hour = plt.subplots()
    ax_hour.hist(dt_trips["hour_pickup"], bins=24, range=(0.5, 24))
    ax_hour.hist(dt_trips["hour_dropoff"], bins=24, range=(0.5, 24))
    plt.xlabel('Hour of the day')
    plt.ylabel('Frequency')
    plt.title('Frequency by hour - Trips - January 2015')
    return fig_hour


def map_week_data15(dt_trips):
    fig_week, ax_week = plt.subplots()
    ax_week.hist(dt_trips["weekday_pickup"], bins=2,
                 range=(2.5, 4.5), rwidth=0.8)
    ax_week.hist(dt_trips["weekday_dropoff"], bins=2,
                 range=(2.5, 4.5), rwidth=0.8)
    plt.xlabel('Weekday')
    plt.ylabel('Frequency')
    plt.title('Frequency by weekday - Trips - January 2015')
    plt.xticks([2, 3, 4], ['Wed', 'Thu', 'Fri'])
    return fig_week


def heatmap_data15(dt_trips):
    fig, ax = plt.subplots()
    ax = sns.heatmap(count_rows_data15(dt_trips))
    plt.title('Frequency by hour in a week - Trips - Jan 2015')
    return fig


@st.cache
def active_date(choice):
    if choice == 1:
        dt = load_data14()
        return analyse_data14(dt)
    elif choice == 2:
        dt = load_data15()
        return analyse_data15(dt)
    else:
        return 0


# sidebar to select which dataset to display
option = st.sidebar.selectbox(
    'Which dataset do you want to display ?',
    ('Uber', 'Trips', 'iFrame'))

if option == 'Uber':
    dt_frame = active_date(1)
    # uber-raw-data
    st.write("Uber Raw Data - Apr 2014")

    # display the dataset
    expander = st.expander("Dataset")
    expander.write(dt_frame)

    # display an histogram of the frequency by dom
    expander = st.expander("Frequency by date of month")
    expander.pyplot(map_dom_data14(dt_frame))

    # display an histogram of the frequency by hour
    expander = st.expander("Frequency by hour")
    expander.pyplot(map_hour_data14(dt_frame))

    # display an histogram of the frequency by weekday
    expander = st.expander("Frequency by week")
    expander.pyplot(map_week_data14(dt_frame))

    # display a heatmap of the frequency by hour
    expander = st.expander("Frequency by hour in a week")

    expander.pyplot(heatmap_data14(dt_frame))

    st.title("Map of Uber")
    st.map(coor_data14(dt_frame))
elif option == 'Trips':
    dt_trips = active_date(2)
    # ny-trips-data
    st.write("NY Trips Data - Jan 2015")
    # display the dataset
    expander = st.expander("Dataset")
    expander.write(dt_trips)

    # display an histogram of the frequency by dom
    expander = st.expander("Frequency by date of month")
    expander.pyplot(map_dom_data15(dt_trips))

    # display an histogram of the frequency by hour
    expander = st.expander("Frequency by hour")
    expander.pyplot(map_hour_data15(dt_trips))

    # display an histogram of the frequency by weekday
    expander = st.expander("Frequency by week")
    expander.pyplot(map_week_data15(dt_trips))

    # display an heatmap of the frequency by hour
    expander = st.expander("Frequency by hour in a week")
    expander.pyplot(heatmap_data15(dt_trips))

    st.title("Map of Ubers - Pickup")
    dt_map_trips1, dt_map_trips2 = coor_data15(dt_trips)
    st.map(dt_map_trips1)
    st.title("Map of Ubers - Dropoff")
    st.map(dt_map_trips2)
elif option == 'iFrame':
    components.iframe(
        "https://treehousetechgroup.com/wp-content/uploads/2020/01/Screen-Shot-2020-01-28-at-10.13.28-AM.png")
    components.iframe(
        "https://www.youtube.com/embed/8pHzROP1D-w")
    