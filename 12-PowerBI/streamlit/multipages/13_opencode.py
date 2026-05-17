import streamlit as st
import pandas as pd
import requests
import io
from PIL import Image

# Update this URL to match your OpenCode API server endpoint
#OPENCODE_API_URL = "https://opencode.ai/zen/v1/chat/completions"
OPENCODE_API_URL = "http://localhost:11434/api/chat"

st.set_page_config(
    page_title="OpenCode AI Dashboard",
    page_icon="🤖",
    layout="wide",
)

# Sidebar configuration for API and Model details
st.sidebar.title("⚙️ OpenCode Engine Settings")
api_url = st.sidebar.text_input("OpenCode Endpoint", value=OPENCODE_API_URL)
api_key = st.sidebar.text_input("API Key / Bearer Token", value="opencode", type="password")

selected_model = st.sidebar.selectbox(
    "Choose Agent Model", 
    ["minimax-m2.5-free", "gemini-3-flash-preview", "gemma4"]
)

# Helper function to send requests to the OpenCode API
def call_opencode_api(prompt, system_instruction="", image_b64=None):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Constructing standard OpenAI/OpenCode compatible payload
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
        
    if image_b64:
        # Handling Vision API Structure
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]
        })
    else:
        messages.append({"role": "user", "content": prompt})

    payload = {
        "model": selected_model,
        "messages": messages,
        "temperature": 0.1
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection failed: {str(e)}"

# Helper function to convert PIL Image to Base64 for the API
def encode_image_to_b64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    import base64
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Main app 
st.title("🤖 OpenCode Multi-Modal AI Workspace")
st.caption("Leveraging the OpenCode agent framework for text, vision, and tabular data operations.")

# Create the Tab Layout
tab1, tab2, tab3 = st.tabs(["📝 Text Summary", "🖼️ Image Captioning", "📊 Dataframe Analysis"])

with tab1:
    st.header("Document & Text Summarizer")
    st.write("Paste long text, articles, or logs to get structured summaries.")
    
    #idea
    summary_type = st.radio(
        "Summary Style", 
        ["Bullet Points (TL;DR)", "Executive Abstract", "Action Items Outline"], 
        horizontal=True
    )
    
    text_input = st.text_area("Paste your text here:", height=300, placeholder="Type or paste context here...")
    
    if st.button("Generate Summary", type="primary"):

        if text_input.strip() == "":
            st.warning("Please insert some text first!")
            #st.toast("Please insert some text first!")
        else:
            with st.spinner("OpenCode is reading and drafting summary..."):
                sys_prompt = f"You are a helpful assistant. Provide a highly accurate summary formatted as {summary_type}."
                prompt = f"Please summarize the following text:\n\n{text_input}"
                
                result = call_opencode_api(prompt, system_instruction=sys_prompt)
                st.subheader("Summary Result")
                st.markdown(result)

with tab2:

    #pip install -q -U google-genai
    st.header("Image Captioning & Scene Description")
    st.write("Upload an image for visual intelligence parsing.")
    
    uploaded_image = st.file_uploader("Upload an image (JPG/PNG)", type=["png", "jpg", "jpeg"])
    vision_prompt = st.text_input(
        "Vision Instructions", 
        value="Provide a detailed caption describing this image, noting structural layout and key text elements if visible."
    )
    
    if uploaded_image is not None:

        image = Image.open(uploaded_image)
        # Resize image for optimal token handling if it's too massive
        image.thumbnail((512, 512))
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(image, caption="Uploaded View", use_column_width=True)
            
        with col2:
            if st.button("Analyze Image", type="primary"):
                with st.spinner("Processing image pixels via OpenCode Vision..."):

                    from google import genai
                    from google.genai import types

                    client = genai.Client(api_key=api_key)

                    response = client.models.generate_content(
                        model=selected_model,
                        contents=[
                        types.Part.from_bytes(
                            data=encode_image_to_b64(image),
                            mime_type='image/jpeg',
                        ),
                        'Caption this image.'
                        ]
                    )

                    st.write(response.text)
                    
                    '''
                    b64_str = encode_image_to_b64(image)
                    result = call_opencode_api(vision_prompt, image_b64=b64_str)
                    st.subheader("Analysis")
                    st.write(result)
                    '''
with tab3:

    st.header("Intelligent Dataframe Auditor")
    st.write("Upload a dataset (.csv) to generate semantic audits and analytics insights.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.subheader("Dataset Preview")
        st.dataframe(df.head(5))
        
        buffer = io.StringIO()
        st.subheader("Buffer")
        st.write(buffer)

        df.info(buf=buffer)
        df_info_str = buffer.getvalue()

        st.subheader("DF info")
        st.write(df_info_str)
        df_describe = df.describe().to_string()

        st.subheader("DF describe")
        st.write(df_describe)
        
        st.subheader("Ask Dataframe a Question")
        user_query = st.text_input(
            "What would you like OpenCode to extract or analyze from this data?",
            value="Give me the distribution of this data."
        )
        
        if st.button("Execute Data Analysis", type="primary"):
            with st.spinner("Aggregating schema details and generating insight matrix..."):
                
                # We feed the model the metadata (shapes, stats, preview) instead of raw massive CSV strings
                compiled_prompt = f"""
                You are a Data Science Expert Agent. Analyze this dataset structure.
                
                ### DATASET SHAPE & METADATA:
                {df_info_str}
                
                ### STATISTICAL SUMMARY:
                {df_describe}
                
                ### SAMPLE DATA SNIPPET (First 5 Rows):
                {df.head(5).to_string()}
                
                ### USER ANALYSIS REQUEST:
                {user_query}
                """
                st.title("Compiled prompt")
                st.write(compiled_prompt)
                
                result = call_opencode_api(compiled_prompt, system_instruction="You are an expert pandas and data analyst system.")
                st.subheader("AI Analytics Report")
                st.markdown(result)