#We add the libreries we need 
from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#The object for the instace is created
app = Flask(__name__)

#We set the values to connect to the DB in our host
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbpython'

mysql = MySQL(app)

#Sesion for get into the app
app.secret_key = 'key'

#This is the function for excecute the main page of our app
@app.route('/')
def index():
	curs = mysql.connection.cursor()
	#We make the query to get the contacts of the DB
	curs.execute('SELECT * FROM datos')
	resultado = curs.fetchall()
	#The values are send to the main page to get showed
	return render_template('front.html', data = resultado)

#This is the route that we need to add a contact
@app.route('/add', methods=['POST'])
def add():
	if request.method == 'POST':
		#The values of the textboxs are saved in variables
		nombre = request.form['nombre']
		telefono = request.form['telefono']
		email = request.form['email']
		#The query is excecuted
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO `datos`(`Nombre`, `Telefono`, `Email`) VALUES ('"+nombre+"', '"+telefono+"', '"+email+"')")
		mysql.connection.commit()
		#The message is send to our main page
		flash('Contacto agregado')
		return redirect(url_for('index'))

#This is the route to delete a contact
@app.route('/delete/<string:id>')
def delete(id):
	cur = mysql.connection.cursor()
	#With the id, we search the value and gets deleted
	cur.execute("DELETE FROM datos WHERE id = " +id)
	mysql.connection.commit()
	flash('Contacto eliminado')
	return redirect(url_for('index'))

#Here is the route to modify a contact, receiving the id of the contact
@app.route('/modify/<string:id>')
def modify(id):
	#Here we search for the values of the contact
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM datos WHERE id = '+id)
	datos = cur.fetchall()
	#And sent them for another view of our app, to confirm the new values of the contact
	return render_template('editar.html', dato = datos[0])

#This is the function to update a contact, receiving the id of the contact and the new values
@app.route('/update/<string:id>', methods = ['POST'])
def update(id):
	if request.method == 'POST':
		#We save the values in variables to make the query
		nombre = request.form['nombre']
		telefono = request.form['telefono']
		email = request.form['email']
		cur = mysql.connection.cursor()
		#The query is executed to update the values in the DB
		cur.execute("UPDATE `datos` SET `Nombre` = '"+nombre+"', `Telefono` = "+telefono+", `Email` = '"+email+"' WHERE ID = " +id)
		mysql.connection.commit()
		flash('Contacto actualizado')
		return redirect(url_for('index'))

#This is the function to search for an especific contact, receiving the id to search
@app.route('/buscar/<string:nombre>')
def busca(nombre):
	#We execut the query
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM datos WHERE Nombre = '"+nombre+"'")
	resul = cur.fetchall()
	#And returning the values we find
	return render_template('front.html', data = resul)

#We make the conection to out localhost on port 3000
if __name__=='__main__':
	app.run(port=3000, debug = True)




