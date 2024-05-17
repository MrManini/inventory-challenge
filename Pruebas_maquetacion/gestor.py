from flask import Flask, render_template, request,redirect,url_for
import pymysql.cursors

app = Flask(__name__, static_folder="static")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jhonatan'
app.config['MYSQL_DB'] = 'datostiempo'

mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Aquí puedes acceder a los datos del formulario
        correo = request.form['correo']

        contraseña=request.form['contraseña']
        # Puedes hacer lo que necesites con los datos, como guardarlos en una base de datos
        if correo == 'jhonatan@hotmail.com' and contraseña == '12345':
            # Redirige a otra página HTML si las credenciales son correctas
            return redirect(url_for('entrada_bodega'))

    return render_template("login.html")

@app.route('/entrada_bodega',methods=['GET','POST'])
def entrada_bodega():
    if request.method=='POST':
        producto1=request.form["cantidad_producto1"]
        print(f"Numero: {producto1}")

        producto2=request.form["cantidad_producto2"]
        print(f"Numero: {producto2}")

        producto3=request.form["cantidad_producto3"]
        print(f"Numero: {producto3}")

        producto4=request.form["cantidad_producto4"]
        print(f"Numero: {producto4}")
    # Renderiza la otra página HTML
    return render_template('ingresar_bodega.html')

@app.route('/salida_bodega',methods=['GET','POST'])
def salida_bodega():
    if request.method=='POST':
        producto1=request.form["s_cantidad_producto1"]
        print(f"Numero salida: {producto1}")

        producto2=request.form["s_cantidad_producto2"]
        print(f"Numero salida: {producto2}")

        producto3=request.form["s_cantidad_producto3"]
        print(f"Numero salida: {producto3}")

        producto4=request.form["s_cantidad_producto4"]
        print(f"Numero salida: {producto4}")

    return render_template('sacar_bodega.html')

@app.route('/inventario',methods=['GET','POST'])
def inventario():
    if request.method=='POST':
        cursor = mysql.cursor()
        mysql.commit()
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM decodificaciones")
    data = cursor.fetchall()
    return render_template('inventario.html',data=data)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)