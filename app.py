from flask import Flask, render_template, redirect, url_for,request ,session,flash
from flask_session import Session
import secrets
from flask_mysqldb import MySQL
import os
from config import *
import uuid
import razorpay.utility



app = Flask(__name__)


# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'school_result'

mysql = MySQL(app)
client = razorpay.Client(auth=(test_key, test_secret))

# Configure session secret key
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/student')
def student_page():
    return render_template('student.html')


@app.route('/contact')
def contact_page():
    # Handle contact page logic and rendering
    return render_template('contact.html')

@app.route('/about')
def about_page():
    # Handle about page logic and rendering
    return render_template('about.html')

@app.route

# Add routes for pay fees and view results pages
@app.route('/pay-fees')
def pay_fees():
    # Handle pay fees logic and rendering
    return render_template('pay_fees.html')



@app.route('/check-result', methods=['GET', 'POST'])
def check_result():
    return render_template('check_result.html')

@app.route('/delete_payment_redirect')
def delete_payment_redirect():
    return render_template("delete_payment_record.html")

@app.route('/delete_admission_redirect')
def delete_admission_redirect():
    return render_template("delete_admission_record.html")



@app.route('/payment', methods=['GET', 'POST'])
def payment():
    global student_name1,mother_name1,roll_no1,amount
    if request.method == 'POST':
        student_name1 = request.form['student_name']
        email = request.form['email']
        contact = request.form['contact']
        mother_name1= request.form['mother_name']
        roll_no1 = request.form['roll_number']
        amount= int(request.form['amount'])  # Get the amount from the form
        print(email,contact)
        # Generate order data with a unique order ID and receipt
        order_id = str(uuid.uuid4())  # Generate a unique order ID
        receipt = str(uuid.uuid4())  # Generate a unique receipt
        data = {
            "amount": amount * 100,  # Convert to paise
            "currency": "INR",
            "receipt": receipt,
            "partial_payment": False
        }
        payment = client.order.create(data=data)

        # Render the payment template with the order details
        order_id = payment['id']
        print("process payment function")
        return render_template('payment.html', order_id=order_id, student_name=student_name1, email=email, contact=contact, roll_no=roll_no1, mother_name=mother_name1, amount=amount,test_key=test_key)

app.secret_key = secrets.token_hex(16)  # Generate a secret key for session encryption

# Configure the session to use server-side storage
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sessions')
Session(app)

# Teacher credentials (replace with your actual database or secure storage)
TEACHER_CREDENTIALS = {
    'admin': 'password'

    # Add more teacher IDs and passwords
}

@app.route('/delete_payment_record', methods=['GET', 'POST'])
def delete_payment_record():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        mother_name = request.form['mother_name']

        # Connect to the MySQL database
        cursor = mysql.connection.cursor()

        # Delete the record from the payments_info table
        query = "DELETE FROM payments_info WHERE roll_no = %s AND mother_name = %s"
        values = (roll_no, mother_name)
        cursor.execute(query, values)
        print("payment record deleted successfully ")
        mysql.connection.commit()

        if cursor.rowcount > 0:
            flash('Payment record deleted successfully', 'success')
        else:
            flash('No payment record found with the provided Roll Number and Mother\'s Name', 'error')

        cursor.close()

    return render_template('delete_payment_record.html')


@app.route('/delete_admission_record', methods=['GET', 'POST'])
def delete_admission_record():
    if request.method == 'POST':
        id = request.form['id']
        mother_name = request.form['mother_name']

        # Connect to the MySQL database
        cursor = mysql.connection.cursor()

        # Delete the record from the admission_info table
        query = "DELETE FROM admission_info WHERE id = %s AND mother_name = %s"
        values = (id, mother_name)
        cursor.execute(query, values)
        print("delete admission record successfully")
        mysql.connection.commit()

        if cursor.rowcount > 0:
            flash('Admission record deleted successfully', 'success')
        else:
            flash('No admission record found with the provided ID and Mother\'s Name', 'error')

        cursor.close()

    return render_template('delete_admission_record.html')



@app.route('/teacher', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_id = request.form['teacher_id']
        password = request.form['password']

        # Check if the teacher ID and password match
        if teacher_id in TEACHER_CREDENTIALS and TEACHER_CREDENTIALS[teacher_id] == password:
            session['teacher_id'] = teacher_id  # Store the teacher_id in the session
            return redirect(url_for('teacher_dashboard'))
        else:
            error = 'Invalid Teacher ID or Password'
            return render_template('teacher.html', error=error)

    return render_template('teacher.html')

@app.route('/teacher_dashboard')
def teacher_dashboard():
    # Check if the user is authenticated (teacher_id in session)
    if 'teacher_id' in session:
        # Render the teacher dashboard template or perform other actions
        return render_template('teacher_dashboard.html')
    else:
        # Redirect to the teacher login page if not authenticated
        return redirect(url_for('teacher_login'))






app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sessions')
Session(app)

# Admin credentials (replace with your actual database or secure storage)
ADMIN_CREDENTIALS = {
    'admin': 'password'
    # Add more admin IDs and passwords
}

@app.route('/admin_check', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']

        # Check if the admin ID and password match
        if admin_id in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[admin_id] == password:
            session['admin_id'] = admin_id  # Store the admin_id in the session
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid Admin ID or Password'
            return render_template('admin_check.html', error=error)

    return render_template('admin_check.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # Check if the user is authenticated (admin_id in session)
    if 'admin_id' in session:
        # Render the admin dashboard template or perform other actions
        return render_template('admin_dashboard.html')
    else:
        # Redirect to the admin login page if not authenticated
        return redirect(url_for('admin_login'))

@app.route('/fill_result')
def fill_result():
    # Render the template for filling student results
    # or perform the necessary logic for filling results
    return render_template('fill_result.html')




@app.route('/submit_scores', methods=['POST'])
def submit_scores():
    if request.method == 'POST':
        # Get form data and remove leading/trailing whitespace
        name = request.form['name'].strip()
        mother_name = request.form['motherName'].strip()
        roll_no = request.form['rollNo'].strip()
        physics = request.form['physics']
        chemistry = request.form['chemistry']
        biology = request.form['biology']
        math = request.form['math']

        # Connect to the MySQL database
        cur = mysql.connection.cursor()

        # Insert data into the student_scores table
        query = "INSERT INTO student_scores (name, mother_name, roll_no, physics, chemistry, biology, math) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (name, mother_name, roll_no, physics, chemistry, biology, math)
        cur.execute(query, values)

        # Commit the changes and close the connection
        mysql.connection.commit()
        cur.close()

        flash('Scores submitted successfully', 'success')
        return render_template('subject_score_submission.html')
    return 'Error: Invalid request method'



@app.route('/delete_record', methods=['GET', 'POST'])
def delete_record():
    if request.method == 'POST':
        roll_no = request.form['roll_no'].strip()
        mother_name = request.form['mother_name'].strip()

        # Connect to the MySQL database
        cursor = mysql.connection.cursor()

        # Delete the record from the student_scores table
        query = "DELETE FROM student_scores WHERE roll_no = %s AND mother_name = %s"
        values = (roll_no, mother_name)
        cursor.execute(query, values)
        mysql.connection.commit()

        if cursor.rowcount > 0:
            flash('Record deleted successfully', 'success')
        else:
            flash('No record found with the provided Roll Number and Mother\'s Name', 'error')

        cursor.close()

    return render_template('delete_record.html')




@app.route('/view-scores', methods=['GET'])
def view_scores():
  # Connect to the MySQL database
    cur = mysql.connection.cursor()

    # Execute a SELECT query to fetch all data from the student_scores table
    query = "SELECT * FROM student_scores"
    cur.execute(query)

    # Fetch all rows from the result
    rows = cur.fetchall()

    # Close the cursor
    cur.close()

    # Calculate total score, percentage, and rank for each student
    student_data = []
    for row in rows:
        id, name, mother_name, roll_no, physics, chemistry, biology, math, created_at = row
        total_score = physics + chemistry + biology + math
        percentage = (total_score / 400) * 100
        student_data.append((id, name, mother_name, roll_no, physics, chemistry, biology, math, total_score, percentage, created_at))

    # Sort the student data by total score in descending order
    student_data.sort(key=lambda x: (-x[9], x[0]))  # Sort by total score in descending order, then by id in ascending order

    # Assign ranks to students
    rank = 1
    prev_score = None
    ranked_student_data = []
    for data in student_data:
        if prev_score != data[9]:
            prev_score = data[9]
            rank = ranked_student_data[-1][11] + 1 if ranked_student_data else 1
        ranked_student_data.append(data + (rank,))

    # Render the HTML template and pass the ranked student data
    return render_template('view_scores.html', students=ranked_student_data)
    
@app.route('/check-rank', methods=['GET', 'POST'])
def check_rank():
    if request.method == 'POST':
        roll_number = request.form['roll_no'].strip()
        mother_name = request.form['mother_name'].strip()
        # Connect to the MySQL database
        cur = mysql.connection.cursor()
        # Query to retrieve student data
        query = "SELECT id, name, mother_name, roll_no, physics, chemistry, biology, math, created_at FROM student_scores WHERE roll_no = %s AND mother_name = %s"
        cur.execute(query, (roll_number, mother_name))
        student = cur.fetchone()
        if student:
            # Unpack student data
            id, name, mother_name, roll_no, physics, chemistry, biology, math, created_at = student
            # Calculate the total score and percentage
            total_score = physics + chemistry + biology + math
            percentage = (total_score / 400) * 100
            # Calculate the rank
            rank = calculate_rank(total_score)
            # Check if the student passed or failed
            passed = percentage >= 40
            # Render the success or failure template
            if passed:
                return render_template('success.html', name=name, roll_no=roll_no, score=percentage, rank=rank, physics=physics, chemistry=chemistry, biology=biology, math=math)
            else:
                return render_template('failure.html', name=name, roll_no=roll_no, score=percentage, rank=rank, physics=physics, chemistry=chemistry, biology=biology, math=math)
        else:
            cur.close()
            return "Invalid roll number or mother's name."
    # return render_template('check_result.html')
    return "What is missing?"

def calculate_rank(total_score):
    # Connect to the MySQL database
    cur = mysql.connection.cursor()

    # Query to retrieve all student scores sorted by total score in descending order
    query = "SELECT id, physics + chemistry + biology + math AS total_score FROM student_scores ORDER BY total_score DESC"
    cur.execute(query)
    scores = cur.fetchall()

    # Find the rank of the student's score
    rank = 1
    prev_score = None
    for score in scores:
        if prev_score != score[1]:
            prev_score = score[1]
            if score[1] == total_score:
                break
            rank += 1

    cur.close()
    return rank




@app.route('/payment_success', methods=['POST'])
def payment_success():
    global Order_ID,Payment_ID
    # Get the payment data from Razorpay
    payment_data = request.get_json()

    # Check if the required keys are present in the payment data
    required_keys = ['student_name', 'roll_no', 'mother_name', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'amount', 'email', 'contact']
    missing_keys = [key for key in required_keys if key not in payment_data]

    if missing_keys:
        print(f"Missing keys in payment data: {', '.join(missing_keys)}")
        print(f"Received payment data: {payment_data}")
        return "Missing required data in the payment request.", 400

    # Extract the values from the payment data
    student_name = payment_data['student_name']
    roll_no = payment_data['roll_no']
    mother_name = payment_data['mother_name']
    order_id = payment_data['razorpay_order_id']
    payment_id = payment_data['razorpay_payment_id']
    signature = payment_data['razorpay_signature']
    amount = int(payment_data['amount'])
    email = payment_data['email']
    contact = payment_data['contact']
    Order_ID=order_id
    Payment_ID=payment_id
    # Store the payment data in the MySQL database
    cur = mysql.connection.cursor()
    sql = "INSERT INTO payments_info (student_name, roll_no, mother_name, order_id, payment_id, signature, amount, email, contact) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (student_name, roll_no, mother_name, order_id, payment_id, signature, amount, email, contact)
    cur.execute(sql, values)
    mysql.connection.commit()
    cur.close()

    # Handle the payment success logic here
    print("Payment successful:", payment_data)
    return "Payment successful."




@app.route('/receive-payment')
def receive_payment():
    # Retrieve all the data from the payments_info table
    cur = mysql.connection.cursor()
    query = "SELECT * FROM payments_info"
    cur.execute(query)
    payment_data = cur.fetchall()
    cur.close()

    # Render the receive_payment.html template and pass the payment data
    return render_template('receive_payment.html', payment_data=payment_data)
@app.route("/admission_page")
def admission_page():
      
      return render_template('admission.html')
 
@app.route('/admission', methods=['GET', 'POST'])
def admission():
    
    global ad_student_name,ad_mother_name,ad_mother_occupation,ad_father_occupation,ad_standard,ad_address,ad_taluka,ad_district,ad_school,ad_email,ad_contact,admission_fees
    print("stage 1")
    if request.method == 'POST':
        print("2 stage")
        # Retrieve form data
        ad_student_name = request.form['student_name']
        ad_mother_name = request.form['mother_name']
        ad_mother_occupation = request.form['mother_occupation']
        ad_father_occupation = request.form['father_occupation']
        ad_standard = request.form['standard']
        ad_address = request.form['address']
        ad_taluka = request.form['taluka']
        ad_district = request.form['district']
        ad_school=request.form['school']
        ad_email=request.form['email']
        ad_contact=request.form['contact']

        if 'pay_fees' in request.form:
            print("stage 4")
            # Generate order data for admission fee payment (₹10)
            order_id = str(uuid.uuid4())
            receipt = str(uuid.uuid4())
            amount=int(500*100)  # change value here to change admission fees amount in paisa
            admission_fees=amount
            data = {
                "amount": amount,  # ₹ in paise
                "currency": "INR",
                "receipt": receipt,
                "partial_payment": False
            }
            payment = client.order.create(data=data)

            # Render the payment template with the order details
            order_id = payment['id']
            return render_template('admission_payment.html', order_id=order_id, amount=amount,test_key=test_key)
    
    return render_template('admission.html')


@app.route('/admission_list')
def admission_list():
    # Connect to the MySQL database
    cur = mysql.connection.cursor()

    # Retrieve all the data from the admission_info table
    query = "SELECT * FROM admission_info"
    cur.execute(query)
    admission_data = cur.fetchall()

    # Close the cursor
    cur.close()

    # Render the admission_list.html template and pass the admission_data
    return render_template('admission_list.html', data=admission_data)

@app.route('/payment_success_for_admission', methods=['POST'])
def payment_success_for_admission():
 
    global ad_order_id,ad_payment_id
    # Get the payment data from Razorpay
    payment_data = request.get_json()
    print("enter to payment_success_for admission")
    student_name=ad_student_name
    mother_name=ad_mother_name
    mother_occupation=ad_mother_occupation
    father_occupation=ad_father_occupation
    standard=ad_standard
    address=ad_address
    taluka=ad_taluka
    district=ad_district
    school=ad_school
    email=ad_email
    contact=ad_contact
    



    order_id = payment_data['razorpay_order_id']
    payment_id = payment_data['razorpay_payment_id']
    signature = payment_data['razorpay_signature']
    ad_order_id=order_id
    ad_payment_id=payment_id
    amount=(admission_fees/100)

    cur = mysql.connection.cursor()
    sql = "INSERT INTO admission_info (student_name, mother_name,mother_occupation, father_occupation,standard,address,taluka,district,school,email,contact,order_id, payment_id, signature,amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"
    values = (student_name,mother_name,mother_occupation,father_occupation,standard,address,taluka,district,school,email,contact,order_id, payment_id,signature, amount)
    cur.execute(sql, values)
    mysql.connection.commit()
    print("data save into mysql db")
    cur.close()

    print("Payment successful  in admission_info:", payment_data)
    return "Payment successful."

@app.route("/payment_pass")
def payment_pass():

    return render_template("payment_pass.html",student_name=student_name1,mother_name=mother_name1,roll_no=roll_no1,amount=amount,order_id=Order_ID,payment_id=Payment_ID)


@app.route("/payment_fail")
def payment_fail():

    return render_template("payment_fail.html")

@app.route('/admission_payment_pass')
def admission_payment_pass():
    amount=(admission_fees/100)

    return render_template("admission_pass.html",name=ad_student_name,mother_name=ad_mother_name,standard=ad_standard,order_id=ad_order_id,payment_id=ad_payment_id,amount=amount)

@app.route("/admission_payment_fail")
def admission_payment_fail():
        
    return render_template("admission_payment_fail.html")

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port='5000')

    
