# Taller: Desarrollo de Endpoints Nativos en Django
**Curso:** Desarrollo de aplicaciones Web I -- 4E  
**Docente:** Jose Javier Torres Vanstrahlen  

---

## 1. Investigación: Verbos HTTP y Operaciones CRUD en Django Nativo

En Django nativo (sin librerías externas como Django REST Framework), la creación de endpoints se implementa mediante **Vistas Basadas en Clases (CBV)** que heredan de `django.views.View`. Estas vistas enrutan automáticamente cada petición HTTP hacia un método homónimo dentro de la clase (`get()`, `post()`, `put()`, `delete()`), permitiendo procesar y devolver datos en formato JSON asociados a las operaciones **CRUD** (*Create, Read, Update, Delete*):

| Verbo HTTP | Operación CRUD | Método en `View` | Caso de Uso | Códigos HTTP |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | **R**ead (Leer) | `get(self, request, pk=None)` | Consultar la lista completa de registros (sin `pk`) o el detalle de un recurso específico (con `pk`). No modifica datos en el servidor. | `200 OK`<br>`404 Not Found` |
| **POST** | **C**reate (Crear) | `post(self, request)` | Recibir datos en formato JSON en el cuerpo de la petición (`request.body`) para crear un nuevo registro en la base de datos. | `201 Created`<br>`400 Bad Request` |
| **PUT** | **U**pdate (Actualizar) | `put(self, request, pk)` | Actualizar los atributos de un registro existente identificado por su llave primaria (`pk`). | `200 OK`<br>`404 Not Found` |
| **DELETE** | **D**elete (Eliminar) | `delete(self, request, pk)` | Eliminar un registro específico de la base de datos utilizando su `pk`. | `200 OK`<br>`404 Not Found` |

---

## 2. Módulos, Funciones y Decoradores Utilizados

* **`django.views.View`**: Clase base para vistas basadas en clases. Inspecciona `request.method` y despacha la solicitud al método correspondiente (`get`, `post`, `put`, `delete`).
* **`django.http.JsonResponse`**: Subclase de `HttpResponse` que serializa diccionarios de Python a JSON y establece la cabecera `Content-Type: application/json`.
* **`json` (`json.loads`)**: Módulo estándar de Python usado para decodificar los bytes de `request.body` a un diccionario manipulable en peticiones `POST` y `PUT`.
* **`django.urls.path`**: Función usada en `urls.py` para mapear rutas URL a vistas y capturar parámetros dinámicos como `<int:pk>`.
* **`View.as_view()`**: Método de clase llamado en `urls.py` que convierte la clase en una función invocable capaz de recibir un `HttpRequest` y retornar una respuesta.
* **`django.shortcuts.get_object_or_404`**: Función auxiliar que busca un objeto en la base de datos; si no existe, lanza automáticamente una respuesta `404 Not Found`.
* **`@method_decorator` (`django.utils.decorators.method_decorator`)**: Decorador que permite aplicar decoradores de funciones sobre vistas basadas en clases (por ejemplo, sobre `name='dispatch'`).
* **`@csrf_exempt` (`django.views.decorators.csrf.csrf_exempt`)**: Desactiva la validación del token CSRF en la vista para permitir peticiones `POST`, `PUT` y `DELETE` desde clientes externos (como Postman) sin sesiones HTML.

---

