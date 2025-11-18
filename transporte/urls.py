from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'vehiculos', views.VehiculoViewSet)
router.register(r'aeronaves', views.AeronaveViewSet)
router.register(r'pilotos', views.PilotoViewSet)
router.register(r'rutas', views.RutaViewSet)
router.register(r'despachos', views.DespachoViewSet, basename='despachos')

# Si necesitas registrar el mismo ViewSet bajo diferentes rutas, usa basename único:
router.register(r'carga', views.DespachoViewSet, basename='carga')
router.register(r'cliente', views.DespachoViewSet, basename='cliente')

urlpatterns = [
    # Páginas HTML
    path('', views.home, name='home'),
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('aeronaves/', views.aeronaves, name='aeronaves'),
    path('pilotos/', views.pilotos, name='pilotos'),
    path('rutas/', views.rutas, name='rutas'),
  path('despachos/', views.despachos, name='despachos'),

    path('carga/', views.carga, name='carga'),
    path('cliente/', views.cliente, name='cliente'),

    # API
    path('api/', include(router.urls)),
]