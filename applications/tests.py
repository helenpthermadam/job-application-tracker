from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import JobApplication


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("helen", password="pass12345!")
        self.other = User.objects.create_user("other", password="pass12345!")
        self.app = JobApplication.objects.create(
            user=self.user, company="Acme", role="Python Developer"
        )
        self.client.login(username="helen", password="pass12345!")


class ModelTests(BaseTestCase):
    def test_str(self):
        self.assertEqual(str(self.app), "Python Developer at Acme")

    def test_default_status_is_saved(self):
        self.assertEqual(self.app.status, JobApplication.Status.SAVED)

    def test_follow_up_overdue_when_past_and_open(self):
        self.app.follow_up_date = timezone.localdate() - timedelta(days=2)
        self.assertTrue(self.app.follow_up_overdue)

    def test_follow_up_not_overdue_when_rejected(self):
        self.app.follow_up_date = timezone.localdate() - timedelta(days=2)
        self.app.status = JobApplication.Status.REJECTED
        self.assertFalse(self.app.follow_up_overdue)


class AuthTests(TestCase):
    def test_list_requires_login(self):
        response = self.client.get(reverse("application_list"))
        self.assertRedirects(response, reverse("login"))

    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "Str0ng-pass-123",
                "password2": "Str0ng-pass-123",
            },
        )
        self.assertRedirects(response, reverse("application_list"))
        self.assertTrue(User.objects.filter(username="newuser").exists())


class CrudTests(BaseTestCase):
    def test_create_sets_logged_in_user(self):
        self.client.post(
            reverse("application_create"),
            {"company": "Globex", "role": "Django Developer", "status": "applied"},
        )
        created = JobApplication.objects.get(company="Globex")
        self.assertEqual(created.user, self.user)

    def test_update(self):
        self.client.post(
            reverse("application_update", args=[self.app.pk]),
            {"company": "Acme", "role": "Senior Dev", "status": "interview"},
        )
        self.app.refresh_from_db()
        self.assertEqual(self.app.role, "Senior Dev")
        self.assertEqual(self.app.status, "interview")

    def test_delete(self):
        self.client.post(reverse("application_delete", args=[self.app.pk]))
        self.assertFalse(JobApplication.objects.filter(pk=self.app.pk).exists())


class PrivacyTests(BaseTestCase):
    def test_cannot_view_or_edit_or_delete_other_users_application(self):
        theirs = JobApplication.objects.create(
            user=self.other, company="Secret", role="Hidden"
        )
        for name in ("application_detail", "application_update", "application_delete"):
            response = self.client.get(reverse(name, args=[theirs.pk]))
            self.assertEqual(response.status_code, 404, name)

    def test_list_shows_only_own_applications(self):
        JobApplication.objects.create(user=self.other, company="Secret", role="Hidden")
        response = self.client.get(reverse("application_list"))
        self.assertContains(response, "Python Developer")
        self.assertNotContains(response, "Hidden")


class SearchFilterTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        JobApplication.objects.create(
            user=self.user, company="Globex", role="Django Dev", status="interview"
        )

    def test_search_by_company(self):
        response = self.client.get(reverse("application_list"), {"q": "globex"})
        self.assertContains(response, "Django Dev")
        self.assertNotContains(response, "Python Developer")

    def test_filter_by_status(self):
        response = self.client.get(reverse("application_list"), {"status": "interview"})
        self.assertContains(response, "Django Dev")
        self.assertNotContains(response, "Python Developer")

    def test_dashboard_counts(self):
        response = self.client.get(reverse("application_list"))
        counts = {c["value"]: c["count"] for c in response.context["status_cards"]}
        self.assertEqual(counts["saved"], 1)
        self.assertEqual(counts["interview"], 1)
        self.assertEqual(counts["offer"], 0)
