from flask import Flask, render_template, request

import numpy as np

app = Flask(__name__)

def definir_activos():
    return ["Acciones", "Bonos", "Oro"], np.array([8, 5, 6])

def definir_matriz_riesgo():
    return np.array([
        [0.1, 0.02, 0.03],
        [0.02, 0.05, 0.01],
        [0.03, 0.01, 0.07]
    ])

def calcular_pesos(riesgo, rendimientos):
    pesos = np.linalg.solve(riesgo, rendimientos)
    return pesos / np.sum(pesos)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        try:
            capital = float(request.form["capital"])
            activos, rendimientos = definir_activos()
            riesgo = definir_matriz_riesgo()
            pesos = calcular_pesos(riesgo, rendimientos)
            inversiones = [(activos[i], round(pesos[i] * capital, 2), round(pesos[i] * 100, 2)) for i in range(len(activos))]
            rendimiento_total = round(np.dot(pesos, rendimientos), 2)
            resultado = {"inversiones": inversiones, "rendimiento_total": rendimiento_total}
        except:
            resultado = {"error": "Por favor, ingrese un capital válido."}
    
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
