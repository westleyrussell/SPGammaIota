from django.contrib import admin
from Archives.models import Guide, MeetingMinutes, HouseRules, Bylaws

#Admin model for guides
class GuideAdmin(admin.ModelAdmin):
	prepopulated_fields = {"path": ("name",)}

admin.site.register(Guide, GuideAdmin)
admin.site.register(MeetingMinutes)
admin.site.register(HouseRules)
admin.site.register(Bylaws)