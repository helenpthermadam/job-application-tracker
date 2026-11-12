from django.urls import path

from . import views

urlpatterns = [
    path("", views.application_list, name="application_list"),
    path("applications/new/", views.ApplicationCreateView.as_view(), name="application_create"),
    path("applications/<int:pk>/", views.ApplicationDetailView.as_view(), name="application_detail"),
    path("applications/<int:pk>/edit/", views.ApplicationUpdateView.as_view(), name="application_update"),
    path("applications/<int:pk>/delete/", views.ApplicationDeleteView.as_view(), name="application_delete"),
    path("signup/", views.signup, name="signup"),
]
