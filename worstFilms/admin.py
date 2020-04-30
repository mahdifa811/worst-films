from django.contrib import admin 
from .models import Film, Comment, Like

@admin.register(Film)
class filmAdmin(admin.ModelAdmin):

    list_display = ('title' , 'director' , 'release_year')
    list_filter = ('published_date',)
    search_fields = ('title' , 'dirctor', 'review')

admin.site.register(Comment)
admin.site.register(Like)


    
    



