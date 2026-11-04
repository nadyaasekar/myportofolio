import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner_test",
            email="owner@example.com",
            password="test-password-123",
        )

        self.visitor = User.objects.create_user(
            username="visitor_test",
            password="test-password-123",
        )

        self.editor = User.objects.create_user(
            username="editor_test",
            password="test-password-123",
        )

        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(editor_group)

        self.experience = Experience.objects.create(
            title="Asisten Praktikum",
            description="Membantu pelaksanaan praktikum.",
            category="part-time",
        )

        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail",
            args=[self.experience.pk],
        )
        self.star_url = reverse(
            "api:experience-star",
            args=[self.experience.pk],
        )

        self.payload = {
            "title": "Pengalaman Baru",
            "description": "Deskripsi pengalaman baru.",
            "category": "volunteer",
            "thumbnail": "",
            "started_at": "2026-01-01",
            "ended_at": None,
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            str(self.experience.pk),
        )
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertNotIn("starred_by", response.data[0])
        self.assertNotIn("password", response.data[0])
        self.assertNotIn("email", response.data[0])

        detail = self.client.get(self.detail_url)

        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.data["title"], self.experience.title)

    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {"title": "ASISTEN"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            self.list_url,
            {"title": "tidak-ada"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        missing_url = reverse(
            "api:experience-detail",
            args=[uuid.uuid4()],
        )

        response = self.client.get(missing_url)

        self.assertEqual(response.status_code, 404)

    def test_guest_and_regular_user_cannot_write(self):
        for user in (None, self.visitor):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)

                response = self.client.post(
                    self.list_url,
                    self.payload,
                    format="json",
                )
                self.assertEqual(response.status_code, 403)

                response = self.client.patch(
                    self.detail_url,
                    {"title": "Tidak boleh berubah"},
                    format="json",
                )
                self.assertEqual(response.status_code, 403)

                response = self.client.delete(self.detail_url)
                self.assertEqual(response.status_code, 403)

        self.assertEqual(Experience.objects.count(), 1)

        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Praktikum")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Experience.objects.count(), 2)
        self.assertTrue(
            Experience.objects.filter(
                pk=response.data["id"],
                title=self.payload["title"],
            ).exists()
        )

    def test_invalid_input_is_rejected(self):
        self.client.force_authenticate(user=self.owner)

        invalid_inputs = [
            ({"title": "   "}, "title"),
            (
                {"title": '<img src="x" onerror="alert(1)">'},
                "title",
            ),
            (
                {"description": "<b></b>"},
                "description",
            ),
            (
                {"thumbnail": "javascript:alert(1)"},
                "thumbnail",
            ),
            (
                {"category": "kategori-tidak-valid"},
                "category",
            ),
            (
                {"started_at": "bukan-tanggal"},
                "started_at",
            ),
        ]

        for changes, field in invalid_inputs:
            with self.subTest(field=field, changes=changes):
                response = self.client.post(
                    self.list_url,
                    {**self.payload, **changes},
                    format="json",
                )

                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)

        self.assertEqual(Experience.objects.count(), 1)

    def test_owner_can_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"title": "Judul Diperbarui"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Judul Diperbarui")
        self.assertEqual(
            self.experience.description,
            "Membantu pelaksanaan praktikum.",
        )

        # PUT harus menyertakan semua field yang wajib.
        response = self.client.put(
            self.detail_url,
            {"title": "Data Tidak Lengkap"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, self.payload["title"])
        self.assertEqual(
            self.experience.description,
            self.payload["description"],
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(
            Experience.objects.filter(
                pk=self.experience.pk
            ).exists()
        )

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(
            self.detail_url,
            {"title": "Diedit oleh Editor"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Diedit oleh Editor")

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, 403)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertTrue(
            Experience.objects.filter(
                pk=self.experience.pk
            ).exists()
        )

    def test_staff_status_alone_does_not_allow_editing(self):
        self.visitor.is_staff = True
        self.visitor.save()

        self.client.force_authenticate(user=self.visitor)

        response = self.client.patch(
            self.detail_url,
            {"title": "Percobaan Staff"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Praktikum")

    def test_star_requires_login_and_toggles(self):
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.experience.starred_by.count(), 0)

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(
            self.experience.starred_by.filter(
                pk=self.visitor.pk
            ).exists()
        )

        # Status star harus sesuai akun yang sedang mengakses.
        self.client.force_authenticate(user=self.editor)
        detail = self.client.get(self.detail_url)

        self.assertEqual(detail.data["star_count"], 1)
        self.assertFalse(detail.data["is_starred"])

        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_computed_fields_cannot_be_forged(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 999,
                "is_starred": True,
                "starred_by_names": "fake-user",
                "starred_by": [self.visitor.pk],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.starred_by.count(), 0)

    def test_wrong_methods_are_rejected(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.list_url)
        self.assertEqual(response.status_code, 405)

        response = self.client.get(self.star_url)
        self.assertEqual(response.status_code, 405)

        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_session_post_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner_test",
                password="test-password-123",
            )
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_post_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner_test",
                password="test-password-123",
            )
        )

        # Browsable API merender form yang menghasilkan cookie CSRF.
        page = client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        self.assertEqual(page.status_code, 200)
        self.assertIn("csrftoken", client.cookies)

        token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Experience.objects.count(), 2)