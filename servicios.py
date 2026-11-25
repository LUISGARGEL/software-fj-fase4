from abc import ABC, abstractmethod
from excepciones_y_logs import OperacionInvalidaError, ValidacionError


class Servicio(ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, disponible: bool = True):
        self._codigo = self._validar_texto(codigo, "código del servicio")
        self._nombre = self._validar_texto(nombre, "nombre del servicio")
        self._tarifa_base = self._validar_monto_positivo(tarifa_base, "tarifa base")
        self._disponible = bool(disponible)

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValidacionError(f"El {campo} debe ser un texto no vacío.")
        return valor.strip()

    @staticmethod
    def _validar_monto_positivo(valor: float, campo: str) -> float:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            raise ValidacionError(f"El {campo} debe ser un número mayor que cero.")
        return float(valor)

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, duracion: int):
        """Valida que la duración cumpla las reglas del servicio específico."""

    @abstractmethod
    def describir_servicio(self) -> str:
        """Devuelve la descripción legible del servicio."""

    @abstractmethod
    def calcular_costo_base(self, duracion: int) -> float:
        """Calcula el costo base según la duración y las reglas del servicio."""

    def calcular_costo(
        self,
        duracion: int,
        impuesto_pct: float = 0.0,
        descuento_pct: float = 0.0,
        recargo_extra: float = 0.0,
    ) -> float:
        """Calcula el costo final admitiendo argumentos opcionales (sobrecarga en Python)."""
        self.validar_parametros(duracion)

        if not self._disponible:
            raise OperacionInvalidaError(f"El servicio '{self._nombre}' no está disponible.")
        if isinstance(descuento_pct, bool) or descuento_pct < 0 or descuento_pct >= 100:
            raise ValidacionError("El porcentaje de descuento debe estar entre 0 y 99.9.")
        if isinstance(impuesto_pct, bool) or impuesto_pct < 0:
            raise ValidacionError("El porcentaje de impuesto no puede ser negativo.")
        if isinstance(recargo_extra, bool) or recargo_extra < 0:
            raise ValidacionError("El recargo extra no puede ser negativo.")

        subtotal = self.calcular_costo_base(duracion) + float(recargo_extra)
        con_descuento = subtotal * (1.0 - float(descuento_pct) / 100.0)
        total = con_descuento * (1.0 + float(impuesto_pct) / 100.0)
        return round(max(0.0, total), 2)


class ReservaSala(Servicio):
    """Servicio de reserva de salas por horas."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad_max: int, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if isinstance(capacidad_max, bool) or not isinstance(capacidad_max, int) or capacidad_max <= 0:
            raise ValidacionError("La capacidad máxima de la sala debe ser un entero positivo.")
        self._capacidad_max = capacidad_max

    @property
    def capacidad_max(self) -> int:
        return self._capacidad_max

    def validar_parametros(self, duracion: int):
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise ValidacionError("La reserva de sala requiere una duración entera en horas mayor a 0.")

    def describir_servicio(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Reserva de Sala] {self._nombre} ({self._codigo}) | "
            f"Capacidad: {self._capacidad_max} | Tarifa: ${self._tarifa_base:.2f}/h | {estado}"
        )

    def calcular_costo_base(self, duracion: int) -> float:
        return self._tarifa_base * duracion


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos por días."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, tipo_equipo: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self._tipo_equipo = self._validar_texto(tipo_equipo, "tipo de equipo")

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    def validar_parametros(self, duracion: int):
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion < 1:
            raise ValidacionError("El alquiler de equipo requiere al menos 1 día.")

    def describir_servicio(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Alquiler de Equipo] {self._nombre} ({self._tipo_equipo}) | "
            f"Tarifa: ${self._tarifa_base:.2f}/día | {estado}"
        )

    def calcular_costo_base(self, duracion: int) -> float:
        # Otorga 10% de rebaja en la tarifa base cuando el alquiler es de 5 días o más
        factor = 0.9 if duracion >= 5 else 1.0
        return self._tarifa_base * duracion * factor


class AsesoriaEspecializada(Servicio):
    """Servicio de asesorías especializadas por sesiones."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self._especialidad = self._validar_texto(especialidad, "especialidad")

    @property
    def especialidad(self) -> str:
        return self._especialidad

    def validar_parametros(self, duracion: int):
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise ValidacionError("La asesoría especializada requiere al menos 1 sesión entera.")

    def describir_servicio(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Asesoría Especializada] {self._nombre} ({self._especialidad}) | "
            f"Tarifa: ${self._tarifa_base:.2f}/sesión | {estado}"
        )

    def calcular_costo_base(self, duracion: int) -> float:
        return self._tarifa_base * duracion