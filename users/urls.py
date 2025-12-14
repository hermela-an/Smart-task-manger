from django.urls import path
from .views import signup
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # User signup
    path('signup/', signup, name='signup'),

    # JWT login → returns access & refresh tokens
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # JWT refresh → get a new access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]