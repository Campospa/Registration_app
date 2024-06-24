from flask import Flask, request, render_template, redirect, url_for, flash
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime 
import os


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Setup Database
engine = create_engine("sqlite:///demo.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# Define a class to register employees
class Registration(Base):
    __tablename__ = 'registration'
    id = Column(Integer, primary_key=True)
    department = Column(String)
    position = Column(String)
    hire_date = Column(DateTime, default=datetime.datetime.utcnow)
    

    # Define foreign key to employees table
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employees", back_populates="registration")

class Employees(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    

    registration = relationship("Registration", back_populates="employee")

    def __str__(self):
        return f"Employee_ID: {self.employee_id}, First Name: {self.first_name}, Last Name: {self.last_name}, Email: {self.email}, Job Title: {self.job_title}, Department: {self.department}, Hire Date: {self.hire_date}"

Base.metadata.create_all(engine)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        department = request.form['department']
        position = request.form['position']
        hire_date_str = request.form['hire_date']
        hire_date = datetime.datetime.strptime(hire_date_str, '%Y-%m-%d')
        
        new_employee = Employees(first_name=first_name, last_name=last_name, email=email)
        session.add(new_employee)
        session.commit()

        # Retrieve the ID of the newly created employee
        employee_id = new_employee.id

        
        new_registration = Registration(department=department, position=position, hire_date=hire_date, employee_id=employee_id )
        session.add(new_registration)
        session.commit()
             
        flash('Employee registered successfully!')
        return redirect(url_for('index'))
    
    return render_template('registration_form.html')

# A function to view all registered employees

# A function to delete employees

# A function to increase salary based on time on the job


if __name__ == '__main__':
    app.run(debug = True)
