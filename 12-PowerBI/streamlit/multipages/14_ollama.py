from ollama import chat
import streamlit as st
import io
from PIL import Image
   

tab1, tab2, tab3 = st.tabs(["Local","Cloud text", "Cloud image"])

with tab1:
    st.header("Document & Text Summarizer")
    st.write("Paste long text, articles, or logs to get structured summaries.")
        
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
                
                #prompt = f"Please summarize the following text:\n\n{text_input}"
                prompt = f"{text_input}"
                
                response = chat(
                    model='gemma4',
                    #messages=[{"role": "system", "content": sys_prompt}, {'role': 'user', 'content': prompt}],
                    messages=[{'role':'user','content':prompt}]
                )

                st.subheader("Summary Result")
                st.markdown(response.message.content)

with tab2:

    from ollama import Client
    
    client = Client(
        host="https://ollama.com",
        headers={'Authorization': 'Bearer ' + "4d5a66d85fd343f483d3af9a469bf087.pUMYCqnLOlXmd9K3v2oGL2RT"}
    )
   
    st.header("Document & Text Summarizer")
    st.write("Paste long text, articles, or logs to get structured summaries.")
        
    summary_type = st.radio(
        "Summary Style2", 
        ["Bullet Points (TL;DR)", "Executive Abstract", "Action Items Outline"], 
        horizontal=True
    )

    
    text_input2 = st.text_area("Paste your text here_:", height=300, placeholder="Type or paste context here...")

    if st.button("Generate Summary2", type="primary"):

        if text_input2.strip() == "":
            st.warning("Please insert some text first!")
            #st.toast("Please insert some text first!")

        else:
            with st.spinner("OpenCode is reading and drafting summary..."):
                sys_prompt = f"You are a helpful assistant. Provide a highly accurate summary formatted as {summary_type}."
                prompt = f"Please summarize the following text:\n\n{text_input2}"
                response = client.chat(
                    #model='gpt-oss:120b',
                    model='gemma4:31b-cloud',
                    #model='deepseek-v4-flash:cloud',
                    messages=[{"role": "system", "content": sys_prompt}, {'role': 'user', 'content': prompt}],
                )

                st.subheader("Summary Result")
                st.markdown(response.message.content)

def encode_image_to_b64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    import base64
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

with tab3:
    
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
            st.image(image, caption="Uploaded View")
            
        with col2:
            if st.button("Analyze Image", type="primary"):
                with st.spinner("Processing image pixels via OpenCode Vision..."):
            
                    from ollama import chat
                    b64_str = encode_image_to_b64(image)
                    response = chat(
                        model='gemma4:31b-cloud',
                        messages=[
                            {
                                'role': 'user',
                                'content': vision_prompt,
                                'images': [b64_str]
                            }
                        ],
                    )

                    st.write(response.message.content)
