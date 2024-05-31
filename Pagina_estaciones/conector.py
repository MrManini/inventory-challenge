from flask import Flask, render_template, request, redirect, url_for
import webbrowser
from threading import Timer

app = Flask(__name__, static_folder="static")

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        horas = request.form["horas"]
        minutos = request.form["minutos"]
        segundos = request.form["segundos"]
        milisegundos = request.form["milisegundos"]
        print(horas, minutos, segundos, milisegundos)

    return render_template("index.html")

@app.route('/ruta_inactivo', methods=["POST", "GET"])
def inactivo():
    if request.method == "POST":
        horas_inactivo = request.form["horas_inactivo"]
        minutos_inactivo = request.form["minutos_inactivo"]
        segundos_inactivo = request.form["segundos_inactivo"]
        milisegundos_inactivo = request.form["milisegundos_inactivo"]
        print(horas_inactivo, minutos_inactivo, segundos_inactivo, milisegundos_inactivo)
    return render_template("index.html")

def open_browser():
    url = "http://localhost:5000"
    webbrowser.open_new_tab(url)

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)  # Deshabilita el cargador automático