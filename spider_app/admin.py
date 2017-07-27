from django.contrib import admin

# Register your models here.
from spider_app.models import EntryPoint, Project

admin.site.disable_action('delete_selected')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'status')
    ordering = ('-id',)
    search_fields = ('name',)


@admin.register(EntryPoint)
class EntryPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'url', 'created_at', 'last_exec_time', 'status')
    ordering = ('-id',)
    search_fields = ('name',)
    list_filter = ('project__name',)
