import streamlit as st

# Function to simulate authentication logic
def authenticate(register_number, password):
    # Replace with actual authentication logic (e.g., check from a database)
    if register_number == "12345" and password == "password":
        return True, "Login successful!"
    else:
        return False, "Invalid register number or password."

# Streamlit app
def main():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #7DF9FF;
                margin: 0;
                padding: 0;
            }
            .container {
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
                width: 350px;
                text-align: center;
                margin: auto;
            }
            h2 {
                color: #333;
                margin-bottom: 20px;
            }
            .stApp {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .error {
                color: red;
                font-weight: bold;
            }
            .success {
                color: green;
                font-weight: bold;
            }
            input[type="text"], input[type="password"] {
                width: 100%;
                padding: 8px;
                margin: 8px 0;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            input[type="submit"] {
                background-color: #5c67f2;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            input[type="submit"]:hover {
                background-color: #4b55c8;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create login form inside a container
    with st.container():
        st.markdown("<div class='container'><h2>Login</h2></div>", unsafe_allow_html=True)
        
        # Form for login
        with st.form("login_form", clear_on_submit=True):
            register_number = st.text_input("Register Number", placeholder="Enter your register number")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login")

            # Handle form submission
            if submit:
                if register_number and password:
                    success, message = authenticate(register_number, password)
                    if success:
                        st.markdown(f"<div class='success'>{message}</div>", unsafe_allow_html=True)
                        st.success("You are now logged in!")
                        # Redirect or take additional actions after successful login
                    else:
                        st.markdown(f"<div class='error'>{message}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='error'>Please fill in all fields.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
