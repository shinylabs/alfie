from django.contrib import admin
from alfie.apps.profiles.models import Profile

class ProfileAdmin(admin.ModelAdmin):
	save_on_top = True
	list_display = ('menu', 'ship_zip_code', 'created')

admin.site.register(Profile, ProfileAdmin)