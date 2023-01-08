from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User, UserMessage

# Register your models here.


class CRMUserAdmin(UserAdmin):
    fieldsets = tuple(
        [x for x in UserAdmin.fieldsets] + [(
            _("Other"), {"fields": (
                "role",
                "phone",
                "lessons",
                "manager",
                "salary",
                "percent_salary",
            )}
        )]
    )


admin.site.register(User, CRMUserAdmin)
admin.site.register(UserMessage)
