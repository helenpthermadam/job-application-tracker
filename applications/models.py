from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class JobApplication(models.Model):
    """One job the user has saved or applied to."""

    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    # Every application belongs to exactly one user (so users only see their own data).
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    company = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    job_url = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    salary = models.CharField(max_length=60, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SAVED
    )
    date_applied = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.role} at {self.company}"

    def get_absolute_url(self):
        return reverse("application_detail", args=[self.pk])

    @property
    def follow_up_overdue(self):
        """True if a follow-up date has passed and the application is still open."""
        open_statuses = {self.Status.SAVED, self.Status.APPLIED, self.Status.INTERVIEW}
        return (
            self.follow_up_date is not None
            and self.follow_up_date < timezone.localdate()
            and self.status in open_statuses
        )
