from django import forms
from django.contrib.auth.forms import UsernameField


class LoginForm(forms.Form):
    """ Base class for authenticating users. Extend this to get a form that accepts
    username/password logins. """
    username = UsernameField(
        label='Логин',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Логин')
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Повторите пароль')
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'type': 'email', 'class': 'form-control',
                                                     'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp',
                                                     'placeholder': 'Введите Логин'})

        self.fields['password'].widget.attrs.update({'type': 'password', 'class': 'form-control',
                                                     'id': 'exampleInputPassword1', 'placeholder': 'Пароль'})

        self.fields['password2'].widget.attrs.update({'type': 'password', 'class': 'form-control',
                                                      'id': 'exampleInputPassword1', 'placeholder': 'Повторите пароль'})

        self.fields['email'].widget.attrs.update({'type': 'email', 'class': 'form-control',
                                                  'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp',
                                                  'placeholder': 'Введите Email'})

        self.fields['first_name'].widget.attrs.update({'type': 'email', 'class': 'form-control',
                                                       'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp',
                                                       'placeholder': 'Введите Имя'})

        self.fields['last_name'].widget.attrs.update({'type': 'email', 'class': 'form-control',
                                                      'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp',
                                                      'placeholder': 'Введите Фамилию'})


class EnterForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def __init__(self, *args, **kwargs):
        super(EnterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'type': 'email', 'class': 'form-control',
                                                     'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp',
                                                     'placeholder': 'Введите Логин'})

        self.fields['password'].widget.attrs.update({'type': 'password', 'class': 'form-control',
                                                     'id': 'exampleInputPassword1', 'placeholder': 'Пароль'})
