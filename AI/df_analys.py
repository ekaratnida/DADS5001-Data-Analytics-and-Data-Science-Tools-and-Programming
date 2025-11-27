import streamlit as st
import pandas as pd
import io
from google import genai

def convert_bytes_to_dataframe(byte_data, encoding='utf-8', **kwargs):
    try:
        string_data = byte_data.decode(encoding)
        data_io = io.StringIO(string_data)
        df = pd.read_csv(data_io, **kwargs)
        return df
    except UnicodeDecodeError as e:
            print(f"Decoding error: {e}")
            return None
    except pd.errors.EmptyDataError:
        print("Empty data error: The byte data is empty.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
#df analysis
uploaded_file = st.file_uploader("Choose a file.")
bytes_data: bytes = None
#st.write(st.session_state.model)
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    df = convert_bytes_to_dataframe(bytes_data, delimiter=',')
    st.write(df)
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Tell me about this data {df}")                          
    st.write(response.text)