import streamlit as st
from script import generate_script
from voice import text_to_speech
import os

# Page Configuration
st.set_page_config(
    page_title="IBM Podcast Generator", 
    layout="wide",
    page_icon="🎙️",
    initial_sidebar_state="collapsed"
)

# Load CSS Styling
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page Title and Description
st.title("🎙️ IBM Podcast Generator")
st.write("Create engaging podcast scripts and voiceovers with IBM Watson AI & TTS")

# English Voice Options
voice_options = {
    "Allison (US English, expressive)": "en-US_AllisonV3Voice",
    "Michael (US English, expressive)": "en-US_MichaelV3Voice", 
    "Olivia (US English, expressive)": "en-US_OliviaV3Voice",
    "Lisa (US English)": "en-US_LisaV3Voice",
    "Heidi (Australian English)": "en-AU_HeidiExpressive",
    "Kate (British English)": "en-GB_KateV3Voice"
}

# Topic Form
with st.form("podcast_form"):

    # Topic Input
    topic = st.text_input(
        "Podcast Topic",
        placeholder="e.g., The Fascinating World of Artificial Intelligence",
        help="Enter the main topic for your podcast episode"
    )

    # Submit Button
    if st.form_submit_button("Generate Podcast Script"):
        if not topic.strip():
            st.warning("⚠️ Please enter a topic to generate your podcast script.")
        else:
            with st.spinner("Generating your podcast script..."):
                try:
                    st.session_state.generated_script = generate_script(topic)
                    st.session_state.script_generated = True
                except Exception as e:
                    st.error(f"❌ Error generating script: {e}")
                    st.session_state.generated_script = None
                    st.session_state.script_generated = False

# Display Generated Script
script_text = st.session_state.get("generated_script")
if script_text:
    if st.session_state.get("script_generated", False):
        st.markdown('<div class="success-message">✅ Script generated successfully!</div>', unsafe_allow_html=True)
        st.session_state.script_generated = False
    st.markdown(f'<div class="script-container">{script_text}</div>', unsafe_allow_html=True)

    # Voice Selection
    selected_voice = st.selectbox(
        "Select Voice for Voiceover",
        list(voice_options.keys()),
        key="voice",
        help="Choose the voice that will narrate your podcast"
    )

    # Generate Voice Button
    if st.button("Generate Voiceover", type="secondary"):

        # Remove Existing Voice
        if os.path.exists("output.wav"):
            os.remove("output.wav")
        with st.spinner("Generating voiceover... This may take a moment."):
            success = text_to_speech(script_text, voice=voice_options[selected_voice])
            
        if success and os.path.exists("output.wav"):
            # Voice Control
            st.markdown('<div class="success-message">✅ Voiceover generated successfully!</div>', unsafe_allow_html=True)
            st.audio("output.wav", format="audio/wav")

            # Download Voice Button
            with open("output.wav", "rb") as audio_file:
                st.download_button(
                    "Download Voiceover",
                    audio_file,
                    "podcast_voiceover.wav",
                    "audio/wav",
                    use_container_width=True
                )
        else:
            st.error("❌ Failed to generate voiceover. Please check your TTS credentials and try again.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    Made with &hearts; by Naincy and Aarjav Jain
</div>
""", unsafe_allow_html=True)