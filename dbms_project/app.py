from multiprocessing import connection
from flask import Flask,render_template,request,flash
from flask_mysqldb import MySQL
from flask.helpers import url_for
import re
import random
from werkzeug.utils import redirect

app = Flask(__name__)
db= MySQL(app)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "users"
app.secret_key='shans'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/employee', methods=['GET','POST'])
def employee():
    if request.method=='POST':
        cur = db.connection.cursor()
        name = request.form.get('name')
        password=request.form.get('password')
        values = cur.execute("SELECT password FROM employee WHERE employee_id=%s",[name])
        data = cur.fetchall()
        if values==0:
            flash('Employee does not exists, contact admin')
            return render_template('employee.html')
        if data == ((password,),):
            another_data = cur.execute("SELECT * FROM employee WHERE employee_id=%s",[name])
            full_data = cur.fetchall()
            cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'employee'")
            col_name = cur.fetchall()
            return render_template('employee_details.html',data=full_data,col_name=col_name)
        elif data!=password:
            flash('Incorrect password')
            return render_template('employee.html')

    if request.method=='GET':
        return render_template('employee.html')






        

@app.route('/admin',methods=['get','post'])
def employee_info():
    if request.method=='POST':
        cur = db.connection.cursor()
        name = request.form.get('name')
        password=request.form.get('password')
        values = cur.execute("SELECT password FROM employee WHERE employee_id  LIKE 'A%%' AND employee_id=%s",[name])
        data = cur.fetchall()
        if values==0:
                flash('Admin does not exists')
                return render_template('admin.html',data=data)
        if data == ((password,),):
                result = cur.execute("SELECT * FROM employee WHERE employee_id=%s",[name])
                admin_data = cur.fetchall()
                result_emp = cur.execute("SELECT name,employee_id,designation,rating FROM employee WHERE employee_id NOT LIKE 'A%'")
                all_emp_data = cur.fetchall()
                return render_template('admin_details.html',admin_data=admin_data,all_emp_data=all_emp_data)
        elif data!=password:
                flash('Incorrect password')
                return render_template('admin.html')
    
    if request.method=='GET':
        return render_template('admin.html')


@app.route('/delete/<string:emp_num>')
def delete(emp_num):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM employee WHERE employee_id=%s',[emp_num])
    db.connection.commit()
    cur.execute("SELECT name,employee_id,designation,rating FROM employee WHERE employee_id NOT LIKE 'A%'")
    complt_emp_info = cur.fetchall()
    flash("deleted successfully ")
    return render_template('admin_details.html',all_emp_data=complt_emp_info)


@app.route('/edit/<string:employee_num>',methods=['GET','POST'])
def edit(employee_num):
    cur = db.connection.cursor()
    values = cur.execute('SELECT * FROM employee WHERE employee_id = %s',[employee_num])
    data= cur.fetchall()
    if request.method == 'POST':
        name = request.form.get('name')
        Employee_ID = request.form.get('Employee_ID')
        joining_date = request.form.get('joining_date')
        Designation = request.form.get('Designation')
        salaray = request.form.get('salaray')
        Rating = request.form.get('Rating')
        bank_account_number = request.form.get('bank_account_number')
        contact_number = request.form.get('contact_number')
        Address = request.form.get('Address')
        Leaves_left = request.form.get('Leaves_left')
        worked_days = request.form.get('worked_days')
        password = request.form.get('password')
        cur = db.connection.cursor()
        values = cur.execute("UPDATE employee SET name = %s, employee_ID=%s,joining_date= %s, designation=%s,salaray=%s, rating=%s, bank_account_number=%s,contact_number= %s, Address=%s, leaves_left=%s,worked_days= %s, password=%s WHERE employee_id=%s",(name,Employee_ID,joining_date,Designation,salaray,Rating,bank_account_number,contact_number,Address,Leaves_left,worked_days,password,Employee_ID,))
        db.connection.commit()
        cur.execute("SELECT name,employee_id,designation,rating FROM employee WHERE employee_id NOT LIKE 'A%'")
        complt_emp_info = cur.fetchall()
        return render_template('admin_details.html',all_emp_data=complt_emp_info)
    if request.method =='GET':
        return render_template('edit.html',data=data)




@app.route('/insert',methods=['POST','GET'])
def insert():
    if request.method == 'POST':
        name = request.form.get('name')
        Employee_ID = request.form.get('Employee_ID')
        joining_date = request.form.get('joining_date')
        Designation = request.form.get('Designation')
        salaray = request.form.get('salaray')
        Rating = request.form.get('Rating')
        bank_account_number = request.form.get('bank_account_number')
        contact_number = request.form.get('contact_number')
        Address = request.form.get('Address')
        Leaves_left = request.form.get('Leaves_left')
        worked_days = request.form.get('worked_days')
        password = request.form.get('password')
        cur = db.connection.cursor()
        values = cur.execute("INSERT INTO  employee VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(name,Employee_ID,joining_date,Designation,salaray,Rating,bank_account_number,contact_number,Address,Leaves_left,worked_days,password,))
        db.connection.commit()
        flash("employee added")
        cur.execute("SELECT name,employee_id,designation,rating FROM employee WHERE employee_id NOT LIKE 'A%'")
        complt_emp_info = cur.fetchall()
        return render_template('admin_details.html',all_emp_data=complt_emp_info)

    return render_template('insert.html')


@app.route('/flights',methods=['POST','GET'])
def flight():
    if request.method=='POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        cur = db.connection.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'flight'")
        col_name = cur.fetchall()
        value = cur.execute('SELECT * FROM flight WHERE source_name = %s and destination_name=%s',(source,destination))
        if value==0:
            flash('No flights available')
            return render_template('flight.html')
        if value>0:
            flight_data = cur.fetchall()
            return render_template('flight.html',flight_data=flight_data,col_name=col_name,num=3)
    if request.method=='GET':
        return render_template('flight.html')







@app.route('/flightnum',methods=['POST','GET'])
def flightnum():
    if request.method=='POST':
        flightnum= request.form.get("flight_number")
        cur = db.connection.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'flight'")
        col_name = cur.fetchall()
        value = cur.execute('SELECT * FROM flight WHERE flight_number = %s',[flightnum])
        if value==0:
            flash('No flights available')
            return render_template('flightnum.html')
        if value>0:
            data = cur.fetchall()
            return render_template('flightnum.html',flight_data=data,col_name=col_name,num=3)
    if request.method=='GET':
        return render_template('flightnum.html')



@app.route('/book/<string:flight_num>',methods=['POST','GET'])
def book(flight_num):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM flight WHERE flight_number=%s',[flight_num])
    flight_data = cur.fetchall()
    
    if request.method =='POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        nationality = request.form.get('Nationality')
        gender = request.form.get('Gender')
        passport_number = request.form.get('passport_number')
        contact_number = request.form.get('contact_number')
        email = request.form.get('email')
        Address = request.form.get('Address')
        classtype = request.form.get('classtype')
        seatNumber = random.randint(1,300)
        price=2000
        pnr = flight_num+flight_data[0][6]+passport_number
        flight_number = flight_data[0][0]
        seats_available = cur.execute("SELECT seats_available FROM flight WHERE flight_number=%s",[flight_number])
        seats_available_data = cur.fetchall()
        if seats_available_data==0:
            flash('seat not available')
        else:
            cur.execute("INSERT INTO passenger VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)",(pnr, first_name, last_name, dob, nationality, gender, flight_number, email,passport_number,contact_number,Address))
            db.connection.commit()
            cur.execute("UPDATE flight SET seats_available =seats_available-1 WHERE flight_number=%s",[flight_number])
            db.connection.commit()
            cur.execute("INSERT INTO ticket VALUES(%s,%s,%s,%s,%s,%s)",(pnr,seatNumber,classtype,price,passport_number,flight_num))
            db.connection.commit()
            ticket = cur.execute("SELECT passenger.first_name, passenger.last_name, passenger.nationality, passenger.contact_number,passenger.passport_number,passenger.address,passenger.flight_number, flight.airline_name,flight.source_name,flight.source_code,flight.destination_name,flight.destination_code,flight.departure,flight.arrival FROM passenger INNER JOIN flight ON passenger.flight_number=flight.flight_number  WHERE passenger.passport_number= %s",[passport_number])

            if ticket>0:
                ticket_data = cur.fetchall()
                return render_template("ticket.html",ticket_data=ticket_data)

            
    
    return render_template('book.html',flight_data=flight_data)


@app.route('/searchpassenger',methods=['POST','GET'])
def searchpassenger():
    if request.method=='POST':
        passport_number =request.form.get('passport_number')
        cur = db.connection.cursor()
        value = cur.execute("SELECT passenger.passport_number, passenger.first_name ,flight.airline_name,flight.departure,flight.arrival,flight.source_name,flight.destination_name FROM passenger INNER JOIN flight ON passenger.flight_number=flight.flight_number  WHERE passenger.passport_number=%s",[passport_number])
        passenger_data = cur.fetchall()
        return render_template('home.html',passenger_data=passenger_data,value=value,num=3)
    return render_template('home.html')



@app.route('/passengers',methods=['GET','POST'])
def passengers():
    cur = db.connection.cursor()
    passengers = cur.execute("SELECT passenger.passport_number,passenger.first_name, passenger.last_name, passenger.contact_number,passenger.nationality,passenger.gender,ticket.PNR,ticket.Seat_number,ticket.Class FROM passenger INNER JOIN ticket ON passenger.passport_number=ticket.Passport_number")
    if passengers > 0:
        userDetails = cur.fetchall()
        return render_template('passenger.html',user_data=userDetails)
    else:
        flash('passengers not found')
        return render_template('passenger.html')



@app.route('/deleteEmp/<string:passport_number>')
def deleteEmp(passport_number):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM passenger WHERE passport_number=%s',[passport_number])
    db.connection.commit()
    passengers = cur.execute("SELECT passenger.passport_number,passenger.first_name, passenger.last_name, passenger.contact_number,passenger.nationality,passenger.gender,ticket.PNR,ticket.Seat_number,ticket.Class FROM passenger INNER JOIN ticket ON passenger.passport_number=ticket.Passport_number")
    if passengers > 0:
        userDetails = cur.fetchall()
    flash(f"deleted passenger passport number {passport_number}  successfully ")
    return render_template('passenger.html',user_data=userDetails)

@app.route('/deletePass/<string:passport_number>')
def deletePass(passport_number):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM passenger WHERE passport_number=%s',[passport_number])
    db.connection.commit()
    passengers = cur.execute("SELECT passenger.passport_number,passenger.first_name, passenger.last_name, passenger.contact_number,passenger.nationality,passenger.gender,ticket.PNR,ticket.Seat_number,ticket.Class FROM passenger INNER JOIN ticket ON passenger.passport_number=ticket.Passport_number")
    if passengers > 0:
        userDetails = cur.fetchall()

        flash(f"deleted passenger passport number {passport_number}  successfully ")
        return render_template('searchpassenger.html',user_data=userDetails)




@app.route('/searchPass',methods=['POST','GET'])
def passengernum():
    if request.method=='POST':
        flightnum= request.form.get("flight_number")
        cur = db.connection.cursor()
        passengers = cur.execute("SELECT passenger.passport_number,passenger.first_name, passenger.last_name, passenger.contact_number,passenger.nationality,passenger.gender,ticket.PNR,ticket.Seat_number,ticket.Class FROM passenger INNER JOIN ticket ON passenger.passport_number=ticket.Passport_number WHERE passenger.flight_number=%s",[flightnum])
        if passengers > 0:
            userDetails = cur.fetchall()
            return render_template('searchpassenger.html',passenger_data = userDetails,num=3)
        else:
            flash('no pasengers found')
            return render_template('searchpassenger.html')    
    if request.method=='GET':
        return render_template('searchpassenger.html')








if __name__ =='__main__':
    app.run(debug=True)


