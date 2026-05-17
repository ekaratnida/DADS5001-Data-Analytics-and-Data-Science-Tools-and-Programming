from openai import OpenAI
import streamlit as st

st.title("Chat with AI.")

@st.cache_resource
def init_connection():
    api = st.secrets["openrouter"]["api"]
    return OpenAI(base_url="https://openrouter.ai/api/v1",api_key=api,)

client = init_connection()

p = st.text_input("Your prompt here","")

if st.button("Press here"):
    completion = client.chat.completions.create(
        #model="liquid/lfm-2.5-1.2b-instruct:free",
        model="openrouter/owl-alpha",
        messages=[
            {
                "role": "user",
                "content": p
            }
        ]
    )

    st.write(completion.choices[0].message.content)