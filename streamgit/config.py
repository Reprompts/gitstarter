import os
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

def get_github_token():
    # 1) session state (entered via UI)
    token = st.session_state.get("github_token", None)
    if token:
        return token

    # 2) Streamlit secrets.toml (if exists)
    try:
        # .get won’t crash even if "github" missing
        tok = st.secrets.get("github", {}).get("token")
        if tok:
            return tok
    except StreamlitSecretNotFoundError:
        # no secrets file → skip
        pass

    # 3) ENV var fallback
    return os.getenv("GITHUB_TOKEN", None)

def set_github_token(token: str):
    """Store token in session and env for this session."""
    st.session_state.github_token = token
    os.environ["GITHUB_TOKEN"] = token
