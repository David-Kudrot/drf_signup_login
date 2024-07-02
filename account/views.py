from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Patient, Doctor
from .serializers import PatientSerializer, DoctorSerializer, UserSerializer

from django.contrib.auth.mixins import LoginRequiredMixin


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # if user.is_patient:
            #     return redirect('/patient-dashboard/')
            # elif user.is_doctor:
            #     return redirect('/doctor-dashboard/')
            # else:
            #     return Response({"message": "Logged in"}, status=200)
            return Response({"message": "Logged in"}, status=200)
        return Response({"error": "Invalid credentials"}, status=400)







class PatientDashboardView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        patient = Patient.objects.get(user=request.user)
        data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'profile_picture': request.user.profile_picture.url if request.user.profile_picture else None,
            'username': request.user.username,
            'email': request.user.email,
            'address_line1': patient.address_line1,
            'city': patient.city,
            'state': patient.state,
            'pincode': patient.pincode,
        }
        return Response(data)

class DoctorDashboardView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        doctor = Doctor.objects.get(user=request.user)
        data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'profile_picture': request.user.profile_picture.url if request.user.profile_picture else None,
            'username': request.user.username,
            'email': request.user.email,
            'address_line1': doctor.address_line1,
            'city': doctor.city,
            'state': doctor.state,
            'pincode': doctor.pincode,
        }
        return Response(data)



class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
