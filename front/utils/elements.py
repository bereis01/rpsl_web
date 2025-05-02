import streamlit as st
from htbuilder import (
    HtmlElement,
    div,
    ul,
    li,
    br,
    hr,
    a,
    p,
    img,
    styles,
    classes,
    fonts,
)
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def big_header():
    _, col2, _ = st.columns([0.3, 0.4, 0.3])
    col2.image("assets/internet.png", use_container_width=True)
    st.html('<h1 style="text-align: center"> RPSL Explorer (please, dont sue me) </h1>')


def small_header():
    _, col2, _ = st.columns([0.45, 0.1, 0.45])
    col2.image("assets/internet.png", use_container_width=True)
    st.html('<h1 style="text-align: center"> RPSL Explorer (please, dont sue me) </h1>')


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


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1,
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2),
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made in [Streamlit]",
        " with ❤️ by ",
        link("https://github.com/bereis01", "@bereis01"),
        br(),
    ]
    layout(*myargs)
