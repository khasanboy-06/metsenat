from django.urls import path
from .views import (SponsorAPIView, StudentCreateAPIView, StudentDetailAPIView,
                SponsorDetailAPIView, SponsorListAPIView, StudentListAPIView,
                StudentSponsorListAPIView, StudentSponsorCreateAPIView,
                StudentSponsorUpdateAPIView, StudentSponsorDestroyAPIView,
                UserInfoView, DashboardStatisticAPIView, DashboardGraphAPIView
                )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('api/v1/user', UserInfoView.as_view()),

    path("api/v1/sponsor/create", SponsorAPIView.as_view()),
    path("api/v1/sponsor/detail/<int:pk>/", SponsorDetailAPIView.as_view()),
    path("api/v1/sponsor/list", SponsorListAPIView.as_view()),

    path("api/v1/student/list", StudentListAPIView.as_view()),
    path("api/v1/student/create", StudentCreateAPIView.as_view()),
    path("api/v1/student/detail/<int:pk>/", StudentDetailAPIView.as_view()),

    path("api/v1/student-sponsor/list", StudentSponsorListAPIView.as_view()),
    path("api/v1/student-sponsor/create", StudentSponsorCreateAPIView.as_view()),
    path("api/v1/student-sponsor/update/<int:pk>", StudentSponsorUpdateAPIView.as_view()),
    path("api/v1/student-sponsor/destroy/<int:pk>", StudentSponsorDestroyAPIView.as_view()),

    path("api/v1/dashboard-statistic", DashboardStatisticAPIView.as_view()),
    path('api/v1/dashboard-graph/', DashboardGraphAPIView.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]