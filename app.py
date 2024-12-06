from flask import Flask, request, render_template, redirect, url_for, session, flash, send_file
import mysql.connector
from werkzeug.utils import secure_filename
import os
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from fpdf import FPDF

# Flask app setup
app = Flask(__name__)
app.secret_key = '9f9cb796f13819cde79058cf72f6270b'

# Database connection setup
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Admin@26",
    database="ExamSystem"
)
cursor = db.cursor()

# File upload settings
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 MB

# Check if the uploads directory exists, create if not
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        register_number = request.form['register_number']
        password = request.form['password']
        cursor.execute("SELECT * FROM Users WHERE register_number=%s AND password=%s", (register_number, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]  # Assuming 'id' is at index 0
            session['user_type'] = user[3]  # 'user_type' column is at index 3
            if session['user_type'] == 'staff':
                return redirect(url_for('staff_dashboard'))
            elif session['user_type'] == 'student':
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid login credentials')
    return render_template('login.py')

# Staff dashboard
@app.route('/staff', methods=['GET', 'POST'])
def staff_dashboard():
    if 'user_type' not in session or session['user_type'] != 'staff':
        flash('Access denied. Staff only.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'question_paper' in request.files and 'answer_key' in request.files:
            question_paper = request.files['question_paper']
            answer_key = request.files['answer_key']
            if allowed_file(question_paper.filename) and allowed_file(answer_key.filename):
                question_paper_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(question_paper.filename))
                answer_key_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(answer_key.filename))
                question_paper.save(question_paper_path)
                answer_key.save(answer_key_path)

                # Insert uploaded document details into UploadedDocuments table
                cursor.execute(
                    "INSERT INTO UploadedDocuments (user_id, document_type, file_path) VALUES (%s, %s, %s)",
                    (session['user_id'], 'question_paper', question_paper_path)
                )
                cursor.execute(
                    "INSERT INTO UploadedDocuments (user_id, document_type, file_path) VALUES (%s, %s, %s)",
                    (session['user_id'], 'answer_key', answer_key_path)
                )
                db.commit()

                flash('Files uploaded successfully')
            else:
                flash('Invalid file type')
    return render_template('staff_dashboard.py')

# Student dashboard
@app.route('/student', methods=['GET', 'POST'])
def student_dashboard():
    if 'user_type' not in session or session['user_type'] != 'student':
        flash('Access denied. Students only.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'answer_sheet' in request.files:
            answer_sheet = request.files['answer_sheet']
            if allowed_file(answer_sheet.filename):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(answer_sheet.filename))
                answer_sheet.save(filepath)

                # Insert uploaded document details into UploadedDocuments table
                cursor.execute(
                    "INSERT INTO UploadedDocuments (user_id, document_type, file_path) VALUES (%s, %s, %s)",
                    (session['user_id'], 'answer_sheet', filepath)
                )
                db.commit()

                session['uploaded_file'] = filepath
                flash('File uploaded successfully')
                return redirect(url_for('evaluate'))
            else:
                flash('Invalid file type')
    return render_template('student_dashboard.py')

# OCR and text processing route
@app.route('/evaluate')
def evaluate():
    if 'user_type' not in session or session['user_type'] != 'student':
        flash('Access denied. Students only.')
        return redirect(url_for('login'))

    filepath = session.get('uploaded_file')
    if not filepath:
        flash('No file to evaluate')
        return redirect(url_for('student_dashboard'))

    answer_key_path = os.path.join(app.config['UPLOAD_FOLDER'], 'answer_key.pdf')
    if not os.path.exists(answer_key_path):
        flash('Answer key is missing. Please contact staff to upload it.')
        return redirect(url_for('student_dashboard'))

    try:
        extracted_text = ''
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ''
                extracted_text += page_text

        if not extracted_text:
            flash('No text could be extracted from the uploaded file.')
            return redirect(url_for('student_dashboard'))

        answer_key_text = ''
        with pdfplumber.open(answer_key_path) as pdf:
            for page in pdf.pages:
                answer_key_text += page.extract_text() or ''

        if not answer_key_text:
            flash('No text could be extracted from the answer key.')
            return redirect(url_for('student_dashboard'))

        vectorizer = TfidfVectorizer().fit_transform([extracted_text, answer_key_text])
        similarity_score = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]
        marks = float(similarity_score * 100)  # Convert to native Python float

        # Insert marks into the EvaluationResults table
        cursor.execute(
            "INSERT INTO EvaluationResults (user_id, register_number, marks) VALUES (%s, %s, %s)",
            (session['user_id'], session.get('register_number'), marks)
        )
        db.commit()

        flash(f'Similarity score: {marks:.2f}%')
    except Exception as e:
        flash(f'Error during evaluation: {str(e)}')

    return redirect(url_for('student_dashboard'))

# Sending email route
def send_email(recipient, subject, body, attachment_path=None):
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))
    if attachment_path:
        try:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                message.attach(part)
        except FileNotFoundError:
            flash(f'Attachment {os.path.basename(attachment_path)} not found.')

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message.as_string())
        server.quit()
        flash('Email sent successfully.')
    except smtplib.SMTPException as e:
        flash(f'Error sending email: {str(e)}')

# Download PDF report route
@app.route('/download_report')
def download_report():
    if 'user_type' not in session or session['user_type'] != 'staff':
        flash('Access denied. Staff only.')
        return redirect(url_for('login'))

    # Fetch evaluation data from the database
    cursor.execute("SELECT Users.name, Users.register_number, EvaluationResults.marks FROM EvaluationResults JOIN Users ON EvaluationResults.user_id = Users.id")
    results = cursor.fetchall()

    # Create a PDF report
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Student Marks Report", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.cell(40, 10, "Name")
    pdf.cell(40, 10, "Register Number")
    pdf.cell(40, 10, "Marks")
    pdf.ln()

    for row in results:
        pdf.cell(40, 10, row[0])
        pdf.cell(40, 10, row[1])
        pdf.cell(40, 10, f"{row[2]:.2f}")
        pdf.ln()

    report_path = os.path.join(app.config['UPLOAD_FOLDER'], 'marks_report.pdf')
    pdf.output(report_path)

    # Send the PDF file as a response to download
    return send_file(report_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
