import streamlit as st


# Removes all keys from streamlit state
# Except those in the exceptions list
def clear_cache(exceptions=[]):
    state_keys = list(st.session_state.keys())
    keys = list(set(state_keys) - set(exceptions))
    for key in keys:
        st.session_state.pop(key)
