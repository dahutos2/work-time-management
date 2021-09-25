from django.contrib import admin

# Register your models here.
from . import models
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilter

class WorktimeInline(admin.TabularInline):
    model = models.Worktime
    fields = ('date', 'start_time','end_time')
    extra = 0

@admin.register(models.User)
class UserAdmin(UserAdmin):
    inlines = [WorktimeInline]
    fieldsets =(
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'full_name', 'is_staff')
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(models.Worktime)
class WorktimeAdmin(admin.ModelAdmin):
    list_select_related = ('name',)
    list_display = ('id','start_time','end_time','date','name')
    list_display_links = ('id',)
    ordering = ('-date',)
    list_filter = (('date', DateRangeFilter),'name__full_name')
    
