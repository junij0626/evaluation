import streamlit as st

# Function to handle file upload and simulate processing
def upload_files(question_paper, answer_key):
    if question_paper and answer_key:
        # Simulate file processing logic here
        return True, "Files uploaded successfully!"
    else:
        return False, "Please upload both files."

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
            a.download-report {
                display: inline-block;
                margin-top: 15px;
                background-color: #28a745;
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 16px;
            }
            a.download-report:hover {
                background-color: #218838;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page container
    with st.container():
        st.markdown("<div class='container'><h2>Staff Dashboard</h2></div>", unsafe_allow_html=True)

        # File upload form
        with st.form("file_upload_form", clear_on_submit=True):
            question_paper = st.file_uploader("Upload Question Paper:", type=["pdf", "doc", "docx"])
            answer_key = st.file_uploader("Upload Answer Key:", type=["pdf", "doc", "docx"])
            submit = st.form_submit_button("Upload")

            # Handle file upload
            if submit:
                success, message = upload_files(question_paper, answer_key)
                if success:
                    st.markdown(f"<div class='success'>{message}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='error'>{message}</div>", unsafe_allow_html=True)

        # Download Marks Report button
        report_url = "path_to_marks_report.pdf"  # Replace with the actual URL/path to your report
        st.markdown(
            f"<a href='{report_url}' class='download-report' target='_blank'>Download Marks Report</a>",
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
