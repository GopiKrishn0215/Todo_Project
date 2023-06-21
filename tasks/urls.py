from django.urls import path
from .views import index,Todo, DataView, save_data_in_session, fetch_saved_data_from_session, get_user_id
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",index),
    path("todo/",Todo.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('data/', DataView.as_view(), name='data'),
    path('save/',save_data_in_session),
    path('fetch/',fetch_saved_data_from_session),
    path('getid/',get_user_id)
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)