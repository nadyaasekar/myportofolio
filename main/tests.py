# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.test import Client

from main.models import Experience, Education


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="experience-grid"')
        self.assertContains(
            response,
            reverse("api:experience-list"),
        )
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"',
        )

        # Data kartu diperoleh melalui API, bukan HTML awal.
        api_response = self.client.get(
            reverse("api:experience-list")
        )

        self.assertEqual(api_response.status_code, 200)

        data = api_response.json()
        self.assertEqual(len(data), 1)

        experience = data[0]
        self.assertEqual(
            experience["id"],
            str(self.experience.pk),
        )
        self.assertEqual(
            experience["title"],
            self.experience.title,
        )
        self.assertEqual(
            experience["description"],
            self.experience.description,
        )
        self.assertEqual(
            experience["category_display"],
            "Part-Time",
        )
        self.assertTrue(experience["is_ongoing"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()

        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="experience-empty"')

        api_response = self.client.get(
            reverse("api:experience-list")
        )

        self.assertEqual(api_response.status_code, 200)
        self.assertEqual(api_response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now().date()
        self.experience.save()
        self.experience.refresh_from_db()

        self.assertFalse(self.experience.is_ongoing)

        response = self.client.get(
            reverse(
                "api:experience-detail",
                args=[self.experience.pk],
            )
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertFalse(data["is_ongoing"])
        self.assertEqual(
            data["ended_at"],
            self.experience.ended_at.isoformat(),
        )

class EducationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_education_url_and_template(self):
        response = self.client.get(reverse('main:show_education'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education.html')

    def test_education_empty_condition(self):
        Education.objects.all().delete()

        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="education-empty"')

        api_response = self.client.get(
            reverse("main:get_education_json")
        )

        self.assertEqual(api_response.status_code, 200)
        self.assertEqual(api_response.json(), [])

    def test_education_data_rendered(self):
        education = Education.objects.create(
            degree="S1 Ilmu Komputer",
            institution="Universitas Indonesia",
            start_year=2025,
            end_year="Sekarang",
        )

        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="education-grid"')
        self.assertContains(
            response,
            reverse("main:get_education_json"),
        )

        api_response = self.client.get(
            reverse("main:get_education_json")
        )

        self.assertEqual(api_response.status_code, 200)

        data = api_response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["pk"], str(education.pk))

        fields = data[0]["fields"]
        self.assertEqual(fields["degree"], education.degree)
        self.assertEqual(
            fields["institution"],
            education.institution,
        )
        self.assertEqual(fields["start_year"], 2025)
        self.assertEqual(fields["end_year"], "Sekarang")