import streamlit as st
import pandas as pd
from src.src.Trello import Trello
from src.src.Trello import New_card

instance = Trello('64fad2cf7a0b956876c755be')
data = instance.cards
tag_list = data['id_list'].unique()
client_list = data['client'].unique()
Labels = ['GTM', 'GA4', 'PREZ', 'SUPPORT', 'LOOKER STUDIO', 'PRESTA', 'INTERNE', 'PDM', 'PRIVACY','DEVIS','META','MEDIAGENIUS','R&D']


# Streamlit part
st.set_page_config(
    page_title='HOME',
    page_icon=':house:',
    initial_sidebar_state="expanded",
    layout="wide")
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.image('https://www.d-edge.com/wp-content/themes/d-edge/img/logo_d-edge-white.svg', width=200)
page_title='<p class="head">Data & Measurement - Trello App - HOME</p>'
st.markdown(page_title, unsafe_allow_html=True)


st.subheader('')
first_title = '<p class="title">INTRODUCTION</p>'
st.markdown(first_title, unsafe_allow_html=True)
st.subheader('',divider='rainbow')
intro_text = '<p class="para">In this TRELLO APP you will access the global reporting for the Data & Measurement Team activity.</p>'
intro_text_2 = '<p class="para">The CURRENT TAKS report focus on the workload repartition over time and team members.</p>'
intro_text_3 = '<p class="para">The THIS YEAR ACTIVITY report focus on the amount of taks handled during the year and a revenue and business analysis per type of services and clients.</p>'
st.markdown(intro_text, unsafe_allow_html=True)
st.markdown(intro_text_2, unsafe_allow_html=True)
st.markdown(intro_text_3, unsafe_allow_html=True)

st.subheader('')
second_title = '<p class="title">NEW TASK</p>'
st.markdown(second_title, unsafe_allow_html=True, help='You can create a new Trello card here by filling all the required fields and click on Create card')
st.subheader('',divider='rainbow')
with st.form(key='Card creation'):

    original_title = '<p class="subtitle">TITLE</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns((1,1,1,1),gap='large')
    with c1:
        card_task = st.selectbox(label='Select task type', options=['IMPLE', 'DASH','PREZ','CONFIG'])
    with c2:
        card_client = st.text_input('Client',value='',placeholder='D-EDGE').upper()
    with c3:
        card_title_desc = st.text_input('Task description',value='',placeholder='Task to be done')

    original_tags = '<p class="subtitle">DESCRIPTION</p>'
    st.markdown(original_tags, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns((1,1,1,1),gap='large')
    with col1:
        card_priority = st.selectbox(label='Priority level', options=['0','1', '2','3'])
    with col2:
        estimated_time = st.text_input('Estimated time',value='',placeholder='0,5')
    with col3:
        quoted_amount = st.text_input('Quoted amount',value='',placeholder='300')

    original_description = '<p class="subtitle">TAGS</p>'
    st.markdown(original_description, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns((1,1,1,1),gap='large')
    with col1:
        tag_list_id = st.selectbox(label='Select a list', options=tag_list)
    with col2:
        label_list = st.multiselect(label='Select tags', options=Labels)
    with col3:
        card_members = st.multiselect(label='Select members', options=['VT', 'OB', 'JF'])

    original_description = '<p class="subtitle">DATES</p>'
    st.markdown(original_description, unsafe_allow_html=True)
    col1, col2, col3 = st.columns((1,1,2),gap='large')
    with col1:
        start_date = st.date_input('Start date',value="today",format='YYYY-MM-DD')
    with col2:
        due_date = st.date_input('Due date',value="today",format='YYYY-MM-DD')
    submit = st.form_submit_button('Creat Card')

if submit:
    card_title = '['+card_client+']['+card_task+'] - '+card_title_desc
    card_desc = 'Client: '+card_client+'\n\nPriority level:'+card_priority+'\n\nTemps estimé: '+estimated_time+'\n\nTemps passé:\n\nDevis: '+quoted_amount+'\n\nFacture:\n\nContact:\n\nCommentaire:'
    new_card_instance = New_card(card_title, card_desc, tag_list_id, card_members,label_list,due_date,start_date)
    new_card_instance.new_card()

st.subheader('')
third_title = '<p class="title">OVERVIEW</p>'
st.markdown(third_title, unsafe_allow_html=True)
st.subheader('',divider='rainbow')
global_df = data
summary_df = global_df.drop(['GTM', 'GA4', 'PREZ', 'SUPPORT', 'LOOKER STUDIO', 'PRESTA', 'INTERNE', 'PDM', 'PRIVACY','DEVIS','META','MEDIAGENIUS','card_invoiced','R&D'],axis=1)
summary_df