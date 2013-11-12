from django.contrib import admin
from Archives.models import Guide, MeetingMinutes, HouseRule, Bylaws

# Register your models here.
admin.site.register(Guide)
admin.site.register(MeetingMinutes)
admin.site.register(HouseRule)
admin.site.register(Bylaws)