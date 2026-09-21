# Create your views here.
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ExperienceForm, EducationForm
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied        

from main.models import Experience, Education


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "NADYA SEKAR",
        "npm": "2506607133",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS Student with big dreams ahead. Love to watch and talk about movies or old songs."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

# SHOW
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
    search_query = request.GET.get("q", "").strip()

    json_response = get_education_json(request)
    education_list = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [item.object for item in education_list]

    context = {
        "name": "NADYA SEKAR",
        "education_list": education_list,
        "search_query": search_query,
    }
    return render(request, "education.html", context)


# CREATE
@login_required(login_url="/login/") 
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

@login_required(login_url="/login/") 
def create_education(request):
    if request.method == "POST":
        secret_key = request.POST.get("secret_key")
        if secret_key != settings.PORTFOLIO_SECRET_KEY:
            messages.error(request, "Kode rahasia salah! Data gagal ditambahkan.")
            return redirect('main:show_main')
        
        form = EducationForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "New Education Has Been Added!")
            return redirect("main:show_education")
    else:
        form = EducationForm()
        
    context = {
        "name": "NADYA SEKAR",
        "form": form,
    }
    return render(request, "education_form.html", context)



# API JSON 
def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
    
    experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    return HttpResponse(experiences_json, content_type="application/json")

def get_education_json(request):
    search_query = request.GET.get("q", "").strip()
    education_qs = Education.objects.all()
    if search_query:
        education_qs = education_qs.filter(
            Q(institution__icontains=search_query) | Q(degree__icontains=search_query)
        )

    education_json = serializers.serialize("json", education_qs, use_natural_foreign_keys=True)
    return HttpResponse(education_json, content_type="application/json")
 
# DELETE
@login_required(login_url="/login/") 
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

@login_required(login_url="/login/") 
def delete_education(request, education_id):
    if request.method == "POST":
        secret_key = request.POST.get("secret_key")

        if secret_key != settings.PORTFOLIO_SECRET_KEY:
            messages.error(request, "Kode rahasia salah! Data gagal dihapus.")
            return redirect('main:show_education')

        education = get_object_or_404(Education, pk=education_id)
        education.delete()
        messages.success(request, "Education berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")


# UPDATE
@login_required(login_url="/login/") 
def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
 
    if request.method == "POST":
        secret_key = request.POST.get("secret_key")
        if secret_key != settings.PORTFOLIO_SECRET_KEY:
            messages.error(request, "Kode rahasia salah! Data gagal diperbarui.")
            return redirect("main:show_experience")
 
        form = ExperienceForm(request.POST, instance=experience)
 
        if form.is_valid():
            form.save()
            messages.success(request, "Experience berhasil diperbarui!")
            return redirect("main:show_experience")
    else:
        form = ExperienceForm(instance=experience)
 
    context = {
        "name": "NADYA SEKAR",
        "form": form,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/") 
def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
 
    if request.method == "POST":
        secret_key = request.POST.get("secret_key")
        if secret_key != settings.PORTFOLIO_SECRET_KEY:
            messages.error(request, "Kode rahasia salah! Data gagal diperbarui.")
            return redirect("main:show_education")
 
        form = EducationForm(request.POST, instance=education)
 
        if form.is_valid():
            form.save()
            messages.success(request, "Education berhasil diperbarui!")
            return redirect("main:show_education")
    else:
        form = EducationForm(instance=education)
 
    context = {
        "name": "NADYA SEKAR",
        "form": form,
        "education": education,
    }
    return render(request, "education_form.html", context)


# AUTHENTICATION
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "NADYA SEKAR",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "NADYA SEKAR",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


# STAR
@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")


@login_required(login_url="/login/")
def toggle_star_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)

    return redirect("main:show_education")