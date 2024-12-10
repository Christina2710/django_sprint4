from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blog.models import Category, Comment, Post
from .forms import CommentForm, PostForm, UserForm
from .utils import get_published_posts

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10
    # Определяем набор данных, который будет использоваться
    queryset = get_published_posts(
        # Добавляем в каждый объект подсчитанное поле
        # comment_count, равное числу комментариев, связанных с постом.
        model.objects.annotate(comment_count=Count('comments'))
        .select_related('category', 'location')
    )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self):
        post = get_object_or_404(
            self.model.objects.select_related('category', 'location'),
            id=self.kwargs['post_id'],
        )
        # Проверяем, является ли текущий пользователь автором поста.
        if self.request.user == post.author:
            return post
        # Если пользователь не автор, возвращаем опубликованную версию поста.
        return get_object_or_404(
            get_published_posts(
                self.model.objects.select_related('category', 'location')),
            id=self.kwargs['post_id'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все комментарии, относящиеся к конкретному посту.
        comments = self.object.comments.select_related('author')
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        context['comments'] = comments
        return context


class CategoryPostsView(ListView):
    template_name = 'blog/category.html'
    paginate_by = 10
    context_object_name = 'post_list'

    def get_queryset(self):
        category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True)
        # Получаем список опубликованных постов, относящихся
        # к заданной категории.
        post_list = get_published_posts(
            Post.objects.select_related('category', 'location')
        ).filter(category=category)
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем информацию о категории в контекст шаблона.
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )
        return context


class ProfileView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        # Получаем объект профиля пользователя
        profile = get_object_or_404(
            self.model,
            username=self.kwargs['username'],
        )
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.annotate(
            # Считаем количество комментариев для каждого поста
            comment_count=Count('comments')
        ).select_related('category', 'location').filter(
            author__username=self.kwargs['username']
        )
        # Создаём объект пагинатора с количеством 10 записей на страницу.
        paginator = Paginator(posts, 10)
        # Получаем из запроса значение параметра page.
        page_number = self.request.GET.get('page')
        # Получаем запрошенную страницу пагинатора.
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self):
        # Возвращаем объект текущего пользователя
        return self.request.user

    def get_success_url(self):
        # Указываем, куда перенаправить пользователя
        # после успешного обновления профиля.
        return reverse('blog:profile', kwargs={'username': self.request.user})


class ProfileRedirectMixin(LoginRequiredMixin):
    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class AuthorRequiredMixin(LoginRequiredMixin):
    def get_queryset(self):
        # Пользователь может работать только со своими постами.
        return self.model.objects.filter(author=self.request.user)


class PostCreateView(ProfileRedirectMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        # Устанавливаем текущего пользователя как автора поста.
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(AuthorRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, является ли пользователь автором поста.
        post = get_object_or_404(self.model, id=self.kwargs['post_id'])
        # Если пользователь не автор, перенаправляем его на страницу поста.
        if post.author != request.user:
            return redirect(reverse(
                'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})
            )
        # Если пользователь является автором, выполняем стандартный dispatch.
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(ProfileRedirectMixin, AuthorRequiredMixin, DeleteView):
    form_class = PostForm
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(instance=self.object)
        # Добавляем форму в контекст для отображения в шаблоне.
        context['form'] = form
        return context


class PostRedirectMixin:
    def get_success_url(self):
        # Перенаправление на пост с якорем для комментариев.
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        ) + '#comments'


class CommentCreateView(LoginRequiredMixin, PostRedirectMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        # Устанавливаем текущего пользователя как автора комментария
        # и привязываем его к посту.
        form.instance.author = self.request.user
        post = get_object_or_404(
            Post.objects.select_related('category', 'location'),
            id=self.kwargs['post_id'],
        )
        form.instance.post = post
        return super().form_valid(form)


class CommentMixin(LoginRequiredMixin, PostRedirectMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        # Пользователь может работать только со своими комментариями.
        return self.model.objects.filter(author=self.request.user)


class CommentUpdateView(CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentMixin, PostRedirectMixin, DeleteView):
    pass
