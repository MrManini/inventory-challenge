import webbrowser
from flask import Flask, render_template, request,redirect,url_for, session
import pymysql, socket
from threading import Timer

app = Flask(__name__, static_folder="static")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'central'
app.config['MYSQL_PASSWORD'] = 'Central-Stati0n'
app.config['MYSQL_DB'] = 'storage'
HOST = "192.168.0.125"
PORT = 8080

mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)

app.secret_key = 'secret_key'  

def send_command(command, color = ""):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        light = color + command
        s.sendall(light.encode())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Aquí puedes acceder a los datos del formulario
        correo = request.form['correo']

        contraseña=request.form['contraseña']
        # Puedes hacer lo que necesites con los datos, como guardarlos en una base de datos
        if correo == 'jhonatan@hotmail.com' and contraseña == '12345':
            session['previous_state'] = 'entrada'  # Almacena el estado anterior en la sesión
            # Redirige a otra página HTML si las credenciales son correctas
            return redirect(url_for('entrada_bodega'))
    return render_template("login.html")

@app.route('/entrada_bodega',methods=['GET','POST'])
def entrada_bodega():
    session['previous_state'] = 'entrada'  # Actualiza el estado anterior en la sesión
    if request.method=='POST': #TODO: cambiar a 31 
        productos = tuple(int(request.form[f"cantidad_producto{i}"]) for i in range(1, 5))
        if sum(productos) != 0:
            print(productos)
            cursor = mysql.cursor()
            query = "INSERT INTO `orders` (`kit1`, `kit2`, `kit3`, `kit4`) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, productos)
            mysql.commit()
    # Renderiza la otra página HTML
    return render_template('ingresar_bodega.html')

@app.route('/salida_bodega',methods=['GET','POST'])
def salida_bodega(): #TODO: cambiar modo de lectura y cambiar a 31
    session['previous_state'] = 'salida'  # Actualiza el estado anterior en la sesión
    if request.method=='POST': #TODO: cambiar a 31 
        productos = tuple(int(request.form[f"s_cantidad_producto{i}"]) for i in range(1, 5))
        for i in range(4):
            if productos[i] != 0:
                send_command(str(i+1), "c")
    return render_template('sacar_bodega.html')

@app.route('/inventario',methods=['GET','POST'])
def inventario():
    data = []  # Inicializar data con una lista vacía

    if request.method == 'POST':
        cursor = mysql.cursor()
        mysql.commit()
        consulta = request.form.get("tipo_de_consulta")

        if consulta == "Consultar inventario":
            print("Hola")
            cursor = mysql.cursor()
            cursor.execute("SELECT * FROM inventory;")
            data = cursor.fetchall()
        elif consulta == "Consultar tiempo de linea de produccion":
            print("mundo")
            cursor = mysql.cursor()
            cursor.execute("SELECT * FROM stations;")
            data = cursor.fetchall()

    previous_state = session.get('previous_state', 'vacio')  # Obtiene el estado anterior de la sesión

    return render_template('inventario.html', data=data, last_state=previous_state)
@app.route('/logout')
def logout():
    return redirect(url_for('index'))


def open_browser():
    url = "http://localhost:5000"
    webbrowser.open_new_tab(url)

if __name__ == '__main__':
    cursor = mysql.cursor()
    cursor.execute("TRUNCATE TABLE orders;")
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)  # Deshabilita el cargador automático