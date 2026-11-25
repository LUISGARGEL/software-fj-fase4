import re
from excepciones_y_logs import EntidadSistema, ValidacionError, logger


class Cliente(EntidadSistema):
    """Representa un cliente con atributos encapsulados y validaciones estrictas."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str, es_vip: bool = False):
        super().__init__(id_cliente)
        # Usa las propiedades para validar al instanciar el objeto
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self._es_vip = bool(es_vip)
        logger.info(f"Cliente registrado: {self._id_entidad} - {self._nombre}")

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValidacionError("El nombre del cliente debe tener al menos 2 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not isinstance(valor, str) or not re.match(patron, valor.strip()):
            raise ValidacionError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        # Conserva solo dígitos y exige al menos 7 dígitos
        solo_digitos = re.sub(r"\D", "", str(valor))
        if len(solo_digitos) < 7:
            raise ValidacionError(f"Teléfono inválido: '{valor}'. Debe tener al menos 7 dígitos.")
        self._telefono = solo_digitos

    @property
    def es_vip(self) -> bool:
        return self._es_vip

    def resumen(self) -> str:
        tipo = "VIP" if self._es_vip else "Estándar"
        return f"[{self._id_entidad}] {self._nombre} ({tipo}) | {self._correo} | Tel: {self._telefono}"