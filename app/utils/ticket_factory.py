import os
import qrcode
from fpdf import FPDF

class TicketFactory:
    def __init__(self, solicitud, nivel, municipio, asunto, actualizado=False):
        self.solicitud = solicitud
        self.nivel = nivel
        self.municipio = municipio
        self.asunto = asunto
        self.actualizado = actualizado

        self.folder = os.path.abspath(os.path.join("app", "static", "tickets"))
        os.makedirs(self.folder, exist_ok=True)

    def generar_qr(self):
        qr_path = os.path.join(self.folder, f"{self.solicitud.curp}_qr.png")
        qr = qrcode.make(self.solicitud.curp)
        qr.save(qr_path)
        return qr_path

    def generar_pdf(self):
        pdf_path = os.path.join(self.folder, f"{self.solicitud.curp}_ticket.pdf")
        qr_path = self.generar_qr()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        titulo = "TICKET DE TURNO - ACTUALIZADO" if self.actualizado else "TICKET DE TURNO"
        pdf.cell(200, 10, txt=titulo, ln=True, align="C")
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Nombre del trámite: {self.solicitud.nombre_tramite}", ln=True)
        pdf.cell(200, 10, txt=f"CURP: {self.solicitud.curp}", ln=True)
        pdf.cell(200, 10, txt=f"Nombre completo: {self.solicitud.nombre} {self.solicitud.paterno} {self.solicitud.materno}", ln=True)
        pdf.cell(200, 10, txt=f"Teléfono: {self.solicitud.telefono}", ln=True)
        pdf.cell(200, 10, txt=f"Celular: {self.solicitud.celular}", ln=True)
        pdf.cell(200, 10, txt=f"Correo: {self.solicitud.correo}", ln=True)
        pdf.cell(200, 10, txt=f"Nivel: {self.nivel}", ln=True)
        pdf.cell(200, 10, txt=f"Municipio: {self.municipio}", ln=True)
        pdf.cell(200, 10, txt=f"Asunto: {self.asunto}", ln=True)
        pdf.cell(200, 10, txt=f"Número de turno: {self.solicitud.turno}", ln=True)
        pdf.image(qr_path, x=80, y=pdf.get_y() + 10, w=50)

        pdf.output(pdf_path)
        return pdf_path
