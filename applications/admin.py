from django.contrib import admin

from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "status", "date_applied", "follow_up_date", "user")
    list_filter = ("status", "date_applied", "user")
    search_fields = ("company", "role", "location", "notes")
    date_hierarchy = "date_applied"
