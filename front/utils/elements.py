import streamlit as st


# Returns a big version of the page's header
def big_header():
    _, col2, _ = st.columns([0.3, 0.4, 0.3])
    col2.image("assets/internet.png", use_container_width=True)
    st.html('<h1 style="text-align: center"> RPSL Web (please, dont sue me) </h1>')


# Returns a small version of the page's header
def small_header():
    _, col2, _ = st.columns([0.45, 0.1, 0.45])
    col2.image("assets/internet.png", use_container_width=True)
    st.html('<h1 style="text-align: center"> RPSL Web (please, dont sue me) </h1>')


# Returns navigation controls for a dataframe
# Utilizes state keys 'skip' and 'limit' for paging
def navigation_controls(key: str = ""):
    st.markdown(
        """
        <style>
            div[data-testid="stButton"]
            {
                text-align: center;
            } 
        </style>
        """,
        unsafe_allow_html=True,
    )
    _, left, middle, right, _ = st.columns([0.3, 0.1, 0.2, 0.1, 0.3])

    with middle:
        count = st.session_state.count
        lower_bound = st.session_state[f"{key}_skip"]
        upper_bound = min(
            st.session_state[f"{key}_skip"] + st.session_state[f"{key}_limit"], count
        )
        st.markdown(
            f'<div style="text-align: center"> Showing {lower_bound}-{upper_bound} of {count}</div>',
            unsafe_allow_html=True,
        )
    with left:
        left_click = st.button("← Back", key=f"{key}_back_button")
        if (
            left_click
            and st.session_state[f"{key}_skip"] >= st.session_state[f"{key}_limit"]
        ):
            st.session_state[f"{key}_skip"] = (
                st.session_state[f"{key}_skip"] - st.session_state[f"{key}_limit"]
            )
            st.rerun()
    with right:
        right_click = st.button("Next →", key=f"{key}_next_button")
        if (
            right_click
            and st.session_state[f"{key}_skip"] + st.session_state[f"{key}_limit"]
            < count
        ):
            st.session_state[f"{key}_skip"] = (
                st.session_state[f"{key}_skip"] + st.session_state[f"{key}_limit"]
            )
            st.rerun()


# Returns the footer of the website
def footer():
    st.markdown(
        """
    <style>
    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #E6E6E6;
    color: black;
    text-align: center;
    padding-top:15px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="footer">
    <p>Developed with ❤️ by <a style='display: block; text-align: center;' href="https://github.com/bereis01" target="_blank">Bernardo Reis de Almeida</a></p>
    </div>
    """,
        unsafe_allow_html=True,
    )
