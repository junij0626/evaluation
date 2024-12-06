import streamlit as st

# Simulated logic to fetch marks
def get_marks():
    # Replace with actual logic to retrieve marks
    return None

# Function to simulate answer sheet upload
def upload_answer_sheet(answer_sheet):
    if answer_sheet:
        # Simulate processing the uploaded file
        return True, "Answer sheet uploaded successfully!"
    else:
        return False, "Please upload your answer sheet."

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
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh; /* Changed from min-height to height */
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
            .success {
                color: green;
            }
            .error {
                color: red;
            }
            .marks {
                font-size: 24px;
                color: #333;
                margin-top: 20px;
                font-weight: bold;
            }
            .logout-message {
                font-size: 18px;
                color: #333;
                margin-top: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page container
    with st.container():
        st.markdown("<div class='container'><h2>Student Dashboard</h2></div>", unsafe_allow_html=True)

        # Check if marks are available
        marks = get_marks()

        if marks is not None:
            # Display marks and logout message
            st.markdown(f"<div class='marks'>Your Marks: {marks}%</div>", unsafe_allow_html=True)
            st.markdown("<div class='logout-message'>You will be logged out in 30 seconds...</div>", unsafe_allow_html=True)
        else:
            # Form to upload answer sheet
            st.write("No marks available yet. Please upload your answer sheet.")
            with st.form("upload_form", clear_on_submit=True):
                answer_sheet = st.file_uploader("Upload Answer Sheet:", type=["pdf", "doc", "docx"])
                submit = st.form_submit_button("Upload")

                if submit:
                    success, message = upload_answer_sheet(answer_sheet)
                    if success:
                        st.markdown(f"<div class='success'>{message}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='error'>{message}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
