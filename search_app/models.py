from django.db import models


class SearchResult(models.Model):
    SEARCH_TYPES = [
        ('bfs', 'Búsqueda en Amplitud (BFS)'),
        ('dfs', 'Búsqueda en Profundidad (DFS)'),
        ('ucs', 'Búsqueda con Costo Uniforme (UCS)'),
    ]
    
    search_type = models.CharField(max_length=3, choices=SEARCH_TYPES)
    initial_state = models.TextField()
    target_state = models.TextField()
    result_path = models.TextField()
    total_cost = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_search_type_display()} - {self.initial_state} -> {self.target_state}"
