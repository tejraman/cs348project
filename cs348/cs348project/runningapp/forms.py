from django import forms
from .models import User, Run, BikeRide, Swim, ProgressReport
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ['date', 'distance_miles', 'time_minutes']

class BikeRideForm(forms.ModelForm):
    class Meta:
        model = BikeRide
        fields = ['date', 'distance_miles', 'time_minutes']

class SwimForm(forms.ModelForm):
    class Meta:
        model = Swim
        fields = ['date', 'distance_meters', 'time_minutes']

class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        fields = ['title', 'note']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        