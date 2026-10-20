
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("jobs/", views.jobs, name="jobs"),
    path("vip-members/", views.vip_members, name="vip_members"),
    path("become-vip/", views.become_vip, name="become_vip"),
    path("contact/", views.contact, name="contact"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
