# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:30:11 2024

@author: gowtham.balachan
"""
import openai

class ChatGPTClient:
    def __init__(self, api_key):
        openai.api_key = api_key

    def get_response(self, wiki_content, question, system_message):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"{wiki_content}\n\nQuestion: {question}"}
                ],
                max_tokens=150
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"An error occurred: {e}")
            return None