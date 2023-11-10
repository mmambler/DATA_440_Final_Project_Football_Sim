
from __future__ import annotations

import streamlit as st
from src.football_viz import FBField
from src.football_db import FootballDB
import src.dropdown_lists as dropdown

class FBApp:

    def __init__(self):

        if 'MINUTES' not in st.session_state:
            st.session_state.MINUTES = 15
        if 'SECONDS' not in st.session_state:
            st.session_state.SECONDS = 0

        self.field = FBField()
        self.db = FootballDB()

        self.load_tables_from_db()
        self.build_page()
        self.streamlit_defaults()
        return
    
    def build_page(self):
        
        st.header("Gridiron Guru: Offensive Playcalling Simulator")

        st.write('')

        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('USER: 34')
            st.button('RESET CLOCK', on_click=self.reset_game_clock)
        with col2:
            st.subheader('Play Clock: ' + str(st.session_state.MINUTES) + ':' + f"{st.session_state.SECONDS:02}")
        with col3:
            col_1, col_2 = st.columns(2)
            with col_2:
                st.subheader('CPU: 34')

        field_slot = st.empty()

        col1, col2, col3 = st.columns(3)
        with col1:
            self.offense = st.selectbox('Offense', sorted(dropdown.nfl_teams), index=31)
            st.selectbox('Game Clock (Min.)', dropdown.clock_min)
            st.selectbox('Quarter', [1,2,3,4])
        with col2:
            self.defense = st.selectbox('Defense', sorted(dropdown.nfl_teams), index=9)
            st.selectbox('Game Clock (Sec.)', sorted(dropdown.clock_sec))
            st.selectbox('Down', [1,2,3,4])
        with col3:
            self.field_pos = st.selectbox('Field Pos.', dropdown.field_pos)
            self.hash = st.selectbox('Hash', ['Center','Left','Right'])
            self.distance = st.selectbox('Distance', dropdown.distance, index=9)
        
        self.field = FBField(hash = self.hash, field_pos=self.field_pos, distance=self.distance)
        field_slot.pyplot(self.field.fig)

        st.write('')

        _,_,_,col1, col2,_,_,_ = st.columns(8)
        with col1:
            st.button('RUSH', on_click=self.update_game_clock)
            
        with col2:
            st.button('PASS', on_click=self.update_game_clock)

        return
    
    def reset_game_clock(self):
        '''
        Resets the game clock to 15:00
        '''
        st.session_state.MINUTES = 15
        st.session_state.SECONDS = 0
    
        return
    
    def update_game_clock(self):
        '''
        Updates the game clock after play called
        '''
        runoff = -20
        temp_sec = st.session_state.SECONDS + runoff
        if temp_sec < 0:
            st.session_state.MINUTES = st.session_state.MINUTES-1
            st.session_state.SECONDS = 60 + temp_sec
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