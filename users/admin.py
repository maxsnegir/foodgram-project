from django.contrib import admin

from users.models import User, Follow

admin.site.register(Follow)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links = ('id', 'username', 'email')
    search_fields = ('username', 'email')
