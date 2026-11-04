from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    message = "Anda tidak memiliki izin untuk melakukan tindakan ini."

    def has_permission(self, request, view):
        # Semua pengunjung boleh membaca.
        if request.method in SAFE_METHODS:
            return True

        # Tindakan selain membaca membutuhkan akun.
        if not request.user.is_authenticated:
            return False

        # Superuser boleh menambah, mengubah, dan menghapus.
        if request.user.is_superuser:
            return True

        # Editor hanya boleh mengubah.
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )