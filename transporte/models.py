from django.db import models
from django.utils import timezone

# ----------------------------------------------------
#                    VEHICULO
# ----------------------------------------------------
class Vehiculo(models.Model):
    patente = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    capacidad_kg = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"


# ----------------------------------------------------
#                    AERONAVE
# ----------------------------------------------------
class Aeronave(models.Model):
    matricula = models.CharField(max_length=15, unique=True)
    tipo = models.CharField(max_length=50)
    capacidad_kg = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.matricula


# ----------------------------------------------------
#                    CONDUCTOR
# ----------------------------------------------------
class Conductor(models.Model):
    nombre = models.CharField(max_length=100)
    licencia = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# ----------------------------------------------------
#                    PILOTO
# ----------------------------------------------------
class Piloto(models.Model):
    nombre = models.CharField(max_length=100)
    licencia_vuelo = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# ----------------------------------------------------
#                    RUTA
# ----------------------------------------------------
class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    distancia_km = models.DecimalField(max_digits=8, decimal_places=2)
    duracion_estim_min = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.origen} → {self.destino}"


# ----------------------------------------------------
#                    CLIENTE
# ----------------------------------------------------
class Cliente(models.Model):
    TIPO_CHOICES = [
        ('empresa', 'Empresa'),
        ('particular', 'Particular'),
    ]

    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    direccion = models.CharField(max_length=300, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, default='Chile')
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

    @property
    def despachos_count(self):
        return self.despachos.count()

    @property
    def es_vip(self):
        return self.despachos_count > 20


# ----------------------------------------------------
#                    DESPACHO
# ----------------------------------------------------
class Despacho(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    fecha = models.DateField(auto_now_add=True)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True, blank=True)

    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True, blank=True)
    piloto = models.ForeignKey(Piloto, on_delete=models.SET_NULL, null=True, blank=True)

    # Relación Cliente → Despachos
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="despachos"
    )

    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('en_transito', 'En tránsito'),
            ('entregado', 'Entregado'),
        ],
        default='pendiente'
    )

    def __str__(self):
        return f"Despacho {self.codigo} - {self.estado}"


# ----------------------------------------------------
#                    CARGA
# ----------------------------------------------------
class Carga(models.Model):
    TIPO_CHOICES = [
        ('terrestre', 'Terrestre'),
        ('aereo', 'Aéreo'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en-transito', 'En Tránsito'),
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada'),
    ]

    id_carga = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    dimensiones = models.CharField(max_length=100, blank=True, null=True)
    fecha_envio = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    descripcion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Carga'
        verbose_name_plural = 'Cargas'

    def save(self, *args, **kwargs):
        if not self.id_carga:
            last_carga = Carga.objects.order_by('fecha_creacion').last()
            new_id = 1 if not last_carga else int(last_carga.id_carga.split('-')[1]) + 1
            self.id_carga = f'CRG-{str(new_id).zfill(3)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_carga} - {self.cliente}"

    @property
    def is_heavy(self):
        return self.peso > 1000
