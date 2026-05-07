from django.contrib import admin
from .models import SearchResult


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ('search_type', 'initial_state', 'target_state', 'created_at')
    list_filter = ('search_type', 'created_at')
    search_fields = ('initial_state', 'target_state')
