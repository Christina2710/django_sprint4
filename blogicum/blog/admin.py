from django.contrib import admin
from .models import Post, Category, Location


# Вместо пустого значения в админке будет отображена строка "Не задано".
admin.site.empty_value_display = 'Не задано'


# Модель Post для вставки на страницу других моделей.
class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    # Добавляем вставку на страницу управления объектом модели Category:
    inlines = (
        PostInline,
    )


class LocationAdmin(admin.ModelAdmin):
    # Добавляем вставку на страницу управления объектом модели Location:
    inlines = (
        PostInline,
    )


class PostAdmin(admin.ModelAdmin):
    # Поля, которые будут показаны на странице списка объектов.
    list_display = (
        'title',
        'text',
        'is_published',
        'author',
        'category',
        'location',
        'created_at',
        'pub_date',
    )
    # Поля, которые можно редактировать прямо на странице списка объектов.
    list_editable = (
        'is_published',
        'category',
    )
    # Кортеж с перечнем полей, по которым будет проводиться поиск.
    search_fields = ('title',)
    # Кортеж с полями, по которым можно фильтровать записи.
    list_filter = ('category',)
    # Поля, при клике на которые можно перейти на страницу
    # просмотра и редактирования записи.
    list_display_links = ('title',)


# Регистрируем кастомное представление админ-зоны для модели Post:
admin.site.register(Post, PostAdmin)
# Регистрируем кастомное представление админ-зоны для модели Category:
admin.site.register(Category, CategoryAdmin)
# Регистрируем кастомное представление админ-зоны для модели Location:
admin.site.register(Location, LocationAdmin)
