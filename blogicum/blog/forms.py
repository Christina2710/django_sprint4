from django import forms
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


# Форма для создания и редактирования поста
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Исключаем поля из формы
        exclude = ('is_published', 'created_at', 'author')
        # Указываем виджет для выбора даты и времени
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


# Форма для создания и редактирования комментария
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Поле для редактирования текста комментария
        fields = ('text',)


# Форма для редактирования данных пользователя
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # Поля для редактирования пользовательских данных
        fields = ('first_name', 'last_name', 'username', 'email')
