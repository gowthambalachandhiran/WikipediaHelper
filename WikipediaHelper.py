# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:29:41 2024

@author: gowtham.balachan
"""

import wikipedia

class WikipediaHelper:
    def __init__(self, user_agent):
        wikipedia.set_user_agent(user_agent)

    def fetch_content(self, heading):
        try:
            return wikipedia.page(heading).content
        except wikipedia.exceptions.PageError:
            return None
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Disambiguation page, options: {e.options}"
