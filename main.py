from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

"""
    Flask CRUD Web Application. To start set correctly the database configuration below.
    Ussage: python3 main.py
"""

"""MySQL database configuration"""

app = Flask(__name__)
app.config['MYSQL_HOST'] = '' #MySQL host.
app.config['MYSQL_USER'] = '' #MySQL user.
app.config['MYSQL_PASSWORD'] = '' #MySQL password.
app.config['MYSQL_DB'] = '' #MySQL database name.
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

"""Index of the Application"""
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
        
    return render_template('index.html', contacts=data)


"""Add contact function"""
@app.route('/add-contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO contacts (fullname, phone, email) VALUES ('{fullname}', '{phone}', '{email}')")
        mysql.connection.commit()
        flash('Contact added succesfully')

        return redirect(url_for('index'))

"""Edit contact function"""
@app.route('/edit-contact/<string:id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT * FROM contacts WHERE id={id}')
    data = cur.fetchall()
    
    return render_template('edit-contact.html', contact=data[0])

"""Delete contact function"""
@app.route('/delete-contact/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute(f'DELETE FROM contacts WHERE id={id}')
    mysql.connection.commit()
    flash('Contact deleted succesfully')
    
    return redirect(url_for('index'))

"""Update contact function"""
@app.route('/update/<string:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(f"""
            UPDATE contacts
            SET fullname = '{fullname}',
            email = '{email}',
            phone = '{phone}'
            WHERE id = {id}
        """)
        mysql.connection.commit()
        flash('Contact updated succesfully')

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0', debug=True)