from django.shortcuts import render

# Create your views here.
import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Proyecto


@method_decorator(csrf_exempt, name='dispatch')
class ProyectoView(View):

    def get(self, request, pk=None):
        if pk:
            proyecto = get_object_or_404(Proyecto, pk=pk)
            return JsonResponse({
                "id": proyecto.id,
                "nombre": proyecto.nombre,
                "descripcion": proyecto.descripcion,
                "activo": proyecto.activo
            }, status=200)

        proyectos = list(Proyecto.objects.values("id", "nombre", "descripcion", "activo"))
        return JsonResponse({"proyectos": proyectos}, status=200)

    def post(self, request):
        try:
            body = json.loads(request.body.decode("utf-8"))
            if not body.get("nombre"):
                return JsonResponse({"error": "El campo 'nombre' es obligatorio"}, status=400)

            proyecto = Proyecto.objects.create(
                nombre=body["nombre"],
                descripcion=body.get("descripcion", ""),
                activo=body.get("activo", True)
            )
            return JsonResponse({
                "mensaje": "Proyecto creado",
                "id": proyecto.id,
                "nombre": proyecto.nombre
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

    def put(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        try:
            body = json.loads(request.body.decode("utf-8"))
            proyecto.nombre = body.get("nombre", proyecto.nombre)
            proyecto.descripcion = body.get("descripcion", proyecto.descripcion)
            proyecto.activo = body.get("activo", proyecto.activo)
            proyecto.save()

            return JsonResponse({
                "mensaje": "Proyecto actualizado",
                "id": proyecto.id,
                "nombre": proyecto.nombre
            }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

    def delete(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        proyecto.delete()
        return JsonResponse({"mensaje": f"Proyecto {pk} eliminado"}, status=200)