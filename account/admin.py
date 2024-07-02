from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patient, Doctor

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('User Type', {'fields': ('is_patient', 'is_doctor')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_patient', 'is_doctor'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_patient', 'is_doctor')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_patient', 'is_doctor')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'state', 'pincode')
    search_fields = ('user__username', 'user__email', 'address_line1', 'city', 'state', 'pincode')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'state', 'pincode')
    search_fields = ('user__username', 'user__email', 'address_line1', 'city', 'state', 'pincode')
