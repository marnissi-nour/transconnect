from django.contrib.auth.mixins import UserPassesTestMixin


ADMIN_ROLE = "administrateur"


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = ()

    def test_func(self):
        if not self.request.user.is_authenticated:
            return True
        return (
            self.request.user.role in self.allowed_roles
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        return super().handle_no_permission()


def is_admin(user):
    return user.is_authenticated and user.role == ADMIN_ROLE


def user_entreprise(user):
    return getattr(user, "entreprise", None)
