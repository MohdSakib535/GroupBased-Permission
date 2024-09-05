from django.contrib import admin
from .models import customUser,Transaction

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ("username","role")

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    display_groups.short_description = 'Groups'


admin.site.register(customUser, MemberAdmin)
admin.site.register(Transaction)
