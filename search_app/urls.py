from django.urls import path
from . import views

app_name = 'search_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/search/', views.search, name='search'),
    path('api/graph-nodes/', views.get_graph_nodes, name='get_graph_nodes'),
    path('api/results/', views.get_results, name='get_results'),
]
