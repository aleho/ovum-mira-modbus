"""Enums for Ovum Mira controllers."""

from enum import IntEnum


class OvumLicense(IntEnum):
    """License levels as per docs."""
    BASIC = 1
    PLUS = 2


class OvumHeatpumpStatus(IntEnum):
    """Operating status of the Ovum heat pump."""

    ERROR = 0  # Störung
    OFFLINE = 1  # Inverter Offline
    HOLD_OFF = 3  # Sperrzeit
    OIL_PREHEATING = 4  # Ölvorheizen
    STANDBY = 5  # Bereit
    STARTING = 6  # Start
    HOT_WATER = 7  # WW
    HEATING = 8  # HZ
    COOLING = 9  # Kühlen
    DEFROSTING = 10  # Abtauen
    MANUAL_DEFROST = 11  # Manuell Enteisen
    STOPPING = 12  # Stoppt
    LIMIT_UNDERCUT = 13  # Einsatzgrenze unterschritten
    INVERTER_RESET = 14  # Inverterresetprozess


class OvumHotWaterStatus(IntEnum):
    """Hot water production off/on."""

    OFF = 0  # WW_AUS
    ON = 1  # WW_EIN


class OvumHotWaterAvailable(IntEnum):
    """Hot water production installed and usable."""

    NO = 0  # NEIN
    YES = 1  # JA


class OvumHeatingCircuitType(IntEnum):
    """Heating circuit type installed."""

    NONE = 0  # HK_KEINER
    UNREGULATED = 1  # HK_UNGEREGELT
    RETURN = 2  # HK_RUECKLAUF
    MIXED = 3  # HK_GEMISCHT
    CUBE_DIRECT = 4  # HK_CUBE_DIREKT


class OvumHeatingCircuitMode(IntEnum):
    """Heating circuit mode."""

    OFF = 0  # HK_AUS
    AUTO = 1  # HK_AUTOMATIK
    HEATING = 2  # HK_WINTER
    COOLING = 3  # HK_SOMMER


class OvumHeatingCircuitOperationMode(IntEnum):
    """Heating circuit operation mode."""

    AUTO = 0  # AUTO
    HEATING = 1  # FIX_HEIZEN
    COOLING = 2  # FIX_KÜHLEN


class OvumEmsStatus(IntEnum):
    """Energy management status."""

    NEUTRAL = 0  # Neutral
    INCREASE = 1  # Erhöhen, kostenloser PV-Strom
    DECREASE = 2  # Reduzieren, es wird PV-Strom in kürze erwartet


class OvumHotWaterRequestStatus(IntEnum):
    """Hot water request status."""

    NONE = 0  # Keine Anforderung
    PLUS = 1  # Anforderung PLUS
    PHOTOVOLTAIC = 2  # Anforderung PV
    LEGIONELLA = 3  # Anforderung Legionellen
    NOMINAL = 4  # Anforderung Sollwert
    TURBO = 5  # Anforderung Turbo
    FROST = 6  # Anforderung Frost


class OvumFreshWaterStatus(IntEnum):
    """Fresh water status."""

    NONE = 0  # Keine Zapfung
    STANDBY = 1  # Standbyvolumenstrom
    TAP = 2  # Zapfung


class OvumVacationStatus(IntEnum):
    """Vacation status."""

    NO = 0  # NEIN
    YES = 1  # JA


class OvumBufferType(IntEnum):
    """Buffer type installed."""

    NONE = 0  # NEIN
    BUFFER = 1  # PUFFER
    CUBE = 2  # CUBESPEICHER


class OvumBufferMode(IntEnum):
    """Buffer mode."""

    NONE = 0
    HEATING = 1  # Heizen
    COOLING = 2  # Kühlen


class OvumBufferLoadingStatus(IntEnum):
    """Buffer mode."""

    BELOW_FROST = 0  # unter Frostwert
    BELOW_SWITCH_ON = 1  # unter Einschaltpunkt (Soll-Hys)
    BELOW_TARGET = 2  # unter Sollwert
    ABOVE_TARGET = 3  # über Sollwert
    ABOVE_SWITCH_OFF = 4  # über Soll+Hys
    NONE = 5  # kein Puffer konfiguriert


class OvumCoolBufferLoadingStatus(IntEnum):
    """Buffer mode.

    0: über soll+hys  ->  >24                      ==> einschalten
                    ----------- hysterese_o: +2
    2: unter soll+hys ->  <24 ==> >22 && <24       ==> kühlen
                    ----------- sollwert:    22
    3: unter soll     ->  <22 ==> <22 && >20       ==> kühlen
                    ----------- hysterese_u: -2
    4: unter soll-hys ->  <20                      ==> ausschalten
    """

    ABOVE_SWITCH_ON = 0  # über Soll+Hys
    UNUSED_1 = 1  # x
    ABOVE_TARGET = 2  # unter Sollwert+Hys
    BELOW_TARGET = 3  # unter sollwert
    BELOW_SWITCH_OFF = 4  # unter Soll-Hys
    NONE = 5  # kein Kühlpuffer konfiguriert


class OvumCoolBufferAvailable(IntEnum):
    """Cooling Buffer available."""

    NO = 0  # NEIN
    YES = 1  # JA


class OvumPvReleaseStatus(IntEnum):
    """Photovoltaic release status."""

    NOT_AVAILABLE = 0  # Nicht konfiguriert. Kein WPM verfügbar / Kein Zusatzheizung verfügbar.
    DEACTIVATED = 1  # Deaktiviert (Ausgeschalten)
    WAITING = 2  # Eingeschalten, warte auf PV
    OK = 3  # PVStatus OK (NETZ_PWR, SOC, WR_PWR) --> Freigabe der Sollwertanhebung
    NO_RELEASE = 4  # Keine Freigabe durch die Speicheranforderung.
    TOO_HOT = 5  # Zu warm, Wärmepumpe kann die Anforderung nicht mehr bedienen. / Zu warm, Zusatzheizung kann die Anforderung nicht mehr bedienen.
    ACTIVE = 6  # WP kann PV-Anforderung bedienen. WP-Anforderung. / Zusatzheizung kann PV-Anforderung bedienen. Zusatzheizung-Anforderung.
