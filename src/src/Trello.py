from dotenv import dotenv_values
import numpy as np
import pandas as pd 
import requests
import json

class New_card():
    API_KEY = dotenv_values().get('API_KEY')
    API_TOKEN = dotenv_values().get('API_TOKEN')
    TAG_MAPPING = {
        '64fad2cfc35b447f879e00ad': 'BACKLOG',
        '64fad2cfb7e4d6bda221529b': 'TO DO',
        '64fad2cfd2da8c92cbd88e54': 'WIP',
        '64fad316fab90f193c99ec3e': 'STAND BY',
        '64faf062715bbc35238317b5': 'TO FOLLOW UP',
        '650324d427eaa6d69da3b62c': 'ARCHIVE 2023',
        '64fad30a467a1515aaa4d19e': 'DONE',
        '6500521cddb16e0312704306': 'TEMPLATE'}

    ID_MAPPING = {
        '64fad23e39bba595108b4116': 'VT',
        '625fd31f68b0f364de2796b7': 'JF',
        '64fb35ac0cf8e80acd39291f': 'OB'
        }

    LABELS_MAPPING = {
            "650869bf843c76f75f5fe886":"PRESTA",
            "64fad2cf4410395e0db82bce":"GTM",
            "64fad2cf4410395e0db82bdb":"GA4",
            "65086988c490b2ced7eb1ca3":"SUPPORT",
            "64fad2cf4410395e0db82bd0":"LOOKER STUDIO",
            "65086a4212208eea6a92021b":"INTERNE",
            "64fad2cf4410395e0db82bdf":"PREZ",
            "64fad2cf4410395e0db82be5":"PRIVACY",
            "64fad2cf4410395e0db82bd7":"PDM",
            "650162349e4c8587cc3e57ba":"META",
            "64fb448c932053f3be0f150e":"DEVIS",
            "6530f0b553b834de934d3903":"R&D",
            "652d248403d22038f5dcf1c9":"GADS",
            "653b6842b1a9cfdb85020a8e": "TIKTOK",



        }

    def __init__(self,title,desc,idList,idMembers,idlabels,dueDate,startDate):
        self.title = title
        self.desc = desc
        self.idList = self.get_idList(idList)
        self.idMembers = self.get_idMembers(idMembers)
        self.idLabels = self.get_idLabels(idlabels)
        self.dueDate = dueDate
        self.startDate = startDate

    def get_idList(self, idList):
        TAG_MAPPING = {
        '64fad2cfc35b447f879e00ad': 'BACKLOG',
        '64fad2cfb7e4d6bda221529b': 'TO DO',
        '64fad2cfd2da8c92cbd88e54': 'WIP',
        '64fad316fab90f193c99ec3e': 'STAND BY',
        '64faf062715bbc35238317b5': 'TO FOLLOW UP',
        '650324d427eaa6d69da3b62c': 'ARCHIVE 2023',
        '64fad30a467a1515aaa4d19e': 'DONE',
        '6500521cddb16e0312704306': 'TEMPLATE'}
        return next((key for key, value in TAG_MAPPING.items() if value == idList), None)
        
    def get_idMembers(self, idMembers):
        ID_MAPPING = {
        '64fad23e39bba595108b4116': 'VT',
        '625fd31f68b0f364de2796b7': 'JF',
        '64fb35ac0cf8e80acd39291f': 'OB'
        }
        id_member_list = []
        for id_member in idMembers:
            matching_ids = [key for key, value in self.ID_MAPPING.items() if value == id_member]
            id_member_list.extend(matching_ids)
        return id_member_list
    
    def get_idLabels(self, idLabels):
        LABELS_MAPPING = {
            "650869bf843c76f75f5fe886":"PRESTA",
            "64fad2cf4410395e0db82bce":"GTM",
            "64fad2cf4410395e0db82bdb":"GA4",
            "65086988c490b2ced7eb1ca3":"SUPPORT",
            "64fad2cf4410395e0db82bd0":"LOOKER STUDIO",
            "65086a4212208eea6a92021b":"INTERNE",
            "64fad2cf4410395e0db82bdf":"PREZ",
            "64fad2cf4410395e0db82be5":"PRIVACY",
            "64fad2cf4410395e0db82bd7":"PDM",
            "650162349e4c8587cc3e57ba":"META",
            "64fb448c932053f3be0f150e":"DEVIS",
            "6530f0b553b834de934d3903":"R&D",
            "652d248403d22038f5dcf1c9":"GADS",
            "653b6842b1a9cfdb85020a8e": "TIKTOK",
        }
        id_label_list = []
        for id_label in idLabels:
            matching_labels = [key for key, value in self.LABELS_MAPPING.items() if value == id_label]
            id_label_list.extend(matching_labels)
        return id_label_list

    def new_card(self):
        url = "https://api.trello.com/1/cards"
        headers = {
            "Accept": "application/json"
        }

        query = {
            'idList': self.idList,
            'key': self.API_KEY,
            'token': self.API_TOKEN,
            'name': self.title,
            'desc': self.desc,
            'idMembers': self.idMembers,
            'idLabels': self.idLabels,
            'due':self.dueDate,
            'start':self.startDate,
            'idCardSource':'650dadd093b0f8b4efc7e0fa',
            'keepFromSource':'checklists'
        }
        
        response = requests.request("POST",url, headers=headers, params=query)                                                        
       
class Archive():
    API_KEY = dotenv_values().get('API_KEY')
    API_TOKEN = dotenv_values().get('API_TOKEN')
    url = "https://api.trello.com/1/lists/64fad30a467a1515aaa4d19e/moveAllCards"

    query = {
        'idBoard': '64fad2cf7a0b956876c755be',
        'idList': '650324d427eaa6d69da3b62c',
        'key': API_KEY,
        'token': API_TOKEN
        }

    response = requests.request(
        "POST",
        url,
        params=query
        ) 

class Trello():

    # Retrieve api_key.api_secret and api_base_url from .env file
    API_KEY = dotenv_values().get('API_KEY')
    API_TOKEN = dotenv_values().get('API_TOKEN')
    API_BASE_URL = https://api.trello.com/1

    # other constants 
    LABELS_TO_CHECK = ['GTM', 'GA4', 'PREZ', 'SUPPORT', 'LOOKER STUDIO', 'PRESTA', 'INTERNE', 'PDM', 'PRIVACY','DEVIS','META','MEDIAGENIUS','R&D','GADS','TIKTOK']
    IDS_TO_CHECK = ['64fad23e39bba595108b4116','625fd31f68b0f364de2796b7','64fb35ac0cf8e80acd39291f']
    TAG_MAPPING = {
            '64fad2cfc35b447f879e00ad': 'BACKLOG',
            '64fad2cfb7e4d6bda221529b': 'TO DO',
            '64fad2cfd2da8c92cbd88e54': 'WIP',
            '64fad316fab90f193c99ec3e': 'STAND BY',
            '64faf062715bbc35238317b5': 'FOLLOW UP',
            '650324d427eaa6d69da3b62c': 'ARCHIVE 2023',
            '64fad30a467a1515aaa4d19e': 'DONE',
            '6500521cddb16e0312704306': 'TEMPLATE'
        }
    
    ID_MAPPING = {
          '64fad23e39bba595108b4116': 'VT',
          '625fd31f68b0f364de2796b7': 'JF',
          '64fb35ac0cf8e80acd39291f': 'OB'
        }

    def __init__(self, board_id):
        self.board_id = board_id
        self.session = self.create_session()
        self.raw_df = self._raw_df_cards()
        self.cards = self._cards_df()

    # Create a session with your API key and token when we instanciate the class
    def create_session(self):
        session = requests.Session()
        session.params = {'key': self.API_KEY,
                          'token': self.API_TOKEN
                          }
        return session
    
    # Get all the cards from the board_id, no refurbishments
    def _raw_df_cards(self):
        url = f'{self.API_BASE_URL}/boards/{self.board_id}/cards'
        response = self.session.get(url)
        if response.status_code == 200:
            data = response.json()
            raw_df = pd.json_normalize(data).set_index('id')

        return raw_df


    # Create a specficic dataframe for labels value -> labels column is a list of dict -> we want it flat, with column name equals to label_name
    def _labels_df(self):
        data = self.raw_df.reset_index('id')
        labels_df = pd.json_normalize([dict(data) for index, data in data.explode('labels').iterrows()])[['id','labels.name']]
        labels_df['value'] = 1
        df = labels_df.pivot(index = 'id', columns='labels.name', values = 'value')[self.LABELS_TO_CHECK]
        
        return df

    # Create a dataframe with all description information
    def _card_description_df(self):
        
        description_elements = self.raw_df['desc'].str.split('\n\n', n=6, expand=True)
        description_elements.columns = ['client','priority','estimated_spent_time', 'final_time_spent', 'proposal_price', 'sale_price','rest']
        #Remove prefixes from columns
        description_elements['client'] = [element.split(':')[-1].strip() for element in description_elements['client']]
        description_elements['priority'] = [element.split(':')[-1].strip() for element in description_elements['priority']]
        description_elements['estimated_spent_time'] = [float(element.split(':')[-1].strip().replace(',',".").replace('j','')) for element in description_elements['estimated_spent_time']]
        description_elements['final_time_spent'] = [float(element.split(':')[-1].strip().replace(',',".").replace('j','')) if element.split(':')[-1].strip().replace(',',".") != '' else np.NaN for element in description_elements['final_time_spent']]
        description_elements['proposal_price'] = [float(element.split(':')[-1].strip().replace(',',"."))  if element.split(':')[-1].strip().replace(',',".") != '' else np.NaN for element in description_elements['proposal_price']]
        description_elements['sale_price'] = [float(element.split(':')[-1].strip().replace(',',"."))  if element.split(':')[-1].strip().replace(',',".") != '' else np.NaN for element in description_elements['sale_price']]

        description_df = description_elements.drop(columns='rest')

        return description_df

    def _is_card_invoiced(self, price):
        try:
            price_float = float(price)
            return 1 if price_float > 0 else 0
        except (ValueError, TypeError):
            return 0  # Handle non-numeric or empty values

    def _compute_ratio(self, dividend, divisor):
        try :
            value = np.round(np.divide(dividend, divisor) * 100, 2)
            return value
        except : 
            value = 0
            return value

    def _cards_df(self) -> pd.DataFrame:
        base_keys = ['name', 'due', 'start', 'labels', 'idMembers', 'idList',  'badges.checkItemsChecked', 'badges.checkItems', 'desc']
        final_columns = ['card_name', 'due_date', 'start_date','card_labels','id_members', 'id_list', 
           'items_completed', 'items_amount', 'GTM', 'GA4', 'PREZ', 'SUPPORT', 'LOOKER STUDIO', 'PRESTA', 
           'INTERNE', 'PDM', 'PRIVACY',
           'DEVIS','META','MEDIAGENIUS','R&D','GADS','TIKTOK', 'client','priority',
           'estimated_spent_time', 'final_time_spent','proposal_price', 'sale_price', 
           'ticket_duration', 'card_invoiced','card_completion_rate']
        
        # We will use 3 df : base_df, labels_df, description_df
        base_df = self.raw_df[base_keys]
        labels_df = self._labels_df()
        description_df = self._card_description_df()
        
        # Join to get in one dataframe all the information we need
        df = pd.merge(left = pd.merge(left=base_df, right=labels_df, on ='id'), right = description_df, on ='id')
        
        # Modification/Creation of columns 
        
        datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        df['due'],  df['start']  = pd.to_datetime(df['due'], format=datetime_format), pd.to_datetime(df['start'], format=datetime_format)
        
        # Calculate the time difference between 'Due Date' and 'Start Date' in days
        df['ticket_duration'] = (df['due'] - df['start']).dt.days

        # boolean 
        df['card_invoiced'] = df['sale_price'].apply(self._is_card_invoiced)

        # card completion rate column
        df['card_completion_rate'] = df.apply(lambda row: self._compute_ratio(row['badges.checkItemsChecked'], row['badges.checkItems']), axis =1)

        # Update the 'id_lists' column based on the dictionary mapping
        df['idList'] = df['idList'].replace(self.TAG_MAPPING)

        # Upadate the labels columns
        df['labels'] = df['labels'].apply(lambda labels: [labels['name'] for labels in labels])

        new_list = []
        for element in df['idMembers'] :
            pre_list = []
            for id in element:
                pre_list.append(self.ID_MAPPING.get(id))
            new_list.append(pre_list)
        df['idMembers'] = new_list

        # delete useless columns
        df.drop(columns=['desc'], inplace=True)
        
        df.columns = final_columns
        df.rename_axis(index={'id':'card_id'}, inplace=True)
        
        return df
