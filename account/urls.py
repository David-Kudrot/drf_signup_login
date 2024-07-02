from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet, RegisterAPIView, LoginView, PatientDashboardView, DoctorDashboardView, LogoutView

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('patient-dashboard/', PatientDashboardView.as_view(), name='patient-dashboard'),
    path('doctor-dashboard/', DoctorDashboardView.as_view(), name='doctor-dashboard'),
]








