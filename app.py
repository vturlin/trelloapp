import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.src.Trello import Trello
from src.src.Trello import Archive
from src.src.Trello import New_card

instance = Trello('64fad2cf7a0b956876c755be')
data = instance.cards
tag_list = data['id_list'].unique()
client_list = data['client'].unique()
Labels = ['GTM', 'GA4', 'PREZ', 'SUPPORT', 'LOOKER STUDIO', 'PRESTA', 'INTERNE', 'PDM', 'PRIVACY']

# Streamlit part
st.set_page_config(
    initial_sidebar_state="expanded",
    layout="wide")
st.image('https://www.d-edge.com/wp-content/themes/d-edge/img/logo_d-edge-white.svg', width=200)
st.title("D-Agency - Data & Measurement - Trello App")


#sidebar (membre)
with st.sidebar:
    st.subheader('Filter the dashboard', divider='rainbow')
    members_filter = st.multiselect(label='Member', options=['VT', 'OB', 'JF'])
    tag_list_filter = st.multiselect(label='Tag', options=tag_list)
    clients_list_filter = st.multiselect(label='Client', options=client_list)
    members_filter = members_filter if len(members_filter) > 0 else ['VT', 'OB', 'JF']
    tag_list_filter = tag_list_filter if len(tag_list_filter) > 0 else tag_list
    clients_list_filter = clients_list_filter if len(clients_list_filter) > 0 else client_list
    # ajout de l'élément de création de carte
    st.subheader('Create a new card',divider='rainbow')
    card_task = st.selectbox(label='Select task type', options=['IMPLE', 'DASH','PREZ','CONFIG'])
    card_client = st.text_input('Client',value='',placeholder='D-EDGE').upper()
    card_title_desc = st.text_input('Task description',value='',placeholder='Task to be done')
    estimated_time = st.text_input('Estimated time',value='',placeholder='0,5')
    quoted_amount = st.text_input('Quoted amount',value='',placeholder='300')
    tag_list_id = st.selectbox(label='Select a list', options=tag_list)
    label_list = st.multiselect(label='Select tags', options=Labels)
    card_members = st.multiselect(label='Select members', options=['VT', 'OB', 'JF'])
    due_date = st.text_input('Due date',value='',placeholder='yyyy-mm-dd')
    
    if st.button('Create card'):
        card_title = '['+card_client+']['+card_task+'] - '+card_title_desc
        card_desc = 'Client: '+card_client+'\n\nTemps estimé: '+estimated_time+'\n\nTemps passé:\n\nDevis: '+quoted_amount+'\n\nFacture:\n\nContact:\n\nCommentaire:'
        new_card_instance = New_card(card_title, card_desc, tag_list_id, card_members,label_list,due_date)
        new_card_instance.new_card()

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
def plot_bar_chat(
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

# Fonction de création d'une line chart
def plot_line_chat(
    line_data,
    x='',
    y='',
    title='',
    layout_color='',    
):
    fig = px.line(line_data, x, y, height=400)
    fig.add_trace(go.Scatter(x=line_data[x], y=line_data[y], mode='lines',line=dict(color='#f10096',)))

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

# Partie sur la création des dataframes utilisés pour les différentes visualisations

# Creation d'un dataframe filtré afin d'exclure les cartes archivées
df = dataframe
mask = df['id_list'].str.contains('ARCHIVE 2023')
active_task_df = df[~mask]

# DataFrame sur le nombre d'utilisation des Labels
df = dataframe
df_card_cat = df.drop(['card_name', 'due_date', 'start_date','id_members', 'id_list', 
            'items_completed', 'items_amount','SUPPORT', 
            'PRESTA', 'INTERNE','client', 
            'estimated_spent_time', 'final_time_spent','proposal_price', 'sale_price', 
            'ticket_duration', 'card_invoiced','card_completion_rate'],axis=1)
melted_df = df_card_cat.melt(var_name='Column', value_name='Value')
result_df = melted_df.groupby('Column')['Value'].sum().reset_index()
result_df.columns = ['Labels', 'Card_count']

# DataFrame sur le nombre d'utilisation de type de card
df = dataframe
df_card_type = df.drop(['card_name', 'due_date', 'start_date','id_members', 'id_list', 
            'items_completed', 'items_amount', 'GTM', 'GA4','PREZ', 
            'LOOKER STUDIO', 'PDM','PRIVACY', 'client', 
            'estimated_spent_time', 'final_time_spent','proposal_price', 'sale_price', 
            'ticket_duration', 'card_invoiced','card_completion_rate'],axis=1)
melted_df = df_card_type.melt(var_name='Column', value_name='Value')
card_type_df = melted_df.groupby('Column')['Value'].sum().reset_index()
card_type_df.columns = ['Types', 'Card_count']

# Ajout un DataFrame pour le nombre de carte par client
df = dataframe
card_client_df = df.groupby('client').agg({'card_name': 'count', 'sale_price': 'sum'}).reset_index()
card_client_df.columns = ['Clients', 'Card_count','invoice']

# Ajout un DataFrame de cartes par due date
df = dataframe
due_date_df = df.groupby('due_date')['card_name'].count().reset_index()
due_date_df.columns = ['Due date', 'Taches']



# Partie sur l'ajout des vizualisations au streamlit

# Cartes actives
st.header('Active tasks', help='Tasks currently in progress or recently completed',divider='rainbow')

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

plot_bar_chat(due_date_df,'Due date','Taches','Taches par date de livraison',"#67518e")

# Partie sur l'activité de l'année
st.header('This year activity', divider='rainbow')

# Scorecards
st.subheader('Workload focus', divider='grey')
col1, col2, col3, col4 ,col5 = st.columns((1,1,1,1,1))
with col1:
    plot_metric(len(dataframe),'Tasks','','#3a2363')    
with col2:
    estimated_time = dataframe['estimated_spent_time'].sum()
    plot_metric(estimated_time,'Estimated work load','days',"#3a2363") 
with col3:
    work_load = dataframe['final_time_spent'].sum()
    plot_metric(total_proposal_price,'Time spent','days','#3a2363')
with col4:
    filtered_df_done = active_task_df[active_task_df['id_list'] != 'DONE']
    estimated_work_remaning = filtered_df_done['estimated_spent_time'].sum()
    plot_metric(estimated_work_remaning,'Remaining work','days','#3a2363')
with col5:
    avg_task_duration = dataframe['ticket_duration'].sum() / dataframe['card_name'].count()
    plot_metric(avg_task_duration,'Avg task duration','days','#3a2363')

col1, col2 = st.columns((1,1))
with col1:
    plot_bar_chat(result_df,'Labels','Card_count','Carte par labels',"#67518e")
with col2:
    plot_bar_chat(card_type_df,'Types','Card_count','Carte par types','#573e82')

st.subheader('Business focus', divider='grey')
col1, col2, col3, col4 ,col5 = st.columns((1,1,1,1,1))
with col1:
    count_done_archive = df['id_list'].str.count(r'(DONE|ARCHIVE 2023)').sum()
    plot_metric(count_done_archive,'Completed tasks','','#3a2363')    
with col2:
    total_proposal_price = dataframe['proposal_price'].sum()
    plot_metric(total_proposal_price,'Total quoted','€','#3a2363')
with col3:
    total_sale_price = dataframe['sale_price'].sum()
    plot_metric(total_sale_price,'Total invoice','€',"#3a2363") 
with col4:
    total_invoiced_card = dataframe['card_invoiced'].sum()
    plot_metric(total_invoiced_card,'Invoiced tasks','','#3a2363')
with col5:
    avg_invoiced = dataframe['sale_price'].sum()//dataframe['card_invoiced'].sum()
    plot_metric(avg_invoiced,'Avg invoiced amount','€','#3a2363')

plot_bar_chat(card_client_df,'Clients','Card_count','Tasks per client','#3a2363')

col1, col2 = st.columns((1,1))
with col1:
    filtered_df = card_client_df[card_client_df['invoice'] != 0]
    plot_bar_chat(filtered_df,'Clients','invoice',' Invoiced amount per client',"#67518e")
with col2:
    filtered_df = card_client_df[card_client_df['invoice'] != 0]
    plot_pie_chart(filtered_df['Clients'],filtered_df['invoice'],'Revenue per clients','#573e82')

# Affichage de tout le dataframe
st.header('Overall view', divider='rainbow')
dataframe