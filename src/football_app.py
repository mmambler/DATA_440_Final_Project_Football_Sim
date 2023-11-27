
from __future__ import annotations

import streamlit as st
import numpy as np
import random
from src.football_viz import FBField
from src.football_db import FootballDB
import src.dropdown_lists as dropdown

class FBApp:

    def __init__(self):

        self.field = FBField()
        self.db = FootballDB()

        self.initialize_session_state()
        self.load_tables_from_db()
        self.build_page()
        self.streamlit_defaults()
        return
    
    def build_page(self):
        
        st.header("Gridiron Guru: Offensive Playcalling Simulator")
        _,_,col,_,_ = st.columns(5)
        with col:
            st.write('By: Mac Ambler')

        st.write('')

        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('USER: ' + str(st.session_state.USER_SCORE))
        with col2:
            st.subheader('Play Clock: ' + str(st.session_state.MINUTES) + ':' + f"{st.session_state.SECONDS:02}")
        with col3:
            col_1, col_2 = st.columns(2)
            with col_2:
                st.subheader('CPU: ' + str(st.session_state.CPU_SCORE))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.button('RESTART GAME', on_click=self.reset_game)
        with col2:
            st.subheader('Quarter: ' + str(st.session_state.QUARTER))
        with col3:
            col_1, col_2 = st.columns(2)
            with col_2:
                if st.session_state.DOWN == 1:
                    st.subheader(str(st.session_state.DOWN) + 'st & ' + str(st.session_state.DISTANCE))
                elif st.session_state.DOWN == 2:
                    st.subheader(str(st.session_state.DOWN) + 'nd & ' + str(st.session_state.DISTANCE))
                elif st.session_state.DOWN == 3:
                    st.subheader(str(st.session_state.DOWN) + 'rd & ' + str(st.session_state.DISTANCE))
                elif st.session_state.DOWN == 4:
                    st.subheader(str(st.session_state.DOWN) + 'th & ' + str(st.session_state.DISTANCE))
        
        self.field = FBField(hash = st.session_state.HASH, 
                             field_pos=st.session_state.FIELD_POS, 
                             distance=st.session_state.DISTANCE)
        st.pyplot(self.field.fig)

        st.write('')
        _,col,_ = st.columns([1.5,3,1])
        with col:
            if st.session_state.YARDS_RESULT != '':
                st.subheader(st.session_state.YARDS_RESULT)

        st.write('')

        _,_,_,col1, col2,_,_,_ = st.columns(8)
        with col1:
            st.button('RUSH', on_click=self.rush_master_update)
        with col2:
            st.button('PASS', on_click=self.pass_master_update)

        return
    
    def reset_game(self):
        '''
        Resets the game
        '''

        st.session_state.MINUTES = 15
        st.session_state.SECONDS = 0
        st.session_state.USER_SCORE = 0
        st.session_state.CPU_SCORE = 0
        st.session_state.QUARTER = 1
        st.session_state.DOWN = 1
        st.session_state.DISTANCE = 10
        st.session_state.FIELD_POS = -25
        st.session_state.YARDS_RESULT = ''
    
        return
    
    def reset_drive(self):
        '''
        Resets the drive
        '''
        st.session_state.DOWN = 1
        st.session_state.DISTANCE = 10
        st.session_state.FIELD_POS = -25
        st.session_state.YARDS_RESULT = ''
    
        return
    
    def rush_master_update(self):
        '''
        Runs all functions to occur on rush button click
        '''

        self.update_position_rush()
        self.update_game()
        return
    
    def update_position_rush(self):
        
        df = self.tRush
        filter_df = df[(df['down']==st.session_state.DOWN) & (df['distance']==st.session_state.DISTANCE)]
        yards_gained = filter_df['yards_gained'].sample().iloc[0]
        dist_temp = st.session_state.DISTANCE - yards_gained
        if dist_temp > 0:
            if st.session_state.DOWN < 4:
                st.session_state.DISTANCE = dist_temp
                st.session_state.DOWN += 1
                field_pos_temp = dropdown.field_pos_dict[st.session_state.FIELD_POS] + yards_gained
                st.session_state.FIELD_POS = dropdown.field_pos_dict_reverse[field_pos_temp]
                st.session_state.YARDS_RESULT = 'RUSHED FOR ' + str(yards_gained) + ' YARDS'
            else:
                self.reset_drive()
        else:
            st.session_state.DOWN = 1
            st.session_state.DISTANCE = 10
            field_pos_temp = dropdown.field_pos_dict[st.session_state.FIELD_POS] + yards_gained
            st.session_state.FIELD_POS = dropdown.field_pos_dict_reverse[field_pos_temp]
            st.session_state.YARDS_RESULT = 'RUSHED FOR ' + str(yards_gained) + ' YARDS'

        return
    
    def pass_master_update(self):
        '''
        Runs all functions to occur on pass button click
        '''

        self.update_position_pass()
        self.update_game()
        return
    
    def update_position_pass(self):
        rand_num = random.random()
        if rand_num <= 0.65:
            df = self.tPass
            filter_df = df[(df['down']==st.session_state.DOWN) & (df['distance']==st.session_state.DISTANCE)]
            yards_gained = filter_df['yards_gained'].sample().iloc[0]
        else:
            yards_gained = 0
        dist_temp = st.session_state.DISTANCE - yards_gained
        if dist_temp > 0:
            if st.session_state.DOWN < 4:
                st.session_state.DISTANCE = dist_temp
                st.session_state.DOWN += 1
                field_pos_temp = dropdown.field_pos_dict[st.session_state.FIELD_POS] + yards_gained
                st.session_state.FIELD_POS = dropdown.field_pos_dict_reverse[field_pos_temp]
            else:
                self.reset_drive()
        else:
            st.session_state.DOWN = 1
            st.session_state.DISTANCE = 10
            field_pos_temp = dropdown.field_pos_dict[st.session_state.FIELD_POS] + yards_gained
            st.session_state.FIELD_POS = dropdown.field_pos_dict_reverse[field_pos_temp]

        return
    
    
    def update_game(self):
        '''
        Updates the game situation after play called
        '''

        runoff = -1*int(round(np.random.normal(20,5), 0))
        temp_sec = st.session_state.SECONDS + runoff
        if (st.session_state.MINUTES > 0) and (temp_sec < 0):
            st.session_state.MINUTES = st.session_state.MINUTES-1
            st.session_state.SECONDS = 60 + temp_sec
        elif (st.session_state.MINUTES == 0) and (temp_sec < 0):
            st.session_state.MINUTES = 15
            st.session_state.SECONDS = 0
            st.session_state.QUARTER = st.session_state.QUARTER + 1
        else:
            st.session_state.SECONDS = temp_sec
        
        return
    
    def load_tables_from_db(self):
        '''
        Initialize all dataframes from database
        '''

        self.tGame = self.db.get_tGame()
        self.tPass = self.db.get_tPass()
        self.tRush = self.db.get_tRush()
        self.tRunConcept = self.db.get_tRunConcept()
        
        return
    
    def initialize_session_state(self):
        '''
        Initializes session state variables if they don't already exist
        '''

        if 'MINUTES' not in st.session_state:
            st.session_state.MINUTES = 15
        if 'SECONDS' not in st.session_state:
            st.session_state.SECONDS = 0
        if 'USER_SCORE' not in st.session_state:
            st.session_state.USER_SCORE = 0
        if 'CPU_SCORE' not in st.session_state:
            st.session_state.CPU_SCORE = 0
        if 'QUARTER' not in st.session_state:
            st.session_state.QUARTER = 1
        if 'DOWN' not in st.session_state:
            st.session_state.DOWN = 1
        if 'DISTANCE' not in st.session_state:
            st.session_state.DISTANCE = 10
        if 'FIELD_POS' not in st.session_state:
            st.session_state.FIELD_POS = -25
        if 'HASH' not in st.session_state:
            st.session_state.HASH = 'Center'
        if 'YARDS_RESULT' not in st.session_state:
            st.session_state.YARDS_RESULT = ''

        return
    
    def streamlit_defaults(self):
        '''
        Remove some auto-generated stuff by streamlit
        '''

        hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
        return
      
if __name__ == '__main__':
    FBApp()