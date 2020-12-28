from django.contrib import admin
from.models import Post,BlogComment

# Register your models here.
@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','author','desc',]

# @admin.register(BlogComment)
# class BlogCommentModelAdmin(admin.ModelAdmin):
#     list_display= ['sno','post','parent','comment','user',]
admin.site.register(BlogComment)