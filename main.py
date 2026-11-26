from cliente import Cliente
from excepciones_y_logs import SoftwareFJError, logger
from gestor import GestorSoftwareFJ
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def ejecutar_simulacion():
    logger.info("=== Inicio de simulacion Software FJ ===")
    gestor = GestorSoftwareFJ()

    c1 = Cliente("CLI-01", "Luis Argel", "luisgargel@gmail.com", "3001234567", es_vip=True)
    c2 = Cliente("CLI-02", "Maria Perez", "maria.perez@correo.co", "3159876543", es_vip=False)
    gestor.registrar_cliente(c1)
    gestor.registrar_cliente(c2)

    try:
        Cliente("CLI-03", "A", "correo-invalido", "123")
    except SoftwareFJError as exc:
        logger.warning(f"Validacion de cliente rechazada controlada: {exc}")

    s1 = ReservaSala("SAL-01", "Sala Cartagena", 60000, capacidad_max=15)
    s2 = AlquilerEquipo("EQP-01", "Kit Sonido y Microfonos", 85000, tipo_equipo="Audio profesional")
    s3 = AsesoriaEspecializada("ASE-01", "Asesoria Arquitectura de Software", 120000, especialidad="Backend & Cloud")
    gestor.registrar_servicio(s1)
    gestor.registrar_servicio(s2)
    gestor.registrar_servicio(s3)

    print("\n--- CATALOGO DE SERVICIOS ---")
    for serv in gestor.listar_servicios():
        print(serv.describir_servicio())

    gestor.crear_reserva("RES-01", "CLI-01", "SAL-01", duracion=3)
    gestor.crear_reserva("RES-02", "CLI-02", "EQP-01", duracion=5)
    gestor.crear_reserva("RES-03", "CLI-01", "ASE-01", duracion=2)

    gestor.confirmar_reserva("RES-01")
    gestor.procesar_reserva("RES-01", impuesto_pct=19.0)

    gestor.confirmar_reserva("RES-02")
    gestor.procesar_reserva("RES-02", impuesto_pct=19.0, descuento_adicional=5.0)

    gestor.cancelar_reserva("RES-03", motivo="Reprogramacion solicitada por el cliente")

    try:
        gestor.procesar_reserva("RES-03")
    except SoftwareFJError as exc:
        logger.warning(f"Operacion invalida bloqueada: {exc}")

    print("\n--- RESERVAS PROCESADAS ---")
    for res in gestor.consultar_reservas(estado="PROCESADA"):
        print(res.resumen())

    print("\n--- REPORTE GERENCIAL SOFTWARE FJ ---")
    reporte = gestor.generar_reporte()
    for clave, valor in reporte.items():
        print(f"- {clave}: {valor}")

    logger.info("=== Fin de simulacion Software FJ ===")


if __name__ == "__main__":
    ejecutar_simulacion()