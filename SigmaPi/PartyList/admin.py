from django.contrib import admin
from PartyList.models import Party, Guest, PartyGuest

# Admin site for blog posts
class PartyAdmin(admin.ModelAdmin):
	prepopulated_fields = {"path": ("name",)}

# Register your models here.
admin.site.register(Party)
admin.site.register(Guest)
admin.site.register(PartyGuest)