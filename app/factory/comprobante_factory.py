from abc import ABC, abstractmethod

class ComprobanteFactory(ABC):
    @abstractmethod
    def generar_comprobante(self, datos):
        pass


class PDFComprobante(ComprobanteFactory):
    def generar_comprobante(self, datos):
        from fpdf import FPDF
        import qrcode
        import os

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Comprobante de Turno", ln=True, align='C')
        pdf.ln(10)

        for campo, valor in datos.items():
            pdf.cell(200, 10, txt=f"{campo}: {valor}", ln=True, align='L')
        
        # Crear el QR con la CURP
        qr = qrcode.make(datos['CURP'])
        qr_path = os.path.join("app", "static", "qr_temp.png")
        qr.save(qr_path)

        pdf.image(qr_path, x=160, y=30, w=40, h=40)

        output_path = os.path.join("app", "static", "tickets", f"{datos['CURP']}.pdf")
        pdf.output(output_path)

        return output_path
