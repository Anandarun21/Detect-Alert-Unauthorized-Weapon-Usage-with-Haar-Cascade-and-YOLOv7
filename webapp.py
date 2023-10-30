import streamlit as st
import pandas as pd
import subprocess
import os

# Define a function to register a new user
def register(username, password):
    # Load the existing user data (or create an empty dataframe if it doesn't exist)
    try:
        user_data = pd.read_csv("user_data.csv")
    except:
        user_data = pd.DataFrame(columns=["username", "password"])
    
    # Check if the username already exists
    if username in user_data["username"].values:
        st.error("Username already exists.")
    else:
        # Add the new user to the user data
        new_user = {"username": username, "password": password}
        user_data = user_data.append(new_user, ignore_index=True)
        user_data.to_csv("user_data.csv", index=False)
        st.success("Registration successful.")

# Define a function to log in an existing user
def login(username, password):
    # Load the user data
    try:
        user_data = pd.read_csv("user_data.csv")
    except:
        st.error("No users registered yet.")
        return
    # Check if the username and password match
    if (username in user_data["username"].values) & (password in user_data["password"].values):
        st.success("Login successful.")
        subprocess.run("python face_detector.py")
    else:
        st.error("Incorrect username or password.")

# Define the Streamlit app
def app():
    st.title("Login / Registration")
    
    # Create a sidebar with a menu of options
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Select an option", menu)
    
    # Show the appropriate form based on the user's menu choice
    if choice == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(username, password)
    elif choice == "Register":
        st.header("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Register"):
            if password == confirm_password:
                register(username, password)
            else:
                st.error("Passwords do not match.")
app()