import streamlit as st
import wikipedia
import openai

# Set the user agent for wikipedia
wikipedia.set_user_agent('MyWikipediaAssistant/1.0 (https://example.com/contact; myemail@example.com)')

# Function to fetch Wikipedia content
def fetch_wikipedia_content(heading):
    try:
        return wikipedia.page(heading).content
    except wikipedia.exceptions.PageError:
        return None
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation page, options: {e.options}"

# Function to get response from ChatGPT
def get_chatgpt_response(api_key, wiki_content, question):
    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{wiki_content}\n\nQuestion: {question}"}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Streamlit app
st.title("Wikipedia Assistant using ChatGPT")

# Input fields
api_key = st.text_input("Enter your OpenAI API key:", type="password")
heading = st.text_input("Enter the Wikipedia heading:")
question = st.text_area("Enter your question:")

if st.button("Get Answer"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not heading:
        st.error("Please enter a Wikipedia heading.")
    else:
        wiki_content = fetch_wikipedia_content(heading)
        if wiki_content:
            st.write("### Wikipedia Content")
            #st.write(wiki_content)

            if question:
                chatgpt_response = get_chatgpt_response(api_key, wiki_content, question)
                st.write("### ChatGPT Response")
                st.write(chatgpt_response)
            else:
                st.write("Please enter a question to get a response from ChatGPT.")
        else:
            st.write("The specified Wikipedia heading does not exist or is a disambiguation page. Please try another one.")
