import streamlit as st


# Removes all keys from streamlit state
# Except those in the exceptions list
def clear_cache(exceptions=[]):
    state_keys = list(st.session_state.keys())
    keys = list(set(state_keys) - set(exceptions))
    for key in keys:
        st.session_state.pop(key)


# Used to clear the search bar after pressing enter
def submit():
    st.session_state["query"] = st.session_state.search_bar
    st.session_state.search_bar = ""
