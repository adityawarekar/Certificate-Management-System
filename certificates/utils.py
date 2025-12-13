import io, os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from django.conf import settings
import qrcode
from reportlab.lib.utils import ImageReader
from datetime import date
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


FONT_DIR = os.path.join(settings.BASE_DIR, "static", "fonts")

pdfmetrics.registerFont(
    TTFont("GreatVibes", os.path.join(FONT_DIR, "GreatVibes-Regular.ttf"))
)

pdfmetrics.registerFont(
    TTFont("PlayfairBold", os.path.join(FONT_DIR, "PlayfairDisplay-Bold.ttf"))
)



def generate_certificate_pdf(participant, verify_url=None, background_image_path=None):

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

   
    if background_image_path and os.path.exists(background_image_path):
        bg = ImageReader(background_image_path)
        c.drawImage(bg, 0, 0, width=width, height=height)

   
    c.setFont("GreatVibes", 44)   
    c.setFillColorRGB(0, 0, 0)

    c.drawCentredString(
        width / 2,
        8.5 * cm,    
        participant.full_name
    )

   

    if verify_url:
        qr = qrcode.make(verify_url)

        qr_buffer = io.BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        qr_image = ImageReader(qr_buffer)

        
        c.drawImage(
            qr_image,
            2 * cm,          
            2.8 * cm,        
            width=3.5 * cm,
            height=3.5 * cm,
            mask="auto"
        )

       
        c.setFont("PlayfairBold", 10)
        c.setFillColorRGB(0.2, 0.2, 0.2)

        c.drawString(
            2 * cm,
            2.1 * cm,
            "Issued on: 10 December 2025"
        )


   
    signature_path = os.path.join(settings.BASE_DIR, "static", "images", "signature.png")

    if os.path.exists(signature_path):
        sig = ImageReader(signature_path)

        c.drawImage(
            sig,
            width - 7 * cm,
            3.5 * cm,
            width=5 * cm,
            height=2 * cm,
            mask="auto"
        )

        c.setFont("PlayfairBold", 11)
        c.drawString(width - 7 * cm, 3.1 * cm, "Rhea Malhotra")

        c.setFont("Helvetica", 10)
        c.drawString(width - 7 * cm, 2.6 * cm, "Hackathon Chairperson")

    
    c.showPage()
    c.save()
    buffer.seek(0)

    return buffer
