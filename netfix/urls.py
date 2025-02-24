from django.contrib import admin
from django.urls import include, path
# from django.conf.urls.static import static

import services.views
from . import views

urlpatterns = [
    path("", include("main.urls")),
    path("services/", include("services.urls")),
    path("register/", include("users.urls")),
    path("customer/<slug:name>", views.customer_profile, name="customer_profile"),
    path("company/<slug:name>", views.company_profile, name="company_profile"),
    path("most_requested/", services.views.most_requested_services, name="most_requested_services"),
    path("admin/", admin.site.urls),
]

# ======================================================================================
# Django doesnt automatically runs static files when settings.DEBUG = False,
# so we need to add this here:
# if not settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# and this one to settings.py:
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# and then run this:
# python manage.py collectstatic
# so the new automatically created staticfiles folder will contain all our static files
# ======================================================================================

# ==>> ignore all above if "py manage.py runserver --insecure" is used
