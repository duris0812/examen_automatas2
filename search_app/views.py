from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .searches import buscar_solucion_BFS, buscar_solucion_DFS, buscar_solucion_UCS, obtener_ruta
from .models import SearchResult


# Grafos de ejemplo
GRAFOS = {
    'ciudades': {
        'Jiloyork': ['Celaya', 'CDMX', 'Queretaro'],
        'Sonora': ['Zacatecas', 'Sinaloa'],
        'Guanajuato': ['Aguascalientes'],
        'Oaxaca': ['Queretaro', 'Tamaulipas'],
        'Sinaloa': ['Celaya', 'Sonora', 'Jiloyork'],
        'Queretaro': ['Monterrey'],
        'Celaya': ['Jiloyork', 'Sinaloa'],
        'Zacatecas': ['Sonora', 'Monterrey', 'Queretaro'],
        'Monterrey': ['Zacatecas', 'Sinaloa'],
        'Tamaulipas': ['Queretaro', 'CDMX', 'Aguascalientes', 'Guanajuato'],
        'CDMX': ['Tamaulipas', 'Zacatecas', 'Sinaloa', 'Jiloyork', 'Oaxaca'],
        'Aguascalientes': ['Guanajuato', 'Tamaulipas', 'Oaxaca', 'Zacatecas'],
    },
    'ciudades_costos': {
        'Jiloyork': {'CDMX': 125, 'Queretaro': 513},
        'Morelos': {'Queretaro': 524},
        'CDMX': {'Jiloyork': 125, 'Queretaro': 433, 'Hidalgo': 491},
        'Hidalgo': {'CDMX': 491, 'Queretaro': 356, 'Mexicali': 309, 'Monterrey': 346},
        'Queretaro': {'San Luis Potosi': 203, 'Morelos': 514, 'Jiloyork': 513, 'CDMX': 423, 'Monterrey': 603, 'Sonora': 437, 'Hidalgo': 356, 'Mexicali': 313, 'Aguascalientes': 599},
        'San Luis Potosi': {'Aguascalientes': 390, 'Queretaro': 203},
        'Aguascalientes': {'Queretaro': 599, 'San Luis Potosi': 390},
        'Sonora': {'Queretaro': 437, 'Mexicali': 394},
        'Mexicali': {'Monterrey': 296, 'Queretaro': 313, 'Hidalgo': 309, 'Sonora': 394},
        'Monterrey': {'Mexicali': 296, 'Queretaro': 603, 'Hidalgo': 346}
    }
}


def index(request):
    """Página principal con el formulario"""
    return render(request, 'search_app/index.html')


def _calcular_costo_total(grafo, ruta):
    costo_total = 0
    for origen, destino in zip(ruta, ruta[1:]):
        costo_total += grafo[origen][destino]
    return costo_total


@csrf_exempt
@require_http_methods(["POST"])
def search(request):
    """Ejecuta BFS, DFS y UCS con la misma ciudad origen y destino"""
    try:
        data = json.loads(request.body)
        initial_state = data.get('initial_state')
        target_state = data.get('target_state')
        
        if not all([initial_state, target_state]):
            return JsonResponse({
                'success': False,
                'error': 'Faltan parámetros requeridos'
            })

        try:
            grafo = GRAFOS['ciudades_costos']

            algoritmos = [
                ('bfs', 'Búsqueda en Amplitud (BFS)', buscar_solucion_BFS),
                ('dfs', 'Búsqueda en Profundidad (DFS)', buscar_solucion_DFS),
                ('ucs', 'Búsqueda con Costo Uniforme (UCS)', buscar_solucion_UCS),
            ]

            resultados = []

            for algorithm_key, algorithm_name, algorithm_fn in algoritmos:
                result = algorithm_fn(grafo, initial_state, target_state)

                if result is None:
                    resultados.append({
                        'algorithm_key': algorithm_key,
                        'algorithm_name': algorithm_name,
                        'found': False,
                        'path': [],
                        'route_text': 'No se encontró ruta',
                        'steps': 0,
                        'cost': 0,
                        'average_cost': '0.00',
                    })
                    continue

                ruta = obtener_ruta(result, initial_state)
                total_cost = result.get_costo() if algorithm_key == 'ucs' else _calcular_costo_total(grafo, ruta)
                steps = max(len(ruta) - 1, 0)
                average_cost = (total_cost / steps) if steps > 0 else 0

                resultados.append({
                    'algorithm_key': algorithm_key,
                    'algorithm_name': algorithm_name,
                    'found': True,
                    'path': ruta,
                    'route_text': ' → '.join(ruta),
                    'steps': steps,
                    'cost': total_cost,
                    'average_cost': f'{average_cost:.2f}',
                })

                SearchResult.objects.create(
                    search_type=algorithm_key,
                    initial_state=str(initial_state),
                    target_state=str(target_state),
                    result_path=str(ruta),
                    total_cost=total_cost
                )

            return JsonResponse({
                'success': True,
                'results': resultados,
                'message': '¡Resultados generados para BFS, DFS y UCS!'
            })
        
        except KeyError as e:
            return JsonResponse({
                'success': False,
                'error': f'Estado no encontrado en el grafo: {str(e)}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error en la búsqueda: {str(e)}'
            })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error inesperado: {str(e)}'
        })


def get_graph_nodes(request):
    """Retorna los nodos disponibles según el tipo de grafo"""
    nodes = list(GRAFOS['ciudades_costos'].keys())
    
    return JsonResponse({'nodes': nodes})


def get_results(request):
    """Retorna los últimos resultados de búsqueda"""
    results = SearchResult.objects.all().order_by('-created_at')[:10]
    data = []
    for result in results:
        data.append({
            'search_type': result.get_search_type_display(),
            'initial_state': result.initial_state,
            'target_state': result.target_state,
            'result_path': result.result_path,
            'total_cost': result.total_cost,
            'created_at': result.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({'results': data})
