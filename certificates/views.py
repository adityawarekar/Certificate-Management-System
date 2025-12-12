from django.shortcuts import render, get_object_or_404, redirect
from .forms import LookupForm
from .models import Participant, Certificate
from django.http import HttpResponse
from django.urls import reverse
from .utils import generate_certificate_pdf
from django.core.files.base import ContentFile
import os


def home(request):
    return render(request, "certificates/home.html")


def lookup_participant(request):
    form = LookupForm(request.GET or None)
    participant = None
    if form.is_valid() and any(form.cleaned_data.values()):
        qs = Participant.objects.all()
        if form.cleaned_data.get("email"):
            qs = qs.filter(email__iexact=form.cleaned_data["email"])
        if form.cleaned_data.get("participant_id"):
            qs = qs.filter(participant_id__iexact=form.cleaned_data["participant_id"])
        if form.cleaned_data.get("full_name"):
            qs = qs.filter(full_name__icontains=form.cleaned_data["full_name"])
        participant = qs.first()
    return render(request, "certificates/lookup.html", {"form": form, "participant": participant})


def download_certificate(request, participant_id):
   
    participant = get_object_or_404(Participant, id=participant_id)
   
    verify_url = request.build_absolute_uri(reverse("certificates:verify_certificate", args=[participant.verify_token]))

    

    from django.conf import settings
    bg_path = None
    possible_bg = os.path.join(settings.BASE_DIR, "static", "images", "certificate_bg.png")
    print("BG PATH:", possible_bg)
    print("EXISTS?:", os.path.exists(possible_bg))

    
    if os.path.exists(possible_bg):
        bg_path = possible_bg

    pdf_buffer = generate_certificate_pdf(participant, verify_url=verify_url, background_image_path=bg_path)

    
    cert_obj = Certificate.objects.create(participant=participant)
    cert_obj.pdf_file.save(f"certificate_{participant.id}.pdf", ContentFile(pdf_buffer.getvalue()))
    cert_obj.save()


    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    filename = f"certificate_{participant.full_name.replace(' ', '_')}.pdf"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def verify_certificate(request, token):
   
    participant = get_object_or_404(Participant, verify_token=token)

    certs = participant.certificates.all()
    return render(request, "certificates/verify.html", {"participant": participant, "certs": certs})
