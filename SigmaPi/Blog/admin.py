from django.contrib import admin
from Blog.models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
	"""
		Have a separate blog post admin to 
		prepopulate the path field based on the title
	"""
	prepopulated_fields = {"path": ("title",)}

#admin.site.register(BlogPost, BlogPostAdmin)
