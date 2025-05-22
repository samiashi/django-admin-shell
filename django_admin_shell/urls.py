from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from .views import ShellView

app_name = 'django_admin_shell'

urlpatterns = [
    re_path(r'^$', staff_member_required(ShellView.as_view()), name="shell"),
]
