from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# Importujemy widok listujący miasta z aplikacji trips
from trips import views as trips_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trips/', include('trips.urls')),
    path('api/cities/', trips_views.list_cities, name='list_cities'),
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
