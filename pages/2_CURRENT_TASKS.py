import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.src.Trello import Trello
from src.src.Trello import Archive
from src.src.Trello import New_card
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles
from venn import venn

instance = Trello('64fad2cf7a0b956876c755be')
data = instance.cards
tag_list = data['id_list'].unique()
client_list = data['client'].unique()
Labels = ['GTM', 'GA4', 'PREZ', 'SUPPORT', 'LOOKER STUDIO', 'PRESTA', 'INTERNE', 'PDM', 'PRIVACY','DEVIS','META','MEDIAGENIUS','R&D']

# Streamlit part
st.set_page_config(
    page_title='CURRENT TASKS',
    page_icon='chart_with_upwards_trend',
    initial_sidebar_state="expanded",
    layout="wide")
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.image('https://www.d-edge.com/wp-content/themes/d-edge/img/logo_d-edge-white.svg', width=200)
page_title='<p class="head">Data & Measurement - Trello App - CURRENT TAKS</p>'
st.markdown(page_title, unsafe_allow_html=True)


#sidebar (membre)
with st.sidebar:
    sidebar_title = '<p class="subtitle">FILTERS</p>'
    st.markdown(sidebar_title,help='Apply filter to the whole report here by selecting the required value on each fields', unsafe_allow_html=True)
    st.subheader('', divider='rainbow')
    members_filter = st.multiselect(label='Member', options=['VT', 'OB', 'JF'])
    tag_list_filter = st.multiselect(label='Tag', options=tag_list)
    clients_list_filter = st.multiselect(label='Client', options=client_list)
    members_filter = members_filter if len(members_filter) > 0 else ['VT', 'OB', 'JF']
    tag_list_filter = tag_list_filter if len(tag_list_filter) > 0 else tag_list
    clients_list_filter = clients_list_filter if len(clients_list_filter) > 0 else client_list
    
with st.container():
    dataframe = data
    filtered_values = np.where(dataframe['id_members'].apply(lambda id: any(member in id for member in members_filter))
                               & dataframe['id_list'].isin(tag_list_filter) 
                               & dataframe['client'].isin(clients_list_filter))
    dataframe = data.iloc[filtered_values]


# Fonction de création d'une scorecard
def plot_metric(
    value,
    title='',
    suffix='',
    layout_color='',
):
    fig = go.Figure()
    fig.add_trace(
    go.Indicator(
        value=value,
        number={
                "suffix": suffix,
                "font.size": 20,
            },
        title={
                "text": title,
                "font": {"size": 15},
        },
        domain={'row': 1, 'column': 1},
    )
)
    fig.update_layout(
     paper_bgcolor=layout_color,
     plot_bgcolor=layout_color,
     margin=dict(t=30, b=0),
     showlegend=False,
     height=100,
    )
    st.plotly_chart(fig, use_container_width = True)

# Fontion de création d'un chart en histogramme
def plot_bar_chart(
    chart_data,
    x='',
    y='',
    title='',
    layout_color='',   
):
    fig = px.bar(chart_data, x, y, height=400)
    fig.update_traces(
        marker_color='#ffffff',  # Change bar color
    )

    fig.update_layout(
        title=title,
        paper_bgcolor=layout_color,
        plot_bgcolor=layout_color, 
         margin=dict(
            l=20,
            r=10,
        ),
    )
    st.plotly_chart(fig,use_container_width=True)

def plot_bar_color_chart(
    chart_data,
    x='',
    y='',
    title='',
    layout_color='',color=''):
    fig = px.bar(chart_data, x=x, y=y,color=color, height=400)

    fig.update_layout(
        title=title,
        paper_bgcolor=layout_color,
        plot_bgcolor=layout_color, 
         margin=dict(
            l=20,
            r=10,
        ),
    )
    st.plotly_chart(fig,use_container_width=True)

# Fonction de création d'une line chart
def plot_line_chat(
    line_data,
    x='',
    y='',
    title='',
    layout_color='',
    lengend = '',    
):
    fig = px.line(line_data, x, y, height=400)
    fig.add_trace(go.Scatter(x=line_data[x], y=line_data[y],name = legend, mode='lines',line=dict(color='#f10096',)))

    fig.update_layout(
        title=title,
        paper_bgcolor=layout_color,
        plot_bgcolor=layout_color,
         margin=dict(
            l=20,
            r=10,
        ),
    )
    st.plotly_chart(fig,use_container_width=True)

#Fonction pour créer un pie chart
def plot_pie_chart(
    labels,
    values='',
    title='',
    layout_color='',
):
    night_colors = ['rgb(0, 215, 176)', 'rgb(255, 83, 150)', 'rgb(246, 109, 0)',
                'rgb(36, 55, 57)', 'rgb(6, 4, 4)']

    #fig = px.pie(pie_data, values=values, names=names, color_discrete_sequence=px.colors.sequential.Burg,height=400)
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value',
                  marker=dict(colors=night_colors))
    fig.update_layout(
        title=title,
        paper_bgcolor=layout_color,
        plot_bgcolor=layout_color,
        margin=dict(
            l=20,
            r=10,
            t=60,
        ), 
        height=400,
        )
    st.plotly_chart(fig,use_container_width=True)

def new_venn3_chart(
    d1,
    d2,
    d3,
    d1_name,
    d2_name,
    d3_name, title = '',color=''):
    fig = plt.figure(facecolor=color)

    venn3_instance = venn3([set(d1), set(d2), set(d3)],
      set_colors=('#13bbce', '#ff5396', '#00d7b0'), 
      set_labels = (d1_name,d2_name,d3_name),
      #fontsize=8,
      alpha=0.3)
    venn3_circles([set(d1), set(d2), set(d3)], lw=0.7)
    
    plt.title(title, color = 'white')
    

    st.pyplot(plt.gcf())

def new_venn5_chart(
    d1,
    d2,
    d3,
    d4,
    d1_name,d2_name,d3_name,d4_name):
    labels = [d1_name,d2_name,d3_name,d4_name]
    plt.figure(facecolor="#3a2363")
    sets = {
        labels[0]: set(d1),
        labels[1]: set(d2),
        labels[2]: set(d3),
        labels[3]: set(d4),
    }
    fig, ax = plt.subplots(1, figsize=(16,12))
    venn(sets,fmt="{percentage:.1f}%", ax=ax)
    plt.legend(labels[:4], ncol=6)
    st.pyplot(plt.gcf())

# Partie sur la création des dataframes utilisés pour les différentes visualisations

# Creation d'un dataframe filtré afin d'exclure les cartes archivées
df = dataframe
mask = df['id_list'].str.contains('ARCHIVE 2023')
active_task_df = df[~mask]

# DataFrame sur le nombre d'utilisation des Labels
df = active_task_df
df_card_cat = df.drop(['card_name', 'due_date', 'start_date','id_members', 'id_list','card_labels',
            'items_completed', 'items_amount','SUPPORT',
            'PRESTA', 'INTERNE','client',
            'estimated_spent_time', 'final_time_spent','proposal_price', 'sale_price', 
            'ticket_duration', 'card_invoiced','card_completion_rate'],axis=1)
melted_df = df_card_cat.melt(id_vars=['priority'], var_name='Column', value_name='Value')
# Group by 'Column' and 'priority' and sum the 'Value' column
result_df = melted_df.groupby(['Column', 'priority'])['Value'].sum().reset_index()
result_df.columns = ['Labels', 'Priority', 'Tasks']

# Ajout un DataFrame de cartes par due date et priority
df = active_task_df
filtered_due_date_df = df[df['id_list'] != 'DONE']
due_date_df = filtered_due_date_df.groupby(['due_date','priority'])['card_name'].count().reset_index()
due_date_df.columns = ['Due date','Priority','Tasks']

# Ajout un DataFrame de cartes par client et priority
df = active_task_df
filtered_client_df = df[df['id_list'] != 'DONE']
client_df = filtered_due_date_df.groupby(['client','priority'])['card_name'].count().reset_index()
client_df.columns = ['Clients','Priority','Tasks']

# Ajout un DataFrame de cartes par type et priority
df = active_task_df
filtered_client_df = df[df['id_list'] != 'DONE']
client_df = filtered_due_date_df.groupby(['client','priority'])['card_name'].count().reset_index()
client_df.columns = ['Clients','Priority','Tasks']


# Cartes actives
first_title = '<p class="title">ACTIVE TASKS</p>'
st.markdown(first_title,help='Tasks currently in progress or recently completed', unsafe_allow_html=True)
st.subheader('',divider='rainbow')
# Scorecards
col1, col2, col3, col4 ,col5 = st.columns((1,1,1,1,1))
with col1:
    plot_metric(len(active_task_df),'Active tasks','','#3a2363')   
with col2:
    total_proposal_price = (active_task_df['items_completed'].sum()/dataframe['items_amount'].sum())*100
    plot_metric(total_proposal_price,'Tasks completion rate','%','#3a2363')
with col3:
    total_sale_price = active_task_df['proposal_price'].sum()
    plot_metric(total_sale_price,'Quoted amount','€',"#3a2363")    
with col4:
    total_invoiced_card = active_task_df['card_invoiced'].sum()
    plot_metric(total_invoiced_card,'Invoiced tasks','','#3a2363')
with col5:
    #Ajout d'un bouton pour archiver les cartes done
        if st.button('Archive tasks'):
            Archive()
            st.write('Completed tasks added to archive')
        else:
            done_cards = active_task_df['id_list'].str.count('DONE').sum()
            cards_to_achive = str(done_cards)+' completed tasks to archive'
            st.write(cards_to_achive)

plot_bar_color_chart(due_date_df,'Due date','Tasks','Tasks per due date',"#67518e",'Priority')

col1, col2 = st.columns((1,1))
with col1:
    plot_bar_color_chart(client_df,'Clients','Tasks','Tasks per client',"#573e82",'Priority')
with col2:
    plot_bar_color_chart(result_df,'Labels','Tasks','Tasks per type',"#67518e",'Priority')
