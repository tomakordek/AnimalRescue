from django.forms import ModelForm
from .models import ToDo
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm




class ToDoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ['Miasto', 'Lokalizacja', 'Kontakt', 'Kategoria', 'Zdjęcie', 'Opis']

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None
            self.fields['username'].help_text = "Podaj nazwę użytkownika"
            self.fields['password1'].help_text = "Wpisz hasło"
            self.fields['password2'].help_text = "Powtórz hasło"
