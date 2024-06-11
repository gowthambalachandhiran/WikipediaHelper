# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:31:17 2024

@author: gowtham.balachan
"""

import streamlit as st
from WikipediaHelper import WikipediaHelper
from ChatGPTClient import ChatGPTClient

class StreamlitApp:
    def __init__(self):
        self.wikipedia_helper = WikipediaHelper(
            user_agent='MyWikipediaAssistant/1.0 (https://example.com/contact; myemail@example.com)'
        )
        self.api_key = ""
        self.heading = ""
        self.question = ""
        self.persona = "assistant"
        self.previous_heading = ""
        self.chat_history = []

    def run(self):
        
        st.markdown(
            """
            <h3>Wikipedia Assistant using ChatGPT</h3>
            <p>The application can be considered as a search engine for Wikipedia articles. This is going to come with a cost. You need to supply your OpenAI secret access key; we don't store them, so go ahead. You can put the Wikipedia article name as a topic and any question you would want answers for. Finally, you can select Bot Persona if you want the response in a certain way.</p>
            """, 
            unsafe_allow_html=True
        )
        
        # Sidebar inputs
        with st.sidebar:
            self.api_key = st.text_input("Enter your OpenAI API key:", type="password")
            self.heading = st.text_input("Enter the Wikipedia heading:")
            self.question = st.text_area("Enter your question:")
            self.persona = st.selectbox("Persona", ["assistant", "teacher", "a mean person", "alien"])

        if st.button("Get Answer"):
            if self.heading != self.previous_heading:
                self.chat_history = []
                self.previous_heading = self.heading
            self.handle_get_answer()

        if self.chat_history:
            st.write("### ChatGPT Response")
            for entry in self.chat_history:
                st.write(entry)

    def handle_get_answer(self):
        if not self.api_key:
            st.error("Please enter your OpenAI API key.")
        elif not self.heading:
            st.error("Please enter a Wikipedia heading.")
        else:
            wiki_content = self.wikipedia_helper.fetch_content(self.heading)
            if wiki_content:
                truncated_content = ' '.join(wiki_content.split()[:100])
                st.write("### Wikipedia Content")
                st.write(truncated_content + "...")

                if self.question:
                    chatgpt_client = ChatGPTClient(self.api_key)
                    system_message = f"You are a helpful {self.persona}."
                    chatgpt_response = chatgpt_client.get_response(truncated_content, self.question, system_message)
                    self.chat_history.append(chatgpt_response)
                else:
                    st.write("Please enter a question to get a response from ChatGPT.")
            else:
                st.write("The specified Wikipedia heading does not exist or is a disambiguation page. Please try another one.")
