from django import forms
from main.models import Experience

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at", 
            "ended_at",
        ]
        labels = {
            "title": "Judul Pengalaman",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "URL Gambar/Thumbnail",
            "started_at": "Bulan & Tahun Mulai",
            "ended_at": "Bulan & Tahun Selesai (Kosongkan jika masih berlangsung)",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Contoh: Asisten Dosen PBP", "class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Jelaskan peran dan pencapaianmu...", "rows": 3, "class": "form-control"}
            ),
            "category": forms.Select(
                attrs={"class": "form-control"}
            ),
            "thumbnail": forms.URLInput(
                attrs={"placeholder": "https://example.com/image.jpg", "class": "form-control"}
            ),
            "started_at": forms.DateTimeInput(
                attrs={"type": "date", "class": "form-control"}
                        ),
            "ended_at": forms.DateTimeInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }