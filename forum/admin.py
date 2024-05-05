from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
