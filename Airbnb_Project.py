# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 14:13:56 2023

@author: ELCOT
"""
#IMPORTING THE REQUIRED PACKAGES
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
import base64
from PIL import Image
import warnings
import plotly.figure_factory as ff


warnings.filterwarnings('ignore')

st.set_page_config(page_title="AirBnb-Analysis", page_icon="logo.jfif", layout="wide")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

#BACKGROUND IMAGE
def back_img(image):
    with open(image, "rb") as image_file:
        encode_str = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encode_str.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

back_img("images_1.jfif")  


#HEADBAR
SELECT = option_menu(
    menu_title=None,
    options=["Home", "Airbnb Details", "Analysis"],
    icons=["house", "bar-chart", "at"],
    default_index=0,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "black", "font-size": "20px"},

            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
            "nav-link-selected": {"background-color": "#6F36AD"}})


#HOME PAGE
if SELECT == "Home":
    #display project overview
    st.header('Airbnb Analysis')
    col1, col2 = st.columns(2)
    with col1:
        st.image("download.jfif",width=500)
    with col2:
        st.header('Airbnb Analysis')
        st.subheader(
            ":white[This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.]")
        st.write("---")
        
    st.write("#") 
    st.subheader('Technologies Used:')
    st.subheader('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau')
    st.subheader('Domain:')
    st.subheader('Travel Industry, Property management and Tourism')


#ANALYSIS PAGE
if SELECT == "Analysis":

 os.chdir(r"C:/Users/ELCOT/GUVI/Python/DTM9/.spyder-py3/Projects/Airbnb")
 df = pd.read_csv("airbnb_nyc.csv", encoding="ISO-8859-1")

    
 # CHOOSE neighbourhood_group
 neighbourhood_group = st.multiselect("Choose your city", df["neighbourhood_group"].unique())
 if not neighbourhood_group:
     df2 = df.copy()
 else:
     df2 = df[df["neighbourhood_group"].isin(neighbourhood_group)]

 # CHOOSE neighbourhood
 neighbourhood = st.multiselect("Choose your neighbourhood", df2["neighbourhood"].unique())
 if not neighbourhood:
     df3 = df2.copy()
 else:
     df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

 
# Filter the data based on neighbourhood_group, neighbourhood

 if not neighbourhood_group and not neighbourhood:
     filtered_df = df
 elif not neighbourhood:
     filtered_df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
 elif not neighbourhood_group:
     filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
 elif neighbourhood:
     filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
 elif neighbourhood_group:
     filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group)]
 elif neighbourhood_group and neighbourhood:
     filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
 else:
     filtered_df = df3[df3["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]

 room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

 
#LINE CHART
 st.subheader("Price_Analysis")
 st.line_chart(room_type_df, x="room_type", y="price")
 
 
#SCATTER PLOT
 data1 = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
 data1['layout'].update(title="Room_type in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                        titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                        yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
 st.plotly_chart(data1, use_container_width=True)


 
#MAP VIEW
 st.subheader("Airbnb Analysis in Map view")
 df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

 st.map(df)

# CONTACT PAGE

if SELECT == "Airbnb Details":
    
    os.chdir(r"C:/Users/ELCOT/GUVI/Python/DTM9/.spyder-py3/Projects/Airbnb")
    df = pd.read_csv("airbnb_nyc.csv", encoding="ISO-8859-1")


    # CHOOSE neighbourhood_group
    neighbourhood_group = st.multiselect("Choose your city", df["neighbourhood_group"].unique())
    if not neighbourhood_group:
        df2 = df.copy()
    else:
        df2 = df[df["neighbourhood_group"].isin(neighbourhood_group)]

    # CHOOSE neighbourhood
    neighbourhood = st.multiselect("Choose your neighbourhood", df2["neighbourhood"].unique())
    if not neighbourhood:
        df3 = df2.copy()
    else:
        df3 = df2[df2["neighbourhood"].isin(neighbourhood)]
    
    #FILTERING THE OPTIONS
    if not neighbourhood_group and not neighbourhood:
        filtered_df = df
    elif not neighbourhood:
        filtered_df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif not neighbourhood_group:
        filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood:
        filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood_group:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif neighbourhood_group and neighbourhood:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
    else:
        filtered_df = df3[df3["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]


    #CREATING DF FOR OOM TYPES
    room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

    options_roomtype = st.selectbox("Choose the room type",('All','Entire home/apt','Private room','Shared room'))

    #DATA DISPLAY BASED ON ROOM TYPE
    if 'All' in options_roomtype:
        room_type_df=filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()
    
    if 'Entire home/apt' in options_roomtype:
        room_type_df=room_type_df.loc[room_type_df['room_type']=='Entire home/apt']
    
    if 'Private room' in options_roomtype:
        room_type_df=room_type_df.loc[room_type_df['room_type']=='Private room']
    
    if 'Shared room' in options_roomtype:
        room_type_df=room_type_df.loc[room_type_df['room_type']=='Shared room']
            
            


    st.markdown(
     """
     <style>
     .streamlit-expanderHeader {
         font-size: 20px;
     }
     </style>
     """,
     unsafe_allow_html=True,
    )
    
    cl1, cl2 = st.columns((2))
    with cl1:
       
       with st.expander("Price Details For Rooms"):
           st.write(room_type_df.style.background_gradient(cmap="Blues"))
           
    with cl2:
       with st.expander("Average Price"):
           neighbourhood_group = filtered_df.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
           st.write(neighbourhood_group.style.background_gradient(cmap="Blues"))
           
    with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
        st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Blues"))

    with st.expander("Summary_Table"):
       df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "review_scores", "room_type", "price", "minimum_nights", "host_name"]]
       fig = ff.create_table(df_sample)
       st.plotly_chart(fig, use_container_width=True)

    


   