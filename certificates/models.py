from django.db import models
import uuid

class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    college = models.CharField(max_length=200, blank=True)
    hackathon_name = models.CharField(max_length=200, blank=True)
    date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=100, blank=True)
    Participant_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verify_token = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"    

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="certificates")
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to="certificates_pdf/", blank=True, null=True)

    def __str__(self):
        return f"Certificate for {self.Participant.full_name} at {self.issued_at.date()}"
