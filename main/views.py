# Create your views here.
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ExperienceForm
from django.conf import settings

from main.models import Experience, Education


def show_main(request):
    context = {
        "name": "NADYA SEKAR",
        "npm": "2506607133",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS Student with big dreams ahead. Love to watch and talk about movies or old songs."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experience_json(request)
    
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "NADYA SEKAR",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)


def show_education(request):
    context = {
        "name": "NADYA SEKAR",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)

def create_experience(request):
    if request.method == "POST":
        secret_key = request.POST.get("secret_key")
        if secret_key != settings.PORTFOLIO_SECRET_KEY:
            messages.error(request, "Kode rahasia salah! Data gagal ditambahkan.")
            return redirect('main:show_main')
        
        form = ExperienceForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "New Experience Has Been Added!")
            return redirect("main:show_experience")
    else:
        form = ExperienceForm()
        
    context = {
        "name": "NADYA SEKAR",
        "form": form,
    }
    return render(request, "experience_form.html", context)

# API JSON 
def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
    
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def delete_experience(request, experience_id):
    if request.method == "POST":
        secret_key = request.POST.get("secret_key")

        if secret_key != settings.PORTFOLIO_SECRET_KEY:
            messages.error(request, "Kode rahasia salah! Data gagal dihapus.")
            return redirect('main:show_experience')

        experience = get_object_or_404(Experience, pk=experience_id)
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")