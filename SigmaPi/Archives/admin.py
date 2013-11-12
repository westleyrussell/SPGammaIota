from django.contrib import admin
from Archives.models import Guide, MeetingMinutes, HouseRule, Bylaws

#Admin model for guides
class GuideAdmin(admin.ModelAdmin):
	prepopulated_fields = {"path": ("name",)}

#Admin model for rules
class HouseRuleAdmin(admin.ModelAdmin):
	prepopulated_fields = {"path": ("title",)}

admin.site.register(Guide, GuideAdmin)
admin.site.register(MeetingMinutes)
admin.site.register(HouseRule, HouseRuleAdmin)
admin.site.register(Bylaws)