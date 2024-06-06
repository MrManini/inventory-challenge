from flask import Flask, render_template, request, redirect, url_for,jsonify
import webbrowser, pymysql, json, pytz
from threading import Timer
from datetime import datetime, timedelta

app = Flask(__name__, static_folder="static")

#f = open('Pagina_estaciones/estacion.json')
#data = json.load(f)
#f.close()
'''
mysql = pymysql.connect(
    host = data['host'],
    user = data['user'],
    password = data['password'],
    db = data['database'],
    cursorclass = pymysql.cursors.DictCursor
)'''

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        horas = int(request.form["horas"])
        minutos = int(request.form["minutos"])
        segundos = int(request.form["segundos"])
        milisegundos = int(request.form["milisegundos"])*10
        horas_inactivo = int(request.form["horas_inactivo"])
        minutos_inactivo = int(request.form["minutos_inactivo"])
        segundos_inactivo = int(request.form["segundos_inactivo"])
        milisegundos_inactivo = int(request.form["milisegundos_inactivo"])*10
        tipo_produccion = request.form.get("tipo_de_produccion", "off")  # Usar get() con un valor predeterminado
        if tipo_produccion=="on":
            print("Hola")
        else:
            print("mundo")
        work = timedelta(hours=horas, minutes=minutos, seconds=segundos, milliseconds=milisegundos)
        timeout = timedelta(hours=horas_inactivo, minutes=minutos_inactivo, seconds=segundos_inactivo, milliseconds=milisegundos_inactivo)
        total = work + timeout
        independent_stations(work, timeout, total)

    return render_template("index.html")


'''
@app.route("/handle_option", methods=["POST"])
def handle_option():
    selected_option = request.json["option"]
    if selected_option=="opcion1":
        print("Hola")
    else:
        print("Mundo")
    return jsonify({"message": ""}) # No borrar
'''


def independent_stations(work, timeout, total):
    now = datetime.now(pytz.timezone('America/Bogota'))
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    #station = data['user'][-1]

    #cursor = mysql.cursor()
    query = "INSERT INTO `stations` VALUES (%s, %s, %s, %s, %s)"
    #cursor.execute(query, (now, station, work, timeout, total))
    #mysql.commit()

def open_browser():
    url = "http://localhost:5000"
    webbrowser.open_new_tab(url)

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)  # Deshabilita el cargador automático