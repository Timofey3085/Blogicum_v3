from django.contrib import admin

from .models import Post, Category, Location, Comment

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class PostAdmin(admin.ModelAdmin):
    empty_value_display = 'Не задано'

    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,)


class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'post'
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
