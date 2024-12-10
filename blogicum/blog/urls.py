from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Главная страница
    path('', views.PostListView.as_view(), name='index'),
    # Страница конкретного поста
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    # Посты по категориям
    path('category/<slug:category_slug>/',
         views.CategoryPostsView.as_view(),
         name='category_posts'
         ),
    # Редактирование профиля
    path('profile/edit/',
         views.ProfileUpdateView.as_view(), name='edit_profile'
         ),
    # Профиль пользователя
    path('profile/<username>/',
         views.ProfileView.as_view(),
         name='profile'
         ),
    # Создание нового поста
    path('posts/create/',
         views.PostCreateView.as_view(),
         name='create_post'
         ),
    # Редактирование поста
    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'
         ),
    # Удаление поста
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'
         ),
    # Добавление комментария
    path('posts/<int:post_id>/comment/',
         views.CommentCreateView.as_view(),
         name='add_comment'
         ),
    # Редактирование комментария
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'
         ),
    # Удаление комментария
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'
         ),
]
