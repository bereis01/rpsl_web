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
        left_click = st.button("←", key=f"{key}_back_button")
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
        right_click = st.button("→", key=f"{key}_next_button")
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


@st.fragment
def lazy_expander(
    title: str,
    key: str,
    on_expand,
    expanded: bool = False,
    callback_kwargs: dict = None,
):
    """
    A 'lazy' expander that only loads/renders content on expand.

    Args:
        title (str): Title to show beside the arrow.
        key (str): Unique key for storing expanded state in st.session_state.
        on_expand (callable): A function that takes a container (and optional kwargs)
                              to fill with content *only* after expanding.
        expanded (bool): Initial state (collapsed=False by default).
        callback_kwargs (dict): Extra kwargs for on_expand() if needed.
    """
    if callback_kwargs is None:
        callback_kwargs = {}

    # Initialize session state in the first run
    if key not in st.session_state:
        st.session_state[key] = expanded

    outer_container = st.container(border=True)

    with outer_container:
        if st.button(label=(f"{title}")):
            # If currently collapsed -> expand and call on_expand
            if not st.session_state[key]:
                st.session_state[key] = True
                on_expand(outer_container, **callback_kwargs)

            # If currently expanded -> collapse (force a rerun)
            else:
                st.session_state[key] = False
                st.rerun()
