from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum


class Usuario(models.Model): #Datos de los usuarios
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo_electronico = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    talla_zapatilla = models.CharField(max_length=5)
    direccion = models.CharField(max_length=100)
    numero_telefono = models.CharField(max_length=20)
    rut = models.CharField(max_length=20, unique=True)


class Zapatilla(models.Model): #Datos de las Zapatillas que se rifan y link de su pagina.
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='zapatillas/')
    talla_disponible = models.CharField(max_length=5)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    cupos_maximos_rifa = models.IntegerField()
    enlace_nike = models.URLField()

    def __str__(self):
        return self.nombre


class Rifa(models.Model):
    zapatilla = models.ForeignKey(Zapatilla, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    cupos_disponibles = models.IntegerField()
    fecha_inicio = models.DateTimeField(default=None, null=True)
    fecha_fin = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f'Rifa para {self.zapatilla}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            # Si la zapatilla está completamente pagada en rifas, se puede iniciar la rifa
            if self.zapatilla.cupos_maximos_rifa == self.zapatilla.rifa_set.aggregate(total_cupos=Sum('cupos_disponibles'))['total_cupos']:
                self.fecha_inicio = timezone.now()
                self.fecha_fin = timezone.now() + timedelta(days=7)  # La rifa dura 7 días por defecto
        super(Rifa, self).save(*args, **kwargs)


class Compra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rifa = models.ForeignKey(Rifa, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    cupos_comprados = models.IntegerField(default=1)

    def __str__(self):
        return f'Compra de {self.usuario} para la rifa {self.rifa}'

    def save(self, *args, **kwargs):
        # Verificar si el usuario ha alcanzado el límite de compra en esta rifa
        if self.rifa.compra_set.filter(usuario=self.usuario).count() >= 5:
            raise ValueError('El usuario ha alcanzado el límite de compra en esta rifa')
        super(Compra, self).save(*args, **kwargs)


class Pago(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=20, choices=(
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado')))
   

