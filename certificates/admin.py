from django.contrib import admin
from .models import Participant, Certificate
from django.urls import path
from django.shortcuts import redirect, render
from django.contrib import messages
import csv, io


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "hackathon_name", "date", "custom_participant_id")
    search_fields = ("full_name", "email", "participant_id")
    change_list_template = "admin/participants_change_list.html"

    def custom_participant_id(self, obj):
        return obj.participant_id
    custom_participant_id.short_description = "Participant ID"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("upload-csv/", self.admin_site.admin_view(self.upload_csv), name="participants-upload-csv"),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get("csv_file")
            if not csv_file:
                messages.error(request, "Please choose a CSV file.")
                return redirect("..")
            try:
                decoded = csv_file.read().decode("utf-8")
                io_string = io.StringIO(decoded)
                reader = csv.DictReader(io_string)
                created = 0
                for row in reader:
                    Participant.objects.create(
                        full_name=row.get("full_name") or row.get("name"),
                        email=row.get("email"),
                        college=row.get("college", ""),
                        hackathon_name=row.get("hackathon_name", ""),
                        participant_id=row.get("participant_id", ""),
                    )
                    created += 1
                messages.success(request, f"Created {created} participants.")
            except Exception as e:
                messages.error(request, f"Error: {e}")
            return redirect("..")

        return render(request, "admin/upload_csv.html", {})


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("participant_name", "issued_at")

    def participant_name(self, obj):
        return obj.participant.full_name

    participant_name.short_description = "Participant"
