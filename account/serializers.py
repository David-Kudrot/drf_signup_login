from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, Doctor
from .models import User  # Adjust import path as per your project structure




class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=['patient', 'doctor'], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'profile_picture', 'first_name', 'last_name', 'email', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user_type = validated_data.pop('user_type')
        is_patient = user_type == 'patient'
        is_doctor = user_type == 'doctor'

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            profile_picture=validated_data.get('profile_picture'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            is_patient=is_patient,
            is_doctor=is_doctor
        )
        return user






class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['user', 'address_line1', 'city', 'state', 'pincode']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(validated_data=user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'address_line1', 'city', 'state', 'pincode']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(validated_data=user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor
