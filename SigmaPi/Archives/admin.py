from django.contrib import admin
from Archives.models import Guide, MeetingMinutes, HouseRules, Bylaws

# I'm commenting this stuff out because it doesn't do anything necessary,
# and is mildly confusing. Will remove later if nothing breaks.
# class GuideAdmin(admin.ModelAdmin):
	# prepopulated_fields = {"path": ("name",)}
# admin.site.register(Guide, GuideAdmin)

# Register models to appear in the Django Admin DB Site
admin.site.register(Guide)
admin.site.register(MeetingMinutes)
admin.site.register(HouseRules)
admin.site.register(Bylaws)
