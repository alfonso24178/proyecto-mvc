from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.models import Nivel, Municipio, Asunto

catalagos = Blueprint('catalagos', __name__)


# ---------- CRUD NIVELES ----------
@catalagos.route('/admin/niveles')
def niveles():
    niveles = Nivel.query.all()
    return render_template('catalagos/niveles.html', niveles=niveles)

@catalagos.route('/admin/niveles/agregar', methods=['POST'])
def agregar_nivel():
    nombre = request.form['nombre']
    nuevo = Nivel(nombre=nombre)
    db.session.add(nuevo)
    db.session.commit()
    flash('Nivel agregado con éxito', 'success')
    return redirect(url_for('catalagos.niveles'))

@catalagos.route('/admin/niveles/editar/<int:id>', methods=['POST'])
def editar_nivel(id):
    nivel = Nivel.query.get_or_404(id)
    nivel.nombre = request.form['nombre']
    db.session.commit()
    flash('Nivel actualizado con éxito', 'success')
    return redirect(url_for('catalagos.niveles'))

@catalagos.route('/admin/niveles/eliminar/<int:id>')
def eliminar_nivel(id):
    nivel = Nivel.query.get_or_404(id)
    db.session.delete(nivel)
    db.session.commit()
    flash('Nivel eliminado con éxito', 'success')
    return redirect(url_for('catalagos.niveles'))

# ---------- CRUD MUNICIPIOS ----------
@catalagos.route('/admin/municipios')
def municipios():
    municipios = Municipio.query.all()
    return render_template('catalagos/municipios.html', municipios=municipios)

@catalagos.route('/admin/municipios/agregar', methods=['POST'])
def agregar_municipio():
    nombre = request.form['nombre']
    nuevo = Municipio(nombre=nombre)
    db.session.add(nuevo)
    db.session.commit()
    flash('Municipio agregado con éxito', 'success')
    return redirect(url_for('catalagos.municipios'))

@catalagos.route('/admin/municipios/editar/<int:id>', methods=['POST'])
def editar_municipio(id):
    municipio = Municipio.query.get_or_404(id)
    municipio.nombre = request.form['nombre']
    db.session.commit()
    flash('Municipio actualizado con éxito', 'success')
    return redirect(url_for('catalagos.municipios'))

@catalagos.route('/admin/municipios/eliminar/<int:id>')
def eliminar_municipio(id):
    municipio = Municipio.query.get_or_404(id)
    db.session.delete(municipio)
    db.session.commit()
    flash('Municipio eliminado con éxito', 'success')
    return redirect(url_for('catalagos.municipios'))

# ---------- CRUD ASUNTOS ----------
@catalagos.route('/admin/asuntos')
def asuntos():
    asuntos = Asunto.query.all()
    return render_template('catalagos/asuntos.html', asuntos=asuntos)

@catalagos.route('/admin/asuntos/agregar', methods=['POST'])
def agregar_asunto():
    nombre = request.form['nombre']
    nuevo = Asunto(nombre=nombre)
    db.session.add(nuevo)
    db.session.commit()
    flash('Asunto agregado con éxito', 'success')
    return redirect(url_for('catalagos.asuntos'))

@catalagos.route('/admin/asuntos/editar/<int:id>', methods=['POST'])
def editar_asunto(id):
    asunto = Asunto.query.get_or_404(id)
    asunto.nombre = request.form['nombre']
    db.session.commit()
    flash('Asunto actualizado con éxito', 'success')
    return redirect(url_for('catalagos.asuntos'))

@catalagos.route('/admin/asuntos/eliminar/<int:id>')
def eliminar_asunto(id):
    asunto = Asunto.query.get_or_404(id)
    db.session.delete(asunto)
    db.session.commit()
    flash('Asunto eliminado con éxito', 'success')
    return redirect(url_for('catalagos.asuntos'))
