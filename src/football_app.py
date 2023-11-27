
from __future__ import annotations

import streamlit as st
import numpy as np
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
                st.subheader(st.session_state.DOWN + ' & ' + str(st.session_state.DISTANCE))
        
        self.field = FBField(hash = st.session_state.HASH, 
                             field_pos=st.session_state.FIELD_POS, 
                             distance=st.session_state.DISTANCE)
        st.pyplot(self.field.fig)

        st.write('')

        _,_,_,col1, col2,_,_,_ = st.columns(8)
        with col1:
            st.button('RUSH', on_click=self.rush_master_update)
        with col2:
            st.button('PASS', on_click=self.pass_master_update)

        df = FootballDB().get_tRush()
        filter_df = df[df[('fieldpos'==st.session_state.FIELD_POS) & ('down'==st.session_state.DOWN) & ('distance'==st.session_state.DISTANCE)]]

        st.write(filter_df)
        st.write(st.session_state.FIELD_POS)
        st.write(st.session_state.DOWN)
        st.write(st.session_state.DISTANCE)

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
    
        return
    
    def rush_master_update(self):
        '''
        Runs all functions to occur on rush button click
        '''
        self.update_game()
        return
    
    def update_position_rush(self):
        df = FootballDB().get_tRush()
        filter_df = df[df[('fieldpos'==st.session_state.FIELD_POS) and ('down'==st.session_state.DOWN) and ('distance'==st.session_state.DISTANCE)]]

        return
    
    def pass_master_update(self):
        '''
        Runs all functions to occur on pass button click
        '''
        self.update_game()
        return
    
    def update_position_pass(self):

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