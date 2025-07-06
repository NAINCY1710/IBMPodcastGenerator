import streamlit as st
import re
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods

# Process Generated Text
def process(text):
    text = re.sub(r'\[.*?\]', '', text)
    # remove "speaker:" any where in text and not only at start
    text = re.sub(r'\bSpeaker\b:', '', text, flags=re.IGNORECASE)
    lines = text.splitlines()
    processed = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r'^\[.*\]$', stripped):
            continue
        if re.match(r'^\*.*:\*$', stripped):
            continue
        if re.match(r'^[A-Za-z ]+:$', stripped):
            continue
        if re.match(r'^\d+\.', stripped):
            continue
        processed.append(line)
    return "\n".join(processed)

def generate_script(topic):
    try:
        # Configure Credentials
        credentials = {
            "url": "https://us-south.ml.cloud.ibm.com",
            "apikey": st.secrets["api_keys"]["WATSONX_API_KEY"]
        }        
        project_id = st.secrets["api_keys"]["IBM_PROJECT_ID"]
        
        # Set Generation Parameters
        gen_params = {
            GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
            GenParams.MAX_NEW_TOKENS: 300,
            GenParams.TEMPERATURE: 0.7
        }
        
        # Initialize Model
        model = ModelInference(
            model_id="ibm/granite-3-3-8b-instruct",
            params=gen_params,
            credentials=credentials,
            project_id=project_id
        )

        # Validate Topic
        topic = topic.strip()
        if not topic:
            st.warning("⚠️ Please enter a topic.")
            raise ValueError("Error: Topic cannot be empty.")
    
        # Create Prompt
        prompt = (
            f"Write a small simple podcast script on the topic '{topic}' in single speaker format. "
            "Begin with an engaging introduction. "
            "Continue with one or two points about the topic in a single short paragraph. "
            "Finish with a brief, warm conclusion that wraps up the episode naturally. "
            "Do NOT include any headings, labels, or numbered lists—just write as one smooth, natural conversation."
        )

        # Generate Podcast Script
        response = model.generate_text(prompt=prompt)
        return process(response)

    # Handle Errors
    except KeyError as e:
        st.error(f"❌ Missing IBM Credentials. {e}")
        return "Error: Missing IBM credentials"
    except Exception as e:
        error_msg = str(e)
        if "400" in error_msg:
            st.error("❌ Authentication Failed. Check your API Key and Region.")
        elif "401" in error_msg:
            st.error("❌ Unauthorized. Your API Key may be Expired or Invalid.")
        elif "403" in error_msg:
            st.error("❌ Forbidden. Check IAM Permissions for Watson Machine Learning.")
        elif "404" in error_msg:
            st.error("❌ Not Found. The Requested Resource could not be Found.")
        elif "500" in error_msg:
            st.error("❌ Internal Server Error. Please Try Again Later.")
        else:
            st.error(f"❌ Generation Error: {error_msg}")
        return f"Error: {error_msg}"