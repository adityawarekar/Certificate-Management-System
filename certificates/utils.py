import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from django.conf import settings
import qrcode
from reportlab.lib.utils import ImageReader
import os

def generate_certificate_pdf(participant, verify_url=None, background_image_path=None):
    """
    Generate a certificate PDF in memory and return bytes IO.
    - participant: Participant model instance
    - verify_url: optional verification URL to put on the certificate
    - background_image_path: optional path to background template image (png/jpg)
    """
    buffer = io.BytesIO()
    
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

  
    if background_image_path and os.path.exists(background_image_path):
        bg = ImageReader(background_image_path)
        c.drawImage(bg, 0, 0, width=width, height=height)

  
    name_text = participant.full_name
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2, height * 0.55, name_text)

 
    c.setFont("Helvetica", 20)
    hack_text = f"For participating in: {participant.hackathon_name or 'Hackathon'}"
    c.drawCentredString(width / 2, height * 0.45, hack_text)

    if participant.date:
        date_text = f"Date: {participant.date}"
        c.setFont("Helvetica", 14)
        c.drawCentredString(width / 2, height * 0.40, date_text)

    
    if participant.position:
        c.setFont("Helvetica-Oblique", 16)
        c.drawCentredString(width / 2, height * 0.35, f"Position: {participant.position}")

    
    c.setFont("Helvetica", 10)
    if verify_url:
        c.drawString(2 * cm, 2 * cm, f"Verify: {verify_url}")

      
        qr = qrcode.QRCode(box_size=3, border=2)
        qr.add_data(verify_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = io.BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        qr_reader = ImageReader(qr_buffer)
        c.drawImage(qr_reader, 2 * cm, 3 * cm, width=4*cm, height=4*cm)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
