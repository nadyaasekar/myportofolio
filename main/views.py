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
from django.views.decorators.http import require_POST    
from django.http import HttpResponseNotAllowed  
from django.http import JsonResponse 

from main.models import Experience, Education

def is_editor(user):
    return (
        user.is_authenticated
        and user.groups.filter(name="Editor").exists()
    )

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
    context = {
        "name": "NADYA SEKAR",
        "title_query": request.GET.get("title", "").strip(),
        "is_editor": is_editor(request.user),
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "NADYA SEKAR",
        "search_query":  request.GET.get("q", "").strip(),
        "is_editor": is_editor(request.user),
        "form": EducationForm(),
    }
    return render(request, "education.html", context)


# CREATE
@login_required(login_url="/login/") 
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
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
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
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
    experiences = Experience.objects.prefetch_related(
        "starred_by"
    ).all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []

    for experience in experiences:
        starred_users = list(experience.starred_by.all())

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category_display": experience.get_category_display(),
                "thumbnail": experience.thumbnail or "",
                "started_at": experience.started_at,
                "ended_at": experience.ended_at,
                "is_ongoing": experience.is_ongoing,
                "star_count": len(starred_users),
                "is_starred": (
                    request.user.is_authenticated
                    and any(
                        user.pk == request.user.pk
                        for user in starred_users
                    )
                ),
            },
        })

    return JsonResponse(data, safe=False)

def get_education_json(request):
    search_query = request.GET.get("q", "").strip()
    educations = Education.objects.prefetch_related(
        "starred_by"
    ).order_by("-start_year", "institution", "id")

    if search_query:
        education_qs = education_qs.filter(
            Q(institution__icontains=search_query) | Q(degree__icontains=search_query)
        )

    data = []

    for education in educations:
        starred_users = list(education.starred_by.all())

        data.append({
            "pk": str(education.pk),
            "fields": {
                "institution": education.institution,
                "degree": education.degree,
                "start_year": education.start_year,
                "end_year": education.end_year,
                "star_count": len(starred_users),
                "is_starred": (
                    request.user.is_authenticated
                    and any(
                        user.pk == request.user.pk
                        for user in starred_users
                    )
                ),
            },
        })

    return JsonResponse(data, safe=False)
 
# DELETE
@login_required(login_url="/login/") 
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()
    messages.success(request, "Experience berhasil dihapus!")
    return redirect("main:show_experience")

@login_required(login_url="/login/") 
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method != "POST":
            return HttpResponseNotAllowed(["POST"])
    
    education = get_object_or_404(Education, pk=education_id)
    education.delete()
    messages.success(request, "Education berhasil dihapus!")
    return redirect("main:show_education")


# UPDATE
@login_required(login_url="/login/") 
def update_experience(request, experience_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
 
    if request.method == "POST":
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
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
    
    education = get_object_or_404(Education, pk=education_id)
 
    if request.method == "POST":
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
@require_POST
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    return redirect("main:show_experience")


@login_required(login_url="/login/")
@require_POST
def toggle_star_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)

    return redirect("main:show_education")


# AJAX
@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang dapat "
                    "menambahkan Experience."
                )
            },
            status=403,
        )

    form = ExperienceForm(request.POST)

    if form.is_valid():
        experience = form.save()

        return JsonResponse(
            {
                "message": "Experience berhasil ditambahkan.",
                "pk": str(experience.id),
            },
            status=201,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )

@require_POST
def create_education_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang dapat "
                    "menambahkan Education."
                )
            },
            status=403,
        )

    form = EducationForm(request.POST)

    if form.is_valid():
        education = form.save()

        return JsonResponse(
            {
                "message": "Education berhasil ditambahkan.",
                "pk": str(education.pk),
            },
            status=201,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )