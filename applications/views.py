from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import JobApplicationForm, SignUpForm
from .models import JobApplication


def signup(request):
    """Register a new user and log them in."""
    if request.user.is_authenticated:
        return redirect("application_list")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("application_list")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


class UserOwnedMixin(LoginRequiredMixin):
    """Only ever return the logged-in user's own applications."""

    model = JobApplication

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)


def application_list(request):
    """Dashboard: status counts, search, status filter and pagination."""
    if not request.user.is_authenticated:
        return redirect("login")

    applications = JobApplication.objects.filter(user=request.user)

    # Dashboard counts per status, in one query.
    counts = {
        row["status"]: row["total"]
        for row in applications.values("status").annotate(total=Count("id"))
    }
    status_cards = [
        {"value": value, "label": label, "count": counts.get(value, 0)}
        for value, label in JobApplication.Status.choices
    ]

    # Search and filter from the query string (?q=...&status=...).
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    if query:
        applications = applications.filter(
            Q(company__icontains=query)
            | Q(role__icontains=query)
            | Q(location__icontains=query)
        )
    if status in JobApplication.Status.values:
        applications = applications.filter(status=status)

    page = Paginator(applications, 10).get_page(request.GET.get("page"))

    context = {
        "page": page,
        "status_cards": status_cards,
        "total": sum(counts.values()),
        "query": query,
        "current_status": status,
        "statuses": JobApplication.Status.choices,
    }
    return render(request, "applications/application_list.html", context)


class ApplicationDetailView(UserOwnedMixin, DetailView):
    template_name = "applications/application_detail.html"


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = "applications/application_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Application added.")
        return super().form_valid(form)


class ApplicationUpdateView(UserOwnedMixin, UpdateView):
    form_class = JobApplicationForm
    template_name = "applications/application_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Application updated.")
        return super().form_valid(form)


class ApplicationDeleteView(UserOwnedMixin, DeleteView):
    template_name = "applications/application_confirm_delete.html"
    success_url = reverse_lazy("application_list")

    def form_valid(self, form):
        messages.success(self.request, "Application deleted.")
        return super().form_valid(form)
