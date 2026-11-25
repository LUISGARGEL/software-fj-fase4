from datetime import datetime
from cliente import Cliente
from excepciones_y_logs import OperacionInvalidaError, ValidacionError, logger
from servicios import Servicio


class Reserva:
    """Gestiona una reserva vinculando cliente, servicio, duracion y estado."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        if not isinstance(id_reserva, str) or not id_reserva.strip():
            raise ValidacionError("El ID de reserva debe ser un texto no vacio.")
        if not isinstance(cliente, Cliente):
            raise ValidacionError("Debe proporcionarse un objeto Cliente valido.")
        if not isinstance(servicio, Servicio):
            raise ValidacionError("Debe proporcionarse un objeto Servicio valido.")

        servicio.validar_parametros(duracion)

        self._id_reserva = id_reserva.strip()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "PENDIENTE"
        self._fecha_creacion = datetime.now().isoformat(timespec="seconds")
        self._monto_final = 0.0
        logger.info(
            f"Reserva creada: {self._id_reserva} | Cliente: {cliente.id_entidad} | "
            f"Servicio: {servicio.codigo} | Duracion: {duracion}"
        )

    @property
    def id_reserva(self) -> str:
        return self._id_reserva

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion(self) -> int:
        return self._duracion

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def monto_final(self) -> float:
        return self._monto_final

    def confirmar(self):
        if self._estado == "CANCELADA":
            raise OperacionInvalidaError(f"La reserva '{self._id_reserva}' esta cancelada y no puede confirmarse.")
        if self._estado == "PROCESADA":
            raise OperacionInvalidaError(f"La reserva '{self._id_reserva}' ya fue procesada.")
        if not self._servicio.disponible:
            raise OperacionInvalidaError(f"El servicio '{self._servicio.nombre}' no esta disponible.")

        self._estado = "CONFIRMADA"
        logger.info(f"Reserva confirmada: {self._id_reserva}")

    def cancelar(self, motivo: str = "Cancelacion solicitada por el cliente"):
        if self._estado == "PROCESADA":
            raise OperacionInvalidaError(f"No se puede cancelar la reserva '{self._id_reserva}' ya procesada.")
        if self._estado == "CANCELADA":
            raise OperacionInvalidaError(f"La reserva '{self._id_reserva}' ya esta cancelada.")

        self._estado = "CANCELADA"
        logger.warning(f"Reserva cancelada: {self._id_reserva} | Motivo: {motivo}")

    def procesar(self, impuesto_pct: float = 19.0, descuento_adicional: float = 0.0) -> float:
        if self._estado != "CONFIRMADA":
            raise OperacionInvalidaError(
                f"Solo se pueden procesar reservas CONFIRMADA. Estado de '{self._id_reserva}': {self._estado}."
            )

        descuento_total = float(descuento_adicional) + (5.0 if self._cliente.es_vip else 0.0)
        self._monto_final = self._servicio.calcular_costo(
            duracion=self._duracion,
            impuesto_pct=impuesto_pct,
            descuento_pct=descuento_total,
        )
        self._estado = "PROCESADA"
        logger.info(f"Reserva procesada: {self._id_reserva} | Monto final: ${self._monto_final:.2f}")
        return self._monto_final

    def resumen(self) -> str:
        return (
            f"[{self._id_reserva}] Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} (x{self._duracion}) | Total: ${self._monto_final:.2f}"
        )