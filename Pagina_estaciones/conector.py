from flask import Flask, render_template, request, redirect, url_for,jsonify
import webbrowser, pymysql, json, pytz, os
from threading import Timer
from datetime import datetime, timedelta

app = Flask(__name__, static_folder="static")

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'estacion.json')
f = open(file_path)
data = json.load(f)
f.close()

mysql = pymysql.connect(
    host = data['host'],
    user = data['user'],
    password = data['password'],
    db = data['database'],
    cursorclass = pymysql.cursors.DictCursor
)

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
        work = timedelta(hours=horas, minutes=minutos, seconds=segundos, milliseconds=milisegundos)
        timeout = timedelta(hours=horas_inactivo, minutes=minutos_inactivo, seconds=segundos_inactivo, milliseconds=milisegundos_inactivo)
        total = work + timeout
        if tipo_produccion=="on":
            independent_stations(work, timeout, total)
        else:
            assembly_line(work, timeout)

    return render_template("index.html")


def assembly_line(work, timeout):
    station = int(data['user'][-1])
    
    if station == 1:
        now = datetime.now(pytz.timezone('America/Bogota'))
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        cursor = mysql.cursor()
        query = "INSERT INTO assembly_line (StartTime, WorkTime1, TimeOut1) VALUES (%s, %s, %s)"
        cursor.execute(query, (now, work, timeout))
        mysql.commit()
    elif station == 4:
        now = datetime.now(pytz.timezone('America/Bogota'))
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        cursor = mysql.cursor()
        query = """
                UPDATE assembly_line
                SET EndTime=%s, WorkTime4=%s, TimeOut4=%s
                WHERE WorkTime4 = '00:00:00.00'
                ORDER BY StartTime ASC LIMIT 1
                """
        cursor.execute(query, (now, work, timeout))
        query = """
            UPDATE assembly_line 
            SET TotalWorkTime = ADDTIME(ADDTIME(ADDTIME(WorkTime1, WorkTime2), WorkTime3), WorkTime4)
            WHERE TotalWorkTime = '00:00:00.00'
            ORDER BY StartTime ASC LIMIT 1
        """
        cursor.execute(query)
        query = """
            UPDATE assembly_line 
            SET TotalTimeOut = ADDTIME(ADDTIME(ADDTIME(TimeOut1, TimeOut2), TimeOut3), TimeOut4)
            WHERE TotalTimeOut = '00:00:00.00'
            ORDER BY StartTime ASC LIMIT 1
        """
        cursor.execute(query)
        query = """
            UPDATE assembly_line 
            SET TotalTime = ADDTIME(TotalWorkTime, TotalTimeOut)
            WHERE TotalTime = '00:00:00.00'
            ORDER BY StartTime ASC LIMIT 1
        """
        cursor.execute(query)
        mysql.commit()
    else:
        cursor = mysql.cursor()
        query = """
            UPDATE assembly_line 
            SET WorkTime%s = %s, TimeOut%s = %s
            WHERE WorkTime%s = '00:00:00.00'
            ORDER BY StartTime ASC LIMIT 1
        """
        cursor.execute(query, (station, work, station, timeout, station))
        mysql.commit()

def independent_stations(work, timeout, total):
    now = datetime.now(pytz.timezone('America/Bogota'))
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    station = data['user'][-1]

    cursor = mysql.cursor()
    query = "INSERT INTO `stations` VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (now, station, work, timeout, total))
    mysql.commit()
def open_browser():
    url = "http://localhost:5000"
    webbrowser.open_new_tab(url)

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)  # Deshabilita el cargador automático