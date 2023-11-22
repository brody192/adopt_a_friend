from django.contrib import admin
from .models import Users, Profile, Preference
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea 

class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('-email', )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    fieldsets = (
        ('Personal Information',
            {
                'fields':('email',
                          'first_name',
                          'last_name',
                          'age',
                          'date_of_birth',
                          'home_address',
                          'contact_num',
                          'slug'
                          )
            }
         ),
         ('About',
          {
              'fields':(
                  'user_bio',
              )
          }
         ),
         ('Permissions',
          {
              'fields':(
                  'is_staff',
                  'is_active',
                  'is_superuser',
              )
          }
         )
    )
    prepopulated_fields = {"slug": ("first_name","last_name")}  # new

admin.site.register(Users, UserAdminConfig)
admin.site.register(Profile)
admin.site.register(Preference)
