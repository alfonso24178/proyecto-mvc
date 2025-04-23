import requests

API_BASE = "https://pycsoftwaremx.com/david/rest_api_alu_materias_daw/api/"

# Lista simulada para materias agregadas manualmente
materias_simuladas = []

def get_all_materias():
    response = requests.get(API_BASE + "lista_planes_materias.php")
    try:
        data = response.json()
        return data.get("body", []) + materias_simuladas
    except ValueError:
        print("❌ No es JSON válido.")
        return materias_simuladas  # Mostrar solo las simuladas si la API falla

def get_materia(cve_plan, clave):
    todas = get_all_materias()
    for m in todas:
        if str(m.get("clave")) == str(clave) and str(m.get("cve_plan")) == str(cve_plan):
            return {"success": True, "data": m}
    return {"success": False, "message": "Materia no encontrada."}

def create_materia(data):
    materias_simuladas.append({
        "clave": data["clave"],
        "cve_plan": data["cve_plan"],
        "materia": data["nombre"],
        "creditos": data["creditos"],
        "horas_prac": "",
        "horas_teo": "",
        "grado": ""
    })
    print("✅ Materia simulada guardada:", data)
    return {"success": True, "message": "Materia simulada creada."}

def update_materia(data):
    for m in materias_simuladas:
        if m["clave"] == data["clave"]:
            m["materia"] = data["nombre"]
            m["creditos"] = data["creditos"]
            return {"success": True, "message": "Materia actualizada."}
    return {"success": False, "message": "No encontrada para actualizar."}

def delete_materia(clave):
    global materias_simuladas
    materias_simuladas = [m for m in materias_simuladas if str(m["clave"]) != str(clave)]
    return {"success": True, "message": "Materia eliminada (si existía)."}
