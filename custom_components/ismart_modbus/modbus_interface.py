"""Interface Modbus pour iSMART."""
import logging
import serial
from typing import List, Tuple, Optional

_LOGGER = logging.getLogger(__name__)


def crc16(trame: List[int], trame_size: int) -> int:
    """
    Calcul le CRC16 avec le polynome Modbus.
    
    Args:
        trame: trame modbus
        trame_size: longueur de la trame
        
    Returns:
        CRC calculé
    """
    crc = 0xFFFF
    polynome = 0xA001

    for i in range(0, trame_size):
        crc ^= trame[i]
        for j in range(0, 8):
            parity = crc
            crc >>= 1
            if parity % 2:
                crc ^= polynome
    return crc


def readreg(link: serial.Serial, slave: int, reg: int, length: int) -> List[int]:
    """
    Modbus (03H) Register read operation.
    
    Args:
        link: MODBUS communication serial link
        slave: MODBUS address of the slave to be read
        reg: Address of the first register to be read
        length: Number of registers to be read
        
    Returns:
        Liste des données lues ou -1 en cas d'erreur
    """
    trame = [slave, 0x03, reg >> 8, reg & 0x00FF, length >> 8, length & 0x00FF]
    crc = crc16(trame, 6)
    trame.extend((crc & 0x00FF, crc >> 8))
    
    link.readline()
    link.write(bytes(trame))
   
    trame = list(link.read(3))

    if len(trame) != 3:
        _LOGGER.warning('readreg: receive incomplete Modbus frame')
        link.readline()
        return [-1]
        
    if trame[0] != slave:
        _LOGGER.warning('readreg: returned slave address error')
        link.readline()
        return [-1]
        
    if trame[1] != 0x03:
        if trame[1] == 0x83:
            _LOGGER.warning('readreg: PLC error (Exception code = %x)', trame[2])
        else:
            _LOGGER.warning('readreg: returned function error')
        link.readline()
        return [-1]
        
    if trame[2] != 2 * length:
        _LOGGER.warning('Returned frame length error')
        link.readline()
        return [-1]

    trame += list(link.read(2 * length + 2))
    if len(trame) != 2 * length + 5:
        _LOGGER.warning('Frame length error')
        link.readline()
        return [-1]

    if crc16(trame, len(trame) - 2) != trame[-1] * 0x100 + trame[-2]:
        _LOGGER.warning('CRC error')
        link.readline()
        return [-1]
        
    return trame[3:3 + 2 * length]


def writecoil(link: serial.Serial, slave: int, coil: int, state: int) -> int:
    """
    Modbus Write Single Coil (05H) operation.
    
    Args:
        link: MODBUS communication serial link
        slave: MODBUS address of the slave
        coil: Address of the coil to be written
        state: Coil state (1 or 0)
        
    Returns:
        0 en cas de succès, -1 en cas d'erreur
    """
    trame = [slave, 0x05, coil >> 8, coil & 0x00FF, state * 0xFF, 0x00]
    
    crc = crc16(trame, 6)
    trame.extend((crc & 0x00FF, crc >> 8))
    link.flushInput()
    link.readline()

    _LOGGER.info("writecoil - slave: %s, coil: 0x%04X, state: %s", slave, coil, state)
    
    link.write(bytes(trame))
    
    ack = list(link.read(3))
    if len(ack) != 3:
        _LOGGER.warning('Cannot read the first three bytes')
        return -1
    
    if ack[0] != slave:
        _LOGGER.warning('Returned slave address error')
        link.readline()
        return -1
        
    if ack[1] != 0x05:
        if ack[1] == 0x85:
            _LOGGER.warning("PLC error (Exception code = %x)", ack[2])
        else:
            _LOGGER.warning('Returned function error')
        link.readline()
        return -1

    ack += list(link.read(5))
    if len(ack) != 8:
        _LOGGER.warning('Cannot read the entire frame')
        link.readline()
        return -1
    
    if ack != trame:
        _LOGGER.warning('Ack error')
        return 0
        
    _LOGGER.info('Ack OK')
    return 0


class ModbusInterface:
    """Gestion de l'interface Modbus RS485."""
    
    def __init__(self, port: str, baudrate: int = 38400, timeout: float = 0.03):
        """Initialize Modbus interface."""
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.rs485: Optional[serial.Serial] = None
        
    async def async_connect(self) -> bool:
        """Connect to Modbus interface."""
        try:
            self.rs485 = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                writeTimeout=0.1
            )
            _LOGGER.info('Connection RS485 ouverte sur %s', self.port)
            return True
        except (IOError, OSError) as err:
            _LOGGER.error('Echec ouverture lien RS485: %s', err)
            return False
    
    def disconnect(self):
        """Disconnect from Modbus interface."""
        if self.rs485:
            try:
                self.rs485.close()
                _LOGGER.info('Connection RS485 fermée')
            except Exception as err:
                _LOGGER.error('Erreur fermeture RS485: %s', err)
            finally:
                self.rs485 = None
    
    def writecoil_device(self, slave: int, coil: int, value: int) -> int:
        """Write coil to device."""
        if not self.rs485:
            _LOGGER.error('RS485 non connecté')
            return -1
        return writecoil(self.rs485, slave, coil, value)
    
    def readstate(self) -> Tuple[List[int], List[int], List[int]]:
        """
        Lit l'état de tous les automates.
        
        Returns:
            Tuple (outvalid, outstate, memstate)
        """
        outvalid = [0, 0, 0, 0, 0]
        outstate = [0, 0, 0, 0, 0]
        memstate = [0, 0, 0, 0, 0]
        
        if not self.rs485:
            _LOGGER.error('RS485 non connecté')
            return (outvalid, outstate, memstate)
        
        for i in range(0, 5):
            data = readreg(self.rs485, i + 1, 0x0608, 0x0012)
            if data == [-1] or data[0] == -1:
                outvalid[i] = 0
                _LOGGER.warning('Echec lecture automate %s', i + 1)
            else:
                outvalid[i] = 1
                memstate[i] = data[1] + 0x100 * data[0]
                outstate[i] = data[23] + 0x100 * data[21]
        
        _LOGGER.debug("outvalid: %s", outvalid)
        _LOGGER.debug("outstate: %s", outstate)
        _LOGGER.debug("memstate: %s", memstate)
        
        return (outvalid, outstate, memstate)
