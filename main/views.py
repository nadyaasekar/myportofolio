# Create your views here.
from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "NADYA SEKAR",
        "npm": "2506607133",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS Student with dream big ahead. Love to watch and talk about movies or old songs."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Nadya Sekar",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)