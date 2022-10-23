from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('home-view')), name='redirect-to-admin-panel'),
    path('admin-panel/', include('admin_panel.urls')),
    path('tgbot/', include('tgbot.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
