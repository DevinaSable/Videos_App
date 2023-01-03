from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Document')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/videos/', include('vitube.urls'), name='video-list'),
    path('accounts/', include('users.urls')),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('silk/', include('silk.urls', namespace='silk')),
    path('doc/', schema_view),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


