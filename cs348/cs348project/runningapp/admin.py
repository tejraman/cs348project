from django.contrib import admin
from .models import User, Run, BikeRide, Swim

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
   list_display = ('username', 'email', 'date_joined')

@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
   list_display = ('user', 'date', 'distance_miles', 'time_minutes')
   search_fields = ('user__username',)

@admin.register(BikeRide)
class BikeRideAdmin(admin.ModelAdmin):
   list_display = ('user', 'date', 'distance_miles', 'time_minutes')
   search_fields = ('user__username',)

@admin.register(Swim)
class SwimAdmin(admin.ModelAdmin):
   list_display = ('user', 'date', 'distance_meters', 'time_minutes')
   search_fields = ('user__username',)

   