import streamlit as st
import os
import tempfile
try:
    import moviepy.editor as mp
except ModuleNotFoundError:
    import subprocess
    subprocess.check_call(["pip", "install", "moviepy"])
    import moviepy.editor as mp
import whisper

def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # Load Whisper model
    result = model.transcribe(audio_path)
    return result["text"]

def main():
    st.title("AI Movie Descriptor")
    st.write("Upload a video to get an AI-generated audio description.")
    
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov", "mkv"])
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_file.read())
            video_path = temp_video.name
            
        audio_path = video_path.replace(".mp4", ".wav")
        
        st.write("Extracting audio...")
        extract_audio(video_path, audio_path)
        
        st.write("Transcribing audio...")
        description = transcribe_audio(audio_path)
        
        st.subheader("Generated Audio Description:")
        st.write(description)
        
        os.remove(video_path)
        os.remove(audio_path)

if __name__ == "__main__":
    main()