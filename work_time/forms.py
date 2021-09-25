from django.contrib.auth.forms import UserCreationForm
from .models import User, Worktime
from django import forms

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","full_name","password1", "password2")

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.save()
        return user

class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Worktime
        fields = ('start_time', 'end_time', 'description')
        widgets = {
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return end_time

class SearchForm(forms.Form):
    startdate = forms.DateInput()
    enddate = forms.DateInput()
    
