import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.src.Trello import Trello
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles
from venn import venn

instance = Trello('64fad2cf7a0b956876c755be')
data = instance.cards
tag_list = data['id_list'].unique()
client_list = data['client'].unique()
Labels = ['GTM', 'GA4', 'PREZ', 'SUPPORT', 'LOOKER STUDIO', 'PRESTA', 'INTERNE', 'PDM', 'PRIVACY','DEVIS','META','MEDIAGENIUS','R&D','GADS','TIKTOK']

# Streamlit part
st.set_page_config(
    page_title='THIS YEAR ACTIVITY',
    page_icon='chart_with_upwards_trend',
    initial_sidebar_state="expanded",
    layout="wide")
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
st.image('https://www.d-edge.com/wp-content/themes/d-edge/img/logo_d-edge-white.svg', width=200)
page_title='<p class="head">Data & Measurement - Trello App - THIS YEAR ACTIVITY</p>'
st.markdown(page_title, unsafe_allow_html=True)


#sidebar (membre)
with st.sidebar:
    sidebar_title = '<p class="subtitle">FILTERS</p>'
    st.markdown(sidebar_title, help='Apply filter to the whole report here by selecting the required value on each fields', unsafe_allow_html=True)
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
    fig = px.bar(chart_data, x=x, y=y, color=color, height=400)

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
def plot_line_chart(
    line_data,
    x='',
    y='',
    title='',
    layout_color='',
    lengend = '',    
):
    fig = px.line(line_data, x, y, height=400)
    fig.add_trace(go.Scatter(x=line_data[x], y=line_data[y], name = legend, mode='lines', line=dict(color='#f10096',)))

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
    night_colors = ['rgb(128, 139, 164)', 'rgb(255, 83, 150)', 'rgb(246, 109, 0)',
                'rgb(36, 55, 57)', 'rgb(6, 4, 4)']

    #fig = px.pie(pie_data, values=values, names=names, color_discrete_sequence=px.colors.sequential.Burg.height=400)
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
      set_labels = (d1_name, d2_name, d3_name),
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
    fig, ax = plt.subplots(1, figsize=(16.12))
    venn(sets,fmt="{percentage:.1f}%", ax=ax)
    plt.legend(labels[:4], ncol=6)
    st.pyplot(plt.gcf())

# Partie sur la création des dataframes utilisés pour les différentes visualisations

# Creation d'un dataframe filtré afin d'exclure les cartes archivées
df = dataframe
mask = df['id_list'].str.contains('ARCHIVE 2023')
active_task_df = df[~mask]

# DataFrame sur le nombre d'utilisation des Labels
df_card_cat = dataframe

def check_tracking(labels):
    tracking_values = ['GA4', 'GTM', 'PDM', 'PRIVACY']
    return 1 if any(label in tracking_values for label in labels) else 0

def check_media(labels):
    tracking_values = ['MEDIAGENIUS', 'META', 'GADS','TIKTOK']
    return 1 if any(label in tracking_values for label in labels) else 0

def check_agency(labels):
    tracking_values = ['PREZ', 'DEVIS', 'R&D']
    return 1 if any(label in tracking_values for label in labels) else 0

df_card_cat['TRACKING'] = df_card_cat['card_labels'].apply(check_tracking)
df_card_cat['MEDIA'] = df_card_cat['card_labels'].apply(check_media)
df_card_cat['AGENCY'] = df_card_cat['card_labels'].apply(check_agency)

df_card_cat = df.drop(['card_name', 'due_date', 'start_date','id_members', 'id_list', 'card_labels',
            'items_completed', 'items_amount','SUPPORT','GA4', 'GTM', 'PDM', 'PRIVACY','GADS','TIKTOK',
            'PRESTA', 'INTERNE','client', 'priority','PREZ', 'DEVIS', 'R&D','MEDIAGENIUS', 'META',
            'estimated_spent_time', 'final_time_spent','proposal_price', 'sale_price', 
            'ticket_duration', 'card_invoiced','card_completion_rate'],axis=1)

melted_df = df_card_cat.melt(var_name='Column', value_name='Value')
result_df = melted_df.groupby('Column')['Value'].sum().reset_index()
result_df.columns = ['Labels', 'Tasks']


# DataFrame sur le nombre d'utilisation de type de card
df = dataframe
df_card_type = df.drop(['card_name', 'due_date', 'start_date','id_members', 'id_list','card_labels',
            'items_completed', 'items_amount', 'GTM', 'GA4','PREZ','GADS','TIKTOK',
            'LOOKER STUDIO', 'PDM','PRIVACY', 'client','priority',
            'estimated_spent_time', 'final_time_spent','proposal_price', 'sale_price', 
            'ticket_duration', 'card_invoiced','card_completion_rate'],axis=1)
melted_df = df_card_type.melt(var_name='Column', value_name='Value')
card_type_df = melted_df.groupby('Column')['Value'].sum().reset_index()
card_type_df.columns = ['Types', 'Tasks']

# Ajout un DataFrame pour le nombre de carte par client
df = dataframe
card_client_df = df.groupby('client').agg({'card_name': 'count', 'sale_price': 'sum'}).reset_index()
card_client_df.columns = ['Clients', 'Card_count','invoice']

# Ajout un DataFrame de cartes par due date
df = active_task_df
filtered_due_date_df = df[df['id_list'] != 'DONE']
due_date_df = filtered_due_date_df.groupby(['due_date','priority'])['card_name'].count().reset_index()
due_date_df.columns = ['Due date','priority','Taches']

# Ajout d'un graph pour overlap des type de carte
global_df = data
df = global_df
d1 = df[~df['PRESTA'].isnull()].index.tolist()
d2 = df[~df['SUPPORT'].isnull()].index.tolist()
d3 = df[~df['INTERNE'].isnull()].index.tolist()
d4 = df[~df['GTM'].isnull()].index.tolist()
d5 = df[~df['GA4'].isnull()].index.tolist()
d6 = df[~df['LOOKER STUDIO'].isnull()].index.tolist()
d7 = df[~df['PREZ'].isnull()].index.tolist()
d8 = df[~df['PRIVACY'].isnull()].index.tolist()
d9 = d4 + d5


# Partie sur l'ajout des vizualisations au streamlit
 
# Partie sur l'activité de l'année
first_title = '<p class="subtitle">WORKLOAD FOCUS</p>'
st.markdown(first_title, unsafe_allow_html=True)
st.subheader('',divider='rainbow')

col1, col2, col3, col4, col5 = st.columns((1,1,1,1,1))
with col1:
    plot_metric(len(dataframe),'Tasks','','#3a2363')    
with col2:
    estimated_time = dataframe['estimated_spent_time'].sum()
    plot_metric(estimated_time,'Estimated work load',' days',"#3a2363") 
with col3:
    work_load = dataframe['final_time_spent'].sum()
    plot_metric(work_load,'Time spent',' days','#3a2363')
with col4:
    filtered_df_done = active_task_df[active_task_df['id_list'] != 'DONE']
    estimated_work_remaning = filtered_df_done['estimated_spent_time'].sum()
    plot_metric(estimated_work_remaning,'Remaining work',' days','#3a2363')
with col5:
    avg_task_duration = dataframe['ticket_duration'].sum() / dataframe['card_name'].count()
    plot_metric(avg_task_duration,'Avg task duration',' days','#3a2363')

col1, col2 = st.columns((1,1))
with col1:
    plot_bar_chart(result_df,'Labels','Tasks','Tasks per labels',"#67518e")
with col2:
    plot_bar_chart(card_type_df,'Types','Tasks','Carte par types','#573e82')

col1, col2 = st.columns((1,1))
with col1:
    section_title = '<p class="subsection">Support focus</p>'
    st.markdown(section_title, unsafe_allow_html=True)
    st.subheader('',divider='grey')
    support_tasks = df['SUPPORT'].sum()
    plot_metric(support_tasks,'Support Tasks','','#3a2363')
    new_venn3_chart(d1,d2,d3,'PRESTA','SUPPORT','INTERNE','Support per task type','#3a2363')
with col2:
    section_title = '<p class="subsection">Consulting focus</p>'
    st.markdown(section_title, unsafe_allow_html=True)
    st.subheader('',divider='grey')
    presta_tasks = df['PRESTA'].sum()
    plot_metric(presta_tasks,'Consulting tasks','','#3a2363')
    new_venn3_chart(d6,d1,d9,'DASHBOARDING','PRESTA','IMPLE','Implementation tasks','#67518e')

first_title = '<p class="subtitle">BUSINESS FOCUS</p>'
st.markdown(first_title, unsafe_allow_html=True)
st.subheader('', divider='rainbow')
col1, col2, col3, col4, col5 = st.columns((1,1,1,1,1))
with col1:
    count_done_archive = df['id_list'].str.count(r'(DONE|ARCHIVE 2023)').sum()
    plot_metric(count_done_archive,'Completed tasks','','#3a2363')    
with col2:
    total_proposal_price = dataframe['proposal_price'].sum()
    plot_metric(total_proposal_price,'Total quoted','€','#3a2363')
with col3:
    total_sale_price = dataframe['sale_price'].sum()
    plot_metric(total_sale_price,'Total invoiced','€',"#3a2363") 
with col4:
    total_invoiced_card = dataframe['card_invoiced'].sum()
    plot_metric(total_invoiced_card,'Invoiced tasks','','#3a2363')
with col5:
    avg_invoiced = dataframe['sale_price'].sum()//dataframe['card_invoiced'].sum()
    plot_metric(avg_invoiced,'Avg invoiced amount','€','#3a2363')

plot_bar_chart(card_client_df,'Clients','Card_count','Tasks per client','#3a2363')

col1, col2 = st.columns((1,1))
with col1:
    filtered_df = card_client_df[card_client_df['invoice'] != 0]
    plot_bar_chart(filtered_df,'Clients','invoice',' Invoiced amount per client',"#67518e")
with col2:
    filtered_df = data
    filtered_df = filtered_df[~filtered_df['SUPPORT'].isnull()]
    filtered_df = filtered_df.groupby('card_invoiced').agg({'card_name': 'count', 'sale_price': 'sum'}).reset_index()
    filtered_df['card_invoiced'] = filtered_df['card_invoiced'].replace({0: 'free support', 1: 'invoiced support'})
    plot_pie_chart(filtered_df['card_invoiced'],filtered_df['card_name'],'Invoiced support ratio','#573e82')


col1, col2 = st.columns((1,1))
with col1:

    new_venn3_chart(d7,d2,d9,'DASH','SUPPORT','IMPLE','Other support','#3a2363')
with col2:
    new_venn3_chart(d6,d1,d9,'DASHBOARDING','PRESTA','IMPLE','Implementation tasks','#67518e')
