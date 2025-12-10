import streamlit as st


# Returns navigation controls for a dataframe
# Utilizes state keys '{key}_skip' and '{key}_limit' for paging
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
    _, left, middle, right, _ = st.columns(
        [0.2, 0.1, 0.4, 0.1, 0.2], vertical_alignment="center"
    )

    with middle:
        count = st.session_state[f"{key}_count"]
        lower_bound = st.session_state[f"{key}_skip"]
        upper_bound = min(
            st.session_state[f"{key}_skip"] + st.session_state[f"{key}_limit"], count
        )
        st.markdown(
            f'<div style="text-align: center"> Showing {lower_bound}-{upper_bound} of {count}</div>',
            unsafe_allow_html=True,
        )
    with left:
        left_click = st.button(
            "", key=f"{key}_back_button", icon=":material/arrow_back:", width="stretch"
        )
        if (
            left_click
            and st.session_state[f"{key}_skip"] >= st.session_state[f"{key}_limit"]
        ):
            st.session_state[f"{key}_skip"] = (
                st.session_state[f"{key}_skip"] - st.session_state[f"{key}_limit"]
            )
            st.session_state[f"{key}_changed"] = True
            st.rerun()
    with right:
        right_click = st.button(
            "",
            key=f"{key}_next_button",
            icon=":material/arrow_forward:",
            width="stretch",
        )
        if (
            right_click
            and st.session_state[f"{key}_skip"] + st.session_state[f"{key}_limit"]
            < count
        ):
            st.session_state[f"{key}_skip"] = (
                st.session_state[f"{key}_skip"] + st.session_state[f"{key}_limit"]
            )
            st.session_state[f"{key}_changed"] = True
            st.rerun()
