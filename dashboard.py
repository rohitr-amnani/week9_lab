import streamlit as st
from week7.Auth import login_user, register_user, validate_username, validate_password

st.set_page_config(page_title="Login", page_icon="🔒")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]


if st.session_state.logged_in:
    st.title("Welcome!")
    st.success(f"Hello, {st.session_state.username}! You are now logged in.")

else:
    st.title("🔐 Multi-Domain Intelligence Platform")
    
    tab_login, tab_register = st.tabs(["Login", "Register"])

   
    with tab_login:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Log In", type="primary"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

  
    with tab_register:
        st.subheader("Register New Account")
        new_user = st.text_input("Choose Username", key="reg_user")
        new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")

        if st.button("Create Account"):
            valid_u, msg_u = validate_username(new_user)
            valid_p, msg_p = validate_password(new_pass)

            if not valid_u:
                st.error(msg_u)
            elif not valid_p:
                st.error(msg_p)
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            else:
                if register_user(new_user, new_pass):
                    st.success("Account created! Please log in.")
                else:
                    st.error("Username already exists.")
