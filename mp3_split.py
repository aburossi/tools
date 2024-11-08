import streamlit as st
from pydub import AudioSegment, exceptions
import math
import os
import zipfile
import io

def split_audio(file, max_size_mb=9):
    """
    Splits the audio file into chunks where each chunk is approximately less than max_size_mb.
    """
    try:
        audio = AudioSegment.from_file(file)
    except exceptions.CouldntDecodeError:
        st.error("Failed to decode the audio file. Please ensure it's a valid MP3.")
        return []
    
    max_size_bytes = max_size_mb * 1024 * 1024
    chunks = []
    start_ms = 0
    step_ms = 60000  # Start with 1 minute

    while start_ms < len(audio):
        end_ms = start_ms + step_ms
        chunk = audio[start_ms:end_ms]
        chunk_io = io.BytesIO()
        chunk.export(chunk_io, format="mp3")
        if len(chunk_io.getvalue()) > max_size_bytes:
            if step_ms <= 1000:
                st.warning("Cannot split the file into smaller chunks without reducing audio quality.")
                break
            step_ms = step_ms // 2
            continue
        chunks.append(chunk)
        start_ms += step_ms

    return chunks

def create_zip(chunks, original_filename):
    """
    Creates a zip file containing all audio chunks.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for idx, chunk in enumerate(chunks):
            chunk_filename = f"{os.path.splitext(original_filename)[0]}_part{idx+1}.mp3"
            chunk_io = io.BytesIO()
            chunk.export(chunk_io, format="mp3")
            zipf.writestr(chunk_filename, chunk_io.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

def main():
    st.title("🎵 MP3 Splitter and Zipper")
    st.write("Upload an MP3 file, and this app will split it into parts smaller than 9MB and provide a zip for download.")

    uploaded_file = st.file_uploader("📂 Choose an MP3 file", type=["mp3"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/mp3')
        original_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.write(f"**Original file size:** {original_size_mb:.2f} MB")

        if original_size_mb <= 9:
            st.info("✅ The uploaded file is already smaller than 9MB. No splitting needed.")
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.writestr(uploaded_file.name, uploaded_file.getvalue())
            zip_buffer.seek(0)
            st.download_button(
                label="📥 Download Zip",
                data=zip_buffer,
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}.zip",
                mime="application/zip"
            )
        else:
            with st.spinner('🔄 Processing...'):
                try:
                    chunks = split_audio(uploaded_file, max_size_mb=9)
                    if not chunks:
                        st.error("No chunks were created. Please try a different file.")
                        return
                    zip_buffer = create_zip(chunks, uploaded_file.name)
                    st.success('✅ Splitting and zipping completed!')

                    st.download_button(
                        label="📥 Download Zip",
                        data=zip_buffer,
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}_parts.zip",
                        mime="application/zip"
                    )
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
