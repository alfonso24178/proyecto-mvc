
from flask import Blueprint, render_template, request, redirect, url_for, send_file, session, send_from_directory, flash, current_app, jsonify
from app.models.models import Nivel, Municipio, Asunto, SolicitudTurno, Usuario
from .api_client import get_all_materias, get_materia, create_materia, update_materia, delete_materia
from app import db
from sqlalchemy import func
import requests
import os
from datetime import datetime, timedelta

from app.utils.ticket_factory import TicketFactory  # Importar la fábrica

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/solicitar', methods=['GET', 'POST'])
def solicitar():
    niveles = Nivel.query.all()
    municipios = Municipio.query.all()
    asuntos = Asunto.query.all()

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre_tramite = request.form['nombre_tramite']
            curp = request.form['curp']
            nombre = request.form['nombre']
            paterno = request.form['paterno']
            materno = request.form['materno']
            telefono = request.form['telefono']
            celular = request.form['celular']
            correo = request.form['correo']
            id_nivel = request.form['id_nivel']
            id_municipio = request.form['id_municipio']
            id_asunto = request.form['id_asunto']

            # Asignar turno por municipio
            ultimo_turno = db.session.query(func.max(SolicitudTurno.turno))\
                .filter_by(id_municipio=id_municipio).scalar()
            nuevo_turno = (ultimo_turno or 0) + 1

            # Crear y guardar solicitud
            nueva_solicitud = SolicitudTurno(
                nombre_tramite=nombre_tramite,
                curp=curp,
                nombre=nombre,
                paterno=paterno,
                materno=materno,
                telefono=telefono,
                celular=celular,
                correo=correo,
                id_nivel=id_nivel,
                id_municipio=id_municipio,
                id_asunto=id_asunto,
                turno=nuevo_turno
            )
            db.session.add(nueva_solicitud)
            db.session.commit()

            # Buscar solicitud ya con ID
            solicitud_guardada = SolicitudTurno.query.filter_by(curp=curp, turno=nuevo_turno).first()

            # Generar PDF con patrón Factory
            factory = TicketFactory(
                solicitud=solicitud_guardada,
                nivel=Nivel.query.get(id_nivel).nombre,
                municipio=Municipio.query.get(id_municipio).nombre,
                asunto=Asunto.query.get(id_asunto).nombre
            )

            pdf_path = factory.generar_pdf()
            return send_file(pdf_path, as_attachment=False)  # mostrar en navegador

        except Exception as e:
            print(f"❌ Error al procesar la solicitud: {e}")

    return render_template('solicitar.html', niveles=niveles, municipios=municipios, asuntos=asuntos)


@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        token = request.form.get('g-recaptcha-response')

        respuesta = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={'secret': current_app.config['RECAPTCHA_SECRET_KEY'], 'response': token}
        )
        resultado = respuesta.json()

        if not resultado.get('success'):
            error = 'Captcha inválido.'
        else:
            usuario = Usuario.query.filter_by(correo=correo, password=password).first()
            if usuario:
                session['usuario_id'] = usuario.id
                session['usuario_nombre'] = usuario.nombre
                return redirect(url_for('main.dashboard'))
            else:
                error = 'Correo o contraseña incorrectos.'

    site_key = current_app.config['RECAPTCHA_SITE_KEY']
    return render_template('login.html', error=error, site_key=site_key)

@main.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    municipio_id = request.args.get('municipio', type=int)
    municipios = Municipio.query.all()

    query = SolicitudTurno.query
    if municipio_id:
        query = query.filter_by(id_municipio=municipio_id)

    total_pendientes = query.filter_by(estatus='Pendiente').count()
    total_resueltos = query.filter_by(estatus='Resuelto').count()
    total_tickets = total_pendientes + total_resueltos

    labels = [m.nombre for m in municipios]
    pendientes = []
    resueltos = []

    for m in municipios:
        q = SolicitudTurno.query.filter_by(id_municipio=m.id)
        pendientes.append(q.filter_by(estatus='Pendiente').count())
        resueltos.append(q.filter_by(estatus='Resuelto').count())

    municipio_mas_saturado = "-"
    if municipios:
        municipio_mas_saturado = max(municipios, key=lambda m: SolicitudTurno.query.filter_by(id_municipio=m.id).count()).nombre

    # Resumen de fechas últimos 7 días
    hoy = datetime.today().date()
    una_semana_atras = hoy - timedelta(days=6)

    resumen_fechas = []
    for i in range(7):
        dia = una_semana_atras + timedelta(days=i)
        pendientes_dia = SolicitudTurno.query.filter(
            func.date(SolicitudTurno.fecha_registro) == dia,
            SolicitudTurno.estatus == 'Pendiente'
        ).count()
        resueltos_dia = SolicitudTurno.query.filter(
            func.date(SolicitudTurno.fecha_registro) == dia,
            SolicitudTurno.estatus == 'Resuelto'
        ).count()
        resumen_fechas.append({
            'fecha': dia.strftime('%Y-%m-%d'),
            'pendientes': pendientes_dia,
            'resueltos': resueltos_dia
        })

    return render_template(
        'dashboard.html',
        municipios=municipios,
        municipio_id=municipio_id,
        total_pendientes=total_pendientes,
        total_resueltos=total_resueltos,
        total_tickets=total_tickets,
        municipio_mas_saturado=municipio_mas_saturado,
        labels=labels,
        pendientes=pendientes,
        resueltos=resueltos,
        valores=[total_pendientes, total_resueltos],
        resumen_fechas=resumen_fechas
    )

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main.route('/admin/consultar', methods=['GET'])
def consultar_tickets():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    resultados = []
    buscar = request.args.get('buscar')
    if buscar:
        resultados = SolicitudTurno.query.filter(
            (SolicitudTurno.curp.like(f"%{buscar}%")) |
            (SolicitudTurno.nombre.like(f"%{buscar}%")) |
            (SolicitudTurno.paterno.like(f"%{buscar}%")) |
            (SolicitudTurno.materno.like(f"%{buscar}%"))
        ).all()

    return render_template('consultar.html', resultados=resultados)

@main.route('/admin/modificar/buscar', methods=['GET', 'POST'])
def buscar_ticket_modificar():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        curp = request.form['curp']
        turno = request.form['turno']
        ticket = SolicitudTurno.query.filter_by(curp=curp, turno=turno).first()

        if ticket:
            return redirect(url_for('main.modificar_ticket', ticket_id=ticket.id))
        else:
            return render_template('buscar_ticket.html', error='No se encontró el ticket.')

    return render_template('buscar_ticket.html')

@main.route('/admin/modificar/<int:ticket_id>', methods=['GET', 'POST'])
def modificar_ticket(ticket_id):
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    ticket = SolicitudTurno.query.get_or_404(ticket_id)
    niveles = Nivel.query.all()
    municipios = Municipio.query.all()
    asuntos = Asunto.query.all()

    if request.method == 'POST':
        # Actualizar campos
        ticket.nombre_tramite = request.form['nombre_tramite']
        ticket.nombre = request.form['nombre']
        ticket.paterno = request.form['paterno']
        ticket.materno = request.form['materno']
        ticket.telefono = request.form['telefono']
        ticket.celular = request.form['celular']
        ticket.correo = request.form['correo']
        ticket.id_nivel = request.form['id_nivel']
        ticket.id_municipio = request.form['id_municipio']
        ticket.id_asunto = request.form['id_asunto']

        db.session.commit()  # ✅ Guarda cambios

        # ✅ Generar PDF con Factory
        nivel_nombre = Nivel.query.get(ticket.id_nivel).nombre
        municipio_nombre = Municipio.query.get(ticket.id_municipio).nombre
        asunto_nombre = Asunto.query.get(ticket.id_asunto).nombre

        factory = TicketFactory(
            solicitud=ticket,
            nivel=nivel_nombre,
            municipio=municipio_nombre,
            asunto=asunto_nombre,
            actualizado=True
        )

        pdf_path = factory.generar_pdf()
        return send_file(pdf_path, as_attachment=True)

    return render_template('modificar_ticket.html', ticket=ticket, niveles=niveles, municipios=municipios, asuntos=asuntos)


@main.route('/admin/usuarios/agregar', methods=['GET', 'POST'])
def agregar_usuario():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    mensaje = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']

        existe = Usuario.query.filter_by(correo=correo).first()
        if existe:
            mensaje = 'Ese correo ya está registrado.'
        else:
            nuevo = Usuario(nombre=nombre, correo=correo, password=password)
            db.session.add(nuevo)
            db.session.commit()
            mensaje = 'Usuario agregado exitosamente.'

    return render_template('agregar_usuario.html', mensaje=mensaje)

@main.route('/admin/tickets')
def ver_tickets():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    tickets = SolicitudTurno.query.all()
    return render_template('ver_tickets.html', tickets=tickets)

@main.route('/admin/estatus/<int:ticket_id>')
def cambiar_estatus(ticket_id):
    ticket = SolicitudTurno.query.get_or_404(ticket_id)
    ticket.estatus = 'Resuelto' if ticket.estatus == 'Pendiente' else 'Pendiente'
    db.session.commit()
    return redirect(url_for('main.ver_tickets'))
    buscar = request.args.get('buscar', '')
    return redirect(url_for('main.consultar_tickets', buscar=buscar))

@main.route('/admin/eliminar/<int:ticket_id>')
def eliminar_ticket(ticket_id):
    ticket = SolicitudTurno.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    buscar = request.args.get('buscar', '')
    return redirect(url_for('main.consultar_tickets', buscar=buscar))

@main.route('/admin/pdf/<curp>')
def descargar_pdf(curp):
    nombre_archivo = f"{curp}_ticket.pdf"
    ruta = os.path.join('static', 'tickets', nombre_archivo)

    if os.path.exists(os.path.join(current_app.root_path, ruta)):
        return send_from_directory(directory=os.path.join(current_app.root_path, 'static', 'tickets'),
                                   path=nombre_archivo, as_attachment=False)
    else:
        flash("No se encontró el archivo PDF del ticket", "danger")
        return redirect(url_for('main.consultar_tickets'))
    
# API REST BÁSICA
@main.route('/api/tickets')
def api_tickets():
    tickets = SolicitudTurno.query.all()
    return jsonify([
        {
            'id': t.id,
            'curp': t.curp,
            'nombre': t.nombre,
            'turno': t.turno,
            'estatus': t.estatus,
            'municipio': Municipio.query.get(t.id_municipio).nombre if t.id_municipio else None
        } for t in tickets
    ])

@main.route('/ver-api')
def ver_api():
    return render_template('ver_api.html')

@main.route('/materias')
def listar_materias():
    materias = get_all_materias()
    return render_template('materias/lista.html', materias=materias)

@main.route('/buscar', methods=['GET', 'POST'])
def buscar_materia():
    resultado = None
    if request.method == 'POST':
        resultado = get_materia(request.form['cve_plan'], request.form['clave'])
    return render_template('materias/buscar.html', resultado=resultado)

@main.route('/crear', methods=['GET', 'POST'])
def crear_materia():
    if request.method == 'POST':
        data = {
            "clave": request.form['clave'],
            "nombre": request.form['nombre'],
            "creditos": request.form['creditos'],
            "cve_plan": request.form['cve_plan']
        }
        create_materia(data)
        return redirect(url_for('main.listar_materias'))
    return render_template('materias/crear.html')

@main.route('/editar', methods=['GET', 'POST'])
def editar_materia():
    resultado = None
    if request.method == 'POST':
        if 'buscar' in request.form:
            resultado = get_materia(request.form['cve_plan'], request.form['clave'])
        elif 'actualizar' in request.form:
            data = {
                "clave": request.form['clave'],
                "nombre": request.form['nombre'],
                "creditos": request.form['creditos'],
                "cve_plan": request.form['cve_plan']
            }
            update_materia(data)
            return redirect(url_for('main.listar_materias'))
    return render_template('materias/editar.html', resultado=resultado)

@main.route('/eliminar', methods=['GET', 'POST'])
def eliminar_materia():
    if request.method == 'POST':
        delete_materia(request.form['clave'])
        return redirect(url_for('main.listar_materias'))
    return render_template('materias/eliminar.html')