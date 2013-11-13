from django.contrib import admin
from PubSite.models import BlogPost
# Admin site for blog posts
class BlogPostAdmin(admin.ModelAdmin):
	prepopulated_fields = {"path": ("title",)}

admin.site.register(BlogPost, BlogPostAdmin)
