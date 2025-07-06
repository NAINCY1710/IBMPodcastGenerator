import streamlit as st
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def text_to_speech(text, output_file="output.wav", voice="en-US_AllisonV3Voice"):
    try:
        # Configure Credentials
        api_key = st.secrets["api_keys"]["IBM_WATSON_TTS_API_KEY"]
        url = st.secrets["api_keys"]["IBM_WATSON_TTS_URL"]
        authenticator = IAMAuthenticator(api_key)
        tts = TextToSpeechV1(authenticator=authenticator)
        tts.set_service_url(url)

        # Check if Exceeds Character Limit
        if len(text) > 100:
            text = text[:100] + "..."

        # Synthesize Speech
        ssml = f'<speak>{text}</speak>'
        with open(output_file, "wb") as audio_file:
            response = tts.synthesize(
                ssml,
                voice=voice,
                accept="audio/wav"
            ).get_result()
            audio_file.write(response.content)
        return True

    # Handle Errors
    except Exception as e:
        st.error(f"❌ Error Generating Voice. {e}")
        return False