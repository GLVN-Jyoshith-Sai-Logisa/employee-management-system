from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(80))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    salary = db.Column(db.Integer)

    def __repr__(self):
        return f"<Employee {self.name}>"

@app.route('/')
def home():
    return redirect('/employees')

@app.route('/employees')
def view_employees():
    query = request.args.get('q', '')
    if query:
        employees = Employee.query.filter(
            (Employee.name.contains(query)) | (Employee.department.contains(query))
        ).all()
    else:
        employees = Employee.query.all()
    return render_template('employees.html', employees=employees, query=query)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        new_emp = Employee(
            name=request.form['name'],
            department=request.form['department'],
            position=request.form['position'],
            email=request.form['email'],
            phone=request.form['phone'],
            salary=request.form['salary']
        )
        db.session.add(new_emp)
        db.session.commit()
        return redirect('/employees')
    return render_template('add_employee.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    emp = Employee.query.get_or_404(id)
    if request.method == 'POST':
        emp.name = request.form['name']
        emp.department = request.form['department']
        emp.position = request.form['position']
        emp.email = request.form['email']
        emp.phone = request.form['phone']
        emp.salary = request.form['salary']
        db.session.commit()
        return redirect('/employees')
    return render_template('edit_employee.html', emp=emp)

@app.route('/delete/<int:id>')
def delete_employee(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect('/employees')
    
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)