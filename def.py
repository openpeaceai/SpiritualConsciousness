#!/usr/bin/env python
# coding: utf-8

# In[43]:


import streamlit as st


# In[50]:


st.set_page_config(
    page_title="Spiritual Consciousness Assesment",
    page_icon="☮️",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "https://openpeace.ai/about-us"
    }
)


# In[101]:


# Add css to make text bigger
st.markdown(
    """
    <style>
    
    label 
    {
    font-size: 3rem !important;
    color: #228B22;
    }
    
    div[class*="stSelect"] label {
    font-size: 26px;
    color: #228B22;
    }


    div[class*="stTextArea"] label {
    font-size: 3rem !important;
    color: #228B22;
    }

    div[class*="stTextInput"] label {
    font-size: 3rem !important;
    color: #228B22;
    }
    
    div[class*="stDateInput"] label {
    font-size: 3rem !important;
    color: #228B22;
    }

    div[class*="stNumberInput"] label {
    font-size: 3rem !important;
    color: #228B22;
    }
    
    div[data-testid="column"]:nth-of-type(1)
    {
        border:0px solid blue;
    }
    div[data-testid="column"]:nth-of-type(2)
    {
        border:0px solid blue;
        text-align: end;
    }
        
    </style>
    """,
    unsafe_allow_html=True,
)


# In[ ]:





# In[52]:


import pandas as pd
pd.set_option('display.max_colwidth', None)
from sqlalchemy import create_engine

import numpy as np 
import mysql.connector
import pycountry
from datetime import datetime, date, timedelta


# In[ ]:





# In[94]:


#with st.sidebar:
st.image("https://img1.wsimg.com/isteam/ip/f8df9fda-2223-42be-a383-5d7d72e7c082/Openpeace%20Logo_Layout%201A.png/:/rs=w:230,h:38,cg:true,m/cr=w:230,h:38/qt=q:100/ll", width=230)  # Adjust the width as needed
st.header("Spiritual Consciousness Assesment")
st.markdown('##### The Spiritual Consciousness Assesment is a unique and engaging \
            questionnaire designed to explore individual perspectives on spirituality, \
            personal growth, and transcendent experiences.')
#st.markdown('##') 
st.markdown('##### Use the form below to select the answers to the questions presented and submit it to see your Spiritual \
            Consciousness score.')
st.markdown('---')     
st.markdown('##### Please enter your email address, date of birth, and country.')
st.markdown('###### :red[Note that you can only take this assessment once, and your information \
                will remain anonymous, as we prioritize your privacy and security.]', unsafe_allow_html=False)
#st.write("Please enter your email, birthday and country:")    
# Input fields for email, birthday and country
email = st.text_input("Email:", "")
min_birthday = date.today() - timedelta(days=365*110)
max_birthday = date.today() - timedelta(days=365*14)
birthday = st.date_input("Birthday (MM/DD/YYYY):", value=datetime(2000, 1, 1), min_value=min_birthday, max_value=max_birthday)
countries = ["Select Country"] + sorted(["United States"] + [country.name for country in pycountry.countries if country.name != "United States"])
country = st.selectbox("Country:", countries)
st.markdown('---')     
st.markdown('##### The following section explores a range of topics, \
            including beliefs, practices, interconnectedness, transcendent experiences, \
            and personal development.', unsafe_allow_html=False)


# In[ ]:





# In[82]:


server = '184.168.194.64'
database = 'op_mssql_mama'
username = 'op_papa'
password = 's3x9&B7t'

# Create the connection string
connection_str = f'mssql+pymssql://{username}:{password}@{server}/{database}'

# Create the database engine
engine = create_engine(connection_str)


# In[ ]:





# In[83]:


# Fetch questions and sections from the database
query = f"SELECT question_id, question_text, question_section             FROM spiritual_consciousness_questions             ORDER BY question_id"
questions = pd.read_sql(query, engine)
questions_tuples = list(questions.itertuples(index=False))

# Fetch answers from the database
query = f"SELECT question_id, answer_text, answer_value     FROM spiritual_consciousness_answers     ORDER BY question_id, answer_value"
answers = pd.read_sql(query, engine)
answers_tuples = list(answers.itertuples(index=False))


# In[ ]:





# In[84]:


options_dict = {}

for question_id, answer_text, answer_value in answers_tuples:
    if question_id not in options_dict:
        options_dict[question_id] = [("Select", None)]
    options_dict[question_id].append((answer_text, answer_value))


# In[ ]:





# In[88]:


responses = []

current_section = None
for question_id, question_text, question_section in questions_tuples:
    if current_section != question_section:
        st.markdown('---')
        st.markdown(f"##### {question_section}", unsafe_allow_html=False)
        current_section = question_section

    response = st.selectbox(
        question_text,
        options=[(text, value) for text, value in options_dict[question_id]],
        format_func=lambda option: option[0],
        key=question_id
        
    )
    responses.append(response[1])  # Store the answer value
    


# In[ ]:





# In[58]:


# Active user flag
#active = st.checkbox("Active user", value=True)

survey_id = 1  # You can change this to the ID of the desired survey


# In[ ]:





# In[98]:


st.markdown('##')

if st.button("Submit"):
      
    if all(response is not None for response in responses):
        if email and birthday and country:
            # Check if the user exists
            query = f"SELECT * FROM op_survey_users WHERE email = '{email}'"
            existing_user = pd.read_sql(query, engine)

            if existing_user.empty:
                # Save user information
                query = f"INSERT INTO op_survey_users (email, birthday, country) VALUES ('{email}', '{birthday}', '{country}')"
                engine.execute(query)

                # Get the user_id
                query = f"SELECT id FROM op_survey_users WHERE email = '{email}'"
                user_id = pd.read_sql(query, engine).iloc[0]['id']
            else:
                user_id = existing_user.iloc[0]['id']

            # Check if the user has already submitted this survey
            query = f"SELECT * FROM spiritual_consciousness_survey_responses WHERE user_id = {user_id} AND survey_id = {survey_id}"
            existing_response = pd.read_sql(query, engine)

            if existing_response.empty:
                
                with st.spinner("Please wait while we check your submission..."): 
                    
                    
                    # Check if all questions have been answered
                    if all(response is not None for response in responses):
                        # Calculate the total sum of the answer values
                        #total_sum_of_answers = sum([answer_value for _, _, answer_value in answers_tuples])

                        # Calculate the total value of the user's submission
                        total_value_of_user_submission = sum(responses)

                        # Calculate the total percentage of the user's answer submission
                        total_percentage_of_user_submission = (total_value_of_user_submission / 150) * 100      
        
                
                # Save responses
                for question_id, response in enumerate(responses, start=1):
                    query = f"INSERT INTO spiritual_consciousness_survey_responses (user_id, survey_id, question_id, response) VALUES ({user_id}, {survey_id}, {question_id}, {response})"
                    engine.execute(query)
                    
                # Insert the total_percentage_of_user_submission into the spiritual_consciousness_user_survey_score table
                query = f"INSERT INTO spiritual_consciousness_user_survey_score (user_id, survey_id, score) VALUES ({user_id}, {survey_id}, {total_percentage_of_user_submission})"
                engine.execute(query)

                st.success("Thank you for your submission!")
                st.info(f"Your spiritual consciousness is at the : {total_percentage_of_user_submission:.2f}%")
                st.balloons()
                
            else:
                st.warning("You have already submitted this survey. You cannot submit it more than once.")
        else:
            st.error("Please provide all required information.")     
    else:
        st.error("Please answer all questions before submitting the survey.")


# In[99]:


st.markdown('##')
st.markdown('---')


# In[100]:


col1, col2 = st.columns(2)
with col1:
   st.markdown(' :gray[2023 - openpeace.ai, all rights reserved.]', unsafe_allow_html=False)

with col2:
   st.markdown(' :gray[v - 0.1]', unsafe_allow_html=False)


# In[ ]:





# In[ ]:





# In[ ]:




