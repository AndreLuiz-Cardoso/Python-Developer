from Subtitler import subtitler
import streamlit as st

##subtitle = subtitler("ja comecou a jornada full stack.mp4")

def my_app():
    st.header("Box Subtitler", divider=True)
    st.markdown("#### Generate subtitles for any video or audio automatically")

    context = st.text_input("Give some context about what the video or audio is about to make subtitles easier")
    file = st.file_uploader("Select the video (.mp4) or audio (.mp3) to subtitle", type=["mp4", "mp3"])
    if file:
        subtitle = subtitler(file, context)
        st.write(f"File {file.name} successfully subtitled")
        st.write(subtitle)


if __name__ == "__main__":
    my_app()