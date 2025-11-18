from rest_framework import viewsets
from django.shortcuts import render

from .models import (
    Vehiculo, Aeronave, Piloto, Ruta,
    Despacho, Carga, Cliente
)

from .serializers import (
    VehiculoSerializer, AeronaveSerializer,
    PilotoSerializer, RutaSerializer,
    DespachoSerializer, CargaSerializer,
    ClienteSerializer
)

# --- VISTAS HTML ---
def home(request):
    return render(request, 'home.html')

def aeronaves(request):   # <-- corregido: antes estaba "aeronavess"
    return render(request, 'aeronaves.html')

def despachos(request):
    return render(request, 'despachos.html')

def pilotos(request):
    return render(request, 'pilotos.html')

def rutas(request):
    return render(request, 'rutas.html')

def vehiculos(request):
    return render(request, 'vehiculos.html')

def carga(request):
    return render(request, 'carga.html')

def cliente(request):
    return render(request, 'cliente.html')


# --- API REST ---
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class AeronaveViewSet(viewsets.ModelViewSet):
    queryset = Aeronave.objects.all()
    serializer_class = AeronaveSerializer

class PilotoViewSet(viewsets.ModelViewSet):
    queryset = Piloto.objects.all()
    serializer_class = PilotoSerializer

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class DespachoViewSet(viewsets.ModelViewSet):
    queryset = Despacho.objects.all()
    serializer_class = DespachoSerializer

class CargaViewSet(viewsets.ModelViewSet):
    queryset = Carga.objects.all()
    serializer_class = CargaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
