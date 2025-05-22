
from django.contrib import admin
from django.urls import re_path, include


urlpatterns = [
    re_path(r'^admin/shell/', include('django_admin_shell.urls')),
    re_path(r'^admin/', admin.site.urls),
]
