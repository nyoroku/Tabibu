from django.contrib import admin

from models import Latest, Writer, Category, Team


class LatestAdmin(admin.ModelAdmin):
    list_filter = ('title', 'created')
    list_display = ('title', 'story', 'slug', 'photo')
    search_fields = ('created', 'title')
    date_hierarchy = 'created'
    ordering = ('created',)
admin.site.register(Latest, LatestAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('title', 'date_added')
    list_display = ('title', 'date_added')
    search_fields = ('title', 'date_added')
    date_hierarchy = 'date_added'
    ordering = ('date_added',)
admin.site.register(Category, CategoryAdmin)

class WriterAdmin(admin.ModelAdmin):
    list_filter = ('name', 'date_added')
    list_display = ('name', )
    search_fields = ('date_added', 'name')
    date_hierarchy = 'date_added'
    ordering = ('date_added',)
admin.site.register(Writer, WriterAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_filter = ('name', 'added')
    list_display = ('name', 'job', 'photo')
    search_fields = ('added', 'name')
    date_hierarchy = 'added'
    ordering = ('added',)
admin.site.register(Team, TeamAdmin)






