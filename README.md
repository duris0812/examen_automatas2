# Sistema de Búsquedas - BFS, DFS y UCS

Un sistema Django interactivo que permite ejecutar tres algoritmos de búsqueda diferentes:
- **BFS** (Búsqueda en Amplitud)
- **DFS** (Búsqueda en Profundidad)
- **UCS** (Búsqueda con Costo Uniforme)

La interfaz pide primero la ciudad inicial y la ciudad objetivo. Después muestra el selector de algoritmo para ejecutar la búsqueda.

## 🚀 Instalación

1. Navega a la carpeta del proyecto:
```bash
cd "Examen"
```

2. Crea y activa un entorno virtual (si no está activado):
```bash
python -m venv .venv
.venv\Scripts\activate  # En Windows
source .venv/bin/activate  # En macOS/Linux
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Realiza las migraciones de la base de datos:
```bash
python manage.py migrate
```

## 🎮 Uso

1. Ejecuta el servidor Django:
```bash
python manage.py runserver
```

2. Abre tu navegador en:
```
http://127.0.0.1:8000/
```

3. Selecciona el algoritmo de búsqueda y ejecuta tu búsqueda.

## 🚀 Despliegue en Render

1. Sube la carpeta `Examen` a GitHub.
2. Crea un nuevo Web Service en Render.
3. Conecta el repositorio de GitHub.
4. Usa estas configuraciones:
    - `Build Command`: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
    - `Start Command`: `gunicorn search_project.wsgi:application`
5. Variables de entorno recomendadas:
    - `DEBUG=false`
    - `SECRET_KEY=<una clave larga y segura>`
    - `ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1`
6. Despliega y abre la URL pública de Render.

## 📊 Algoritmos Disponibles

### 🌊 BFS (Búsqueda en Amplitud)
- Explora por niveles
- Garantiza el camino más corto en términos de pasos
- Funciona con grafos de ciudades

**Ejemplo:**
- Inicio: Jiloyork
- Objetivo: Monterrey
- Resultado: Ruta óptima en número de pasos

### 📊 DFS (Búsqueda en Profundidad)
- Explora hacia las profundidades primero
- Usa menos memoria que BFS
- Funciona con el mismo grafo de ciudades

**Ejemplo:**
- Inicio: Jiloyork
- Objetivo: Monterrey
- Resultado: Ruta encontrada por profundidad

### 💰 UCS (Búsqueda con Costo Uniforme)
- Encuentra la ruta con menor costo total
- Óptimo en términos de costo
- Funciona con grafos ponderados (ciudades con distancias)

**Ejemplo:**
- Inicio: Jiloyork
- Objetivo: Monterrey
- Resultado: Ruta con menor costo total

## 📁 Estructura del Proyecto

```
Examen/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── search_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── search_app/
    ├── migrations/
    ├── static/
    │   └── search_app/
    │       └── style.css
    ├── templates/
    │   └── search_app/
    │       └── index.html
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── arbol.py
    ├── models.py
    ├── searches.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

## 🛠️ Tecnologías

- Django 4.2
- Python 3.7+
- SQLite3
- HTML5, CSS3, JavaScript

## 📝 Notas

- La interfaz muestra los resultados debajo del formulario
- BFS, DFS y UCS usan ciudades como entrada
- La aplicación es completamente responsiva

## 👨‍💻 Desarrollo

Para acceder al panel de administración:
```bash
python manage.py createsuperuser
```

Luego visita: `http://127.0.0.1:8000/admin/`
