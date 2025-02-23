"""netfix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

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
