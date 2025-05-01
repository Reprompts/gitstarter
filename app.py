import streamlit as st
from streamgit.ui import main_ui

def main():
    st.set_page_config(page_title="GitStarter", layout="wide")
    main_ui()

if __name__ == "__main__":
    main()
