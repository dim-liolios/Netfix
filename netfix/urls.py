from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", include("main.urls")),
    path("services/", include("services.urls")),
    path("register/", include("users.urls")),
    path("customer/<slug:name>", views.customer_profile, name="customer_profile"),
    path("company/<slug:name>", views.company_profile, name="company_profile"),
    path("admin/", admin.site.urls),
]

# Django doesnt automatically runs static files when settings.DEBUG = False,
# so we need to add this here:
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# and this one to settings.py:
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# and then run this:
# python manage.py collectstatic
# so the new automatically created staticfiles folder will contain all our static files
