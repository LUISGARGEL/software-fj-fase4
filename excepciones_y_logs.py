import logging
from abc import ABC, abstractmethod

# Registra eventos y errores en archivo de texto sin usar bases de datos
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger("SoftwareFJ")


class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""


class ValidacionError(SoftwareFJError):
    """Error cuando un dato o parámetro no cumple con las reglas de validación."""


class OperacionInvalidaError(SoftwareFJError):
    """Error cuando se intenta una operación no permitida o inconsistente."""


class EntidadSistema(ABC):
    """Clase abstracta base para entidades generales del sistema."""

    def __init__(self, id_entidad: str):
        # Valida que el ID sea un texto no vacío
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ValidacionError("El ID de la entidad debe ser un texto no vacío.")
        self._id_entidad = id_entidad.strip()

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @abstractmethod
    def resumen(self) -> str:
        """Retorna un resumen legible de la entidad."""