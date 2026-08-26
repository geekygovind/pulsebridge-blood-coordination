from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from myapp import views as patient_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', patient_views.home, name='landing'),
    path('patient/', include('myapp.urls')),
    path('blood-bank/', include('blood_bank.urls')),
    path('hospital/', include('hospital.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
