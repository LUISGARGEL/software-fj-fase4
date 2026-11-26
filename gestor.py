from collections import Counter
from cliente import Cliente
from excepciones_y_logs import OperacionInvalidaError, ValidacionError, logger
from reserva import Reserva
from servicios import Servicio


class GestorSoftwareFJ:
    """Administra colecciones de clientes, servicios y reservas con consultas y reportes."""

    def __init__(self):
        self._clientes: dict[str, Cliente] = {}
        self._servicios: dict[str, Servicio] = {}
        self._reservas: list[Reserva] = []
        logger.info("GestorSoftwareFJ inicializado.")

    def registrar_cliente(self, cliente: Cliente) -> Cliente:
        if not isinstance(cliente, Cliente):
            raise ValidacionError("Solo se pueden registrar objetos de tipo Cliente.")
        if cliente.id_entidad in self._clientes:
            raise OperacionInvalidaError(f"El cliente con ID '{cliente.id_entidad}' ya esta registrado.")
        self._clientes[cliente.id_entidad] = cliente
        logger.info(f"Cliente agregado al gestor: {cliente.id_entidad}")
        return cliente

    def obtener_cliente(self, id_cliente: str) -> Cliente:
        if id_cliente not in self._clientes:
            raise OperacionInvalidaError(f"No existe cliente con ID '{id_cliente}'.")
        return self._clientes[id_cliente]

    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        if not isinstance(servicio, Servicio):
            raise ValidacionError("Solo se pueden registrar objetos de tipo Servicio.")
        if servicio.codigo in self._servicios:
            raise OperacionInvalidaError(f"El servicio con codigo '{servicio.codigo}' ya esta registrado.")
        self._servicios[servicio.codigo] = servicio
        logger.info(f"Servicio agregado al gestor: {servicio.codigo}")
        return servicio

    def obtener_servicio(self, codigo_servicio: str) -> Servicio:
        if codigo_servicio not in self._servicios:
            raise OperacionInvalidaError(f"No existe servicio con codigo '{codigo_servicio}'.")
        return self._servicios[codigo_servicio]

    def crear_reserva(self, id_reserva: str, id_cliente: str, codigo_servicio: str, duracion: int) -> Reserva:
        if any(r.id_reserva == id_reserva.strip() for r in self._reservas):
            raise OperacionInvalidaError(f"Ya existe una reserva con ID '{id_reserva.strip()}'.")
        cliente = self.obtener_cliente(id_cliente)
        servicio = self.obtener_servicio(codigo_servicio)
        if not servicio.disponible:
            raise OperacionInvalidaError(f"El servicio '{servicio.nombre}' no esta disponible para reservar.")

        reserva = Reserva(id_reserva=id_reserva, cliente=cliente, servicio=servicio, duracion=duracion)
        self._reservas.append(reserva)
        return reserva

    def buscar_reserva(self, id_reserva: str) -> Reserva:
        for reserva in self._reservas:
            if reserva.id_reserva == id_reserva:
                return reserva
        raise OperacionInvalidaError(f"No se encontro reserva con ID '{id_reserva}'.")

    def confirmar_reserva(self, id_reserva: str):
        reserva = self.buscar_reserva(id_reserva)
        reserva.confirmar()

    def cancelar_reserva(self, id_reserva: str, motivo: str = "Cancelacion registrada en gestor"):
        reserva = self.buscar_reserva(id_reserva)
        reserva.cancelar(motivo)

    def procesar_reserva(self, id_reserva: str, impuesto_pct: float = 19.0, descuento_adicional: float = 0.0) -> float:
        reserva = self.buscar_reserva(id_reserva)
        return reserva.procesar(impuesto_pct=impuesto_pct, descuento_adicional=descuento_adicional)

    def listar_servicios(self, solo_disponibles: bool = False) -> list[Servicio]:
        if solo_disponibles:
            return [s for s in self._servicios.values() if s.disponible]
        return list(self._servicios.values())

    def consultar_reservas(self, estado: str | None = None, id_cliente: str | None = None) -> list[Reserva]:
        resultado = self._reservas
        if estado is not None:
            estado_norm = estado.strip().upper()
            resultado = [r for r in resultado if r.estado == estado_norm]
        if id_cliente is not None:
            resultado = [r for r in resultado if r.cliente.id_entidad == id_cliente]
        return resultado

    def generar_reporte(self) -> dict:
        conteo_estados = Counter(r.estado for r in self._reservas)
        ingresos_procesados = round(sum(r.monto_final for r in self._reservas if r.estado == "PROCESADA"), 2)
        conteo_servicios = Counter(r.servicio.nombre for r in self._reservas)
        servicio_mas_solicitado = (
            conteo_servicios.most_common(1)[0] if conteo_servicios else ("Ninguno", 0)
        )
        return {
            "total_clientes": len(self._clientes),
            "total_servicios": len(self._servicios),
            "total_reservas": len(self._reservas),
            "reservas_por_estado": dict(conteo_estados),
            "ingresos_procesados": ingresos_procesados,
            "servicio_mas_solicitado": servicio_mas_solicitado,
        }