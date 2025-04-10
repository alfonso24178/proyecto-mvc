document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const nombreTramite = form.nombre_tramite.value.trim();
        const curp = form.curp.value.trim();
        const nombre = form.nombre.value.trim();
        const paterno = form.paterno.value.trim();
        const materno = form.materno.value.trim();
        const telefono = form.telefono.value.trim();
        const celular = form.celular.value.trim();
        const correo = form.correo.value.trim();
        const idNivel = form.id_nivel.value;
        const idMunicipio = form.id_municipio.value;
        const idAsunto = form.id_asunto.value;

        const soloLetrasRegex = /^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+$/;
        const curpRegex = /^[A-ZÑ&]{4}\d{6}[HM][A-Z]{5}[A-Z\d]{2}$/i;
        const phoneRegex = /^\d{10}$/;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        // Validaciones obligatorias con formato

        if (!nombreTramite || !soloLetrasRegex.test(nombreTramite)) {
            return Swal.fire('Error', 'Debe ingresar el nombre completo del trámite con solo letras.', 'error');
        }

        if (!curp || !curpRegex.test(curp)) {
            return Swal.fire('Error', 'Debe ingresar una CURP válida.', 'error');
        }

        if (!nombre || !soloLetrasRegex.test(nombre)) {
            return Swal.fire('Error', 'El campo Nombre es obligatorio y debe contener solo letras.', 'error');
        }

        if (!paterno || !soloLetrasRegex.test(paterno)) {
            return Swal.fire('Error', 'El campo Paterno es obligatorio y debe contener solo letras.', 'error');
        }

        if (!materno || !soloLetrasRegex.test(materno)) {
            return Swal.fire('Error', 'El campo Materno es obligatorio y debe contener solo letras.', 'error');
        }

        if (!telefono || !phoneRegex.test(telefono)) {
            return Swal.fire('Error', 'El campo Teléfono es obligatorio y debe tener 10 dígitos.', 'error');
        }

        if (!celular || !phoneRegex.test(celular)) {
            return Swal.fire('Error', 'El campo Celular es obligatorio y debe tener 10 dígitos.', 'error');
        }

        if (!correo || !emailRegex.test(correo)) {
            return Swal.fire('Error', 'Debe ingresar un correo electrónico válido.', 'error');
        }

        if (!idNivel) {
            return Swal.fire('Error', 'Debe seleccionar un Nivel.', 'error');
        }
        if (!idMunicipio) {
            return Swal.fire('Error', 'Debe seleccionar un Municipio.', 'error');
        }
        if (!idAsunto) {
            return Swal.fire('Error', 'Debe seleccionar un Asunto.', 'error');
        }

        // Si todo es válido, enviamos el formulario
        form.submit();
    });
});
