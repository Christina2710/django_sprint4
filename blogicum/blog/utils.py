from django.utils.timezone import now


# Фильтрует набор данных для получения опубликованных постов.
def get_published_posts(queryset):
    post_list = queryset.filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True
    )
    return post_list
