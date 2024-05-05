from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'important', ]

        # Комментарии к полям формы
        help_texts = {
            'title': '<br> '
                     '<br> Стилизация текста  <b>ОБЯЗАТЕЛЬНО УБИРАЕМ</b> - внутри <> <br>'
                     ' <-br-> - Переход на новую строку <br>'
                     '<-b->Жирный текст<-/b-> <br>'
                     '<-i->Курсивный текст<-/i-> <br>'
                     '<-u->Подчеркнутый текст<-/u->',
            'content': "<br><br> <b style='color:red'>Если ваш ранг тармана ниже, чем Палач, не ставьте галочку , <br>"
                       "так как данный пост не будет доступен для вас.</b>"
        }

        # Пользовательский метод, который добавляет классы к полям формы
        def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)
            self.fields['title'].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Введите заголовок', 'type': 'text'})
            self.fields['content'].widget.attrs.update({'class': 'form-control', 'id': 'exampleFormControlTextarea1'})
            self.fields['important'].widget.attrs.update({'class': 'form-check-input'})


class CustomUserCreationForm(UserCreationForm):
    # Изменяем help_text для поля username
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        help_text="Имя пользователя должно содержать не более 150 символов и может содержать только буквы, цифры, и символы @/./+/-/_."
    )

    # Изменяем help_text для поля password1
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="<br><br>Ваш пароль должен соответствовать следующим требованиям:<br> \
                      - Не должен совпадать с вашими другими личными данными.<br> \
                      - Содержать не менее 8 символов.<br> \
                      - Не быть часто используемым паролем.<br> \
                      - Не содержать только цифры."
    )

    # Изменяем help_text для поля password2
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput,
        help_text="Пожалуйста, введите тот же пароль, что и выше, для подтверждения."
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    # Translate label to russian
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Имя пользователя"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Пароль еще раз"


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
