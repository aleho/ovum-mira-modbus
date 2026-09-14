"""Modbus register addresses"""
# TODO License level 3  "BMS"  registers

from enum import IntEnum


class Addr(IntEnum):
    """Publicly available registers, docs version 1.1.3

    Float values are big endian and resolution 0.1, unless documented
    otherwise.
    """

    #                                            doc name               type / range             license lvl

    VERSION                          = 20      # Softwareversion        str4                     1

    WW_STATUS                        = 55000   # WW_SWITCH_ON           u16               r/w    1
    WW_TEMP_TARGET                   = 55001   # WW_SOLL                s16    °C  0-62   r/w    1
    WW_TEMP_TARGET_PV                = 55002   # WW_SOLL_PV             s16    °C  0-67   r/w    1
    WW_AVAILABLE                     = 55003   # SYS_WW                 u16                      1
    WW_RES_TEMP_TARGET               = 55004   # WW_DESIREDTEMP         f32    °C                1
    WW_RES_TEMP_ACTUAL_TOP           = 55007   # WW_ACTUALTEMPO         f32    °C                1
    WW_RES_TEMP_ACTUAL_BOTTOM        = 55009   # WW_ACTUALTEMPU         f32    °C                1
    WW_REQ_STATUS                    = 55012   # WW_ANFSTATUS           s16                      2
    WW_FRESH_WATER_TARGET            = 55014   # FWS_SOLL               s16    °C  10-65  r/w    2
    WW_FRESH_WATER_STATUS            = 55015   # WW_FWSSTSSTATUS        s16                      2
    WW_CIRC_PUMP_STATUS              = 55016   # WW_ZIRKPUMP            bool                     2
    WW_CIRC_PUMP_TEMP                = 55017   # WW_ZIRKT               f32    °C                2
    WW_VACATION_STATUS               = 55019   # WW_URLAUB              s16                      2

    BUFFER_TYPE                      = 55020   # SYS_PUFFER             u16                      1
    BUFFER_TEMP_TARGET_PV            = 55021   # PUFFER_SOLL_PV         s16    °C  0-70   r/w    1
    BUFFER_MODE                      = 55022   # HPUF_STATUS            s16                      2
    BUFFER_TEMP_TARGET               = 55023   # HPUF_SOLLTEMP          f32    °C                1
    BUFFER_TEMP_ACTUAL_TOP           = 55026   # HPUF_PUOT              f32    °C                1
    BUFFER_TEMP_ACTUAL_BOTTOM        = 55028   # HPUF_PUUT              f32    °C                1
    BUFFER_LOADING_STATUS            = 55030   # HPUF_LADESTATUS        s16                      2

    COOL_BUFFER_AVAILABLE            = 55040   # SYS_KUE_PUFFER         s16                      2
    COOL_BUFFER_TEMP_ACTUAL_BOTTOM   = 55041   # KPUF_PUUT              f32    °C                2 
    COOL_BUFFER_TEMP_TARGET          = 55043   # KPUF_SOLLTEMP          f32    °C                2
    COOL_BUFFER_LOADING_STATUS       = 55045   # KPUF_LADESTATUS        s16                      2

    WW_CASCADE_REQUEST               = 55058   # BIV_KASKWWANF          bool                     2
    HEAT_CASCADE_REQUEST             = 55059   # BIV_KASKHZANF          bool                     2
    COOL_CASCADE_REQUEST             = 55060   # BIV_KASKKUEANF         bool                     2

    EMS_STATUS                       = 55070   # HSM_EMS_PVSTATUS       s16               r/w    1
    EMS_BATTERY                      = 55071   # HSM_EMS_BATTERIESOC    s16    %          r/w    1
    EMS_GRID_POWER                   = 55072   # HSM_EMS_NETZPOWER      s32    W          r/w1   1
    EMS_INVERTER_POWER               = 55074   # HSM_EMS_WRPOWER        s32    W          r/w    1
    EMS_TARGET_POWER                 = 55076   # HSM_EMS_SOLLPOWER      s32    W          r/w    1

    PV_RELEASE_WW                    = 55079   # HSM_PVENABLE_WPWW      s16                      2
    PV_RELEASE_HEAT                  = 55081   # HSM_PVENABLE_WPHZ      s16                      2
    PV_RELEASE_STAGE_2_WW            = 55083   # HSM_PVENABLE_ST2WW     s16                      2
    PV_RELEASE_STAGE_2_HEAT          = 55085   # HSM_PVENABLE_ST2HZ     s16                      2

    SYS_NAME                         = 56000   # SYS_TYPE               str10                    1
    SERIAL_NUMBER                    = 56010   # SYS_SNRKEY             str10                    1 (docs=2, but available in v1.1.4)

    WPM_DEMAND                       = 56020   # WPM_WP_ANFSOLL         s16    %                 1
    WPM_POWER_CONSUMPTION            = 56021   # WPM_WP_PWR             f32    kW                1
    WPM_POWER_PRODUCTION             = 56023   # WPM_KO_PWR             f32    kW                1
    WPM_STATUS                       = 56025   # WPM_WPM_STATUS         s16                      1
    WPM_CONDENSER_INPUT              = 56026   # WPM_KOET               f32    °C                1
    WPM_CONDENSER_OUTPUT             = 56028   # WPM_KOAT               f32    °C                1
    WPM_COMPRESSOR_ONTIME            = 56030   # WPM_COMPRESSOR_ONTIME  s32    minutes           1

    OUTDOOR_TEMP                     = 56048   # HSM_TAUS               f32    °C                1

    HEAT_CIRC_1_TYPE                 = 56050   # HK1_TYPE               u16                      1
    HEAT_CIRC_1_TARGET_PLUS_PV       = 56051   # HK1_PV_TVLPLUS         s16    K  0-25    r/w    1
    HEAT_CIRC_1_TARGET_MINUS_PV      = 56052   # HK1_PV_TVLMINUS        s16    K  —25-0   r/w    1
    HEAT_CIRC_1_TARGET               = 56053   # HK1_DESIREDTEMP        f32    °C                1 (docs say r/w, but system errors)
    HEAT_CIRC_1_ACTUAL               = 56055   # HK1_ACTUALVALUE        f32    °C         r/w    1
    HEAT_CIRC_1_MODE                 = 56057   # HK1_MODE               u16               r/w    1
    HEAT_CIRC_1_ROOM_TARGET          = 56058   # HK1_RAUMSOLL_HZ        f32    °C  0-50   r/w    1

    HEAT_CIRC_2_TYPE                 = 56060   # HK2_TYPE               u16                      1
    HEAT_CIRC_2_TARGET_PLUS_PV       = 56061   # HK2_PV_TVLPLUS         s16    K  0-25    r/w    1
    HEAT_CIRC_2_TARGET_MINUS_PV      = 56062   # HK2_PV_TVLMINUS        s16    K  -25-0   r/w    1
    HEAT_CIRC_2_TARGET               = 56063   # HK2_DESIREDTEMP        f32    °C                1
    HEAT_CIRC_2_ACTUAL               = 56065   # HK2_ACTUALVALUE        f32    °C         r/w    1
    HEAT_CIRC_2_MODE                 = 56067   # HK2_MODE               u16               r/w    1
    HEAT_CIRC_2_ROOM_TARGET          = 56068   # HK2_RAUMSOLL_HZ        f32    °C  0-50   r/w    1=r/o

    HEAT_CIRC_3_TYPE                 = 56070   # HK3_TYPE               u16                      2
    HEAT_CIRC_3_TARGET_PLUS_PV       = 56071   # HK3_PV_TVLPLUS         s16    K  0-25    r/w    2
    HEAT_CIRC_3_TARGET_MINUS_PV      = 56072   # HK3_PV_TVLMINUS        s16    K  -25-0   r/w    2
    HEAT_CIRC_3_TARGET               = 56073   # HK3_DESIREDTEMP        f32    °C                2
    HEAT_CIRC_3_ACTUAL               = 56075   # HK3_ACTUALVALUE        f32    °C         r/w    2
    HEAT_CIRC_3_MODE                 = 56077   # HK3_MODE               u16               r/w    2
    HEAT_CIRC_3_ROOM_TARGET          = 56078   # HK3_RAUMSOLL_HZ        f32    °C  0-50   r/w    2

    HEAT_CIRC_4_TYPE                 = 56080   # HK4_TYPE               u16                      2
    HEAT_CIRC_4_TARGET_PLUS_PV       = 56081   # HK4_PV_TVLPLUS         s16    K  0-25    r/w    2
    HEAT_CIRC_4_TARGET_MINUS_PV      = 56082   # HK4_PV_TVLMINUS        s16    K  -25-0   r/w    2
    HEAT_CIRC_4_TARGET               = 56083   # HK4_DESIREDTEMP        f32    °C                2
    HEAT_CIRC_4_ACTUAL               = 56085   # HK4_ACTUALVALUE        f32    °C         r/w    2
    HEAT_CIRC_4_MODE                 = 56087   # HK4_MODE               u16               r/w    2
    HEAT_CIRC_4_ROOM_TARGET          = 56088   # HK4_RAUMSOLL_HZ        f32    °C  0-50   r/w    2

    HEAT_CIRC_1_COOL_ROOM_TARGET     = 56150   # HK1_RAUMSOLL_KUE       f32    °C  0-50   r/w    2
    HEAT_CIRC_1_ROOM_ACTUAL          = 56152   # HK1_ACTUALROOMTEMP     f32    °C                2
    HEAT_CIRC_1_VACATION_STATUS      = 56154   # HK1_URLAUB             s16               r/w    2
    HEAT_CIRC_1_VACATION_HEAT_TARGET = 56155   # HK1_TVL_URLAUB_HZ      s16    °C  0-50   r/w    2
    HEAT_CIRC_1_VACATION_COOL_TARGET = 56156   # HK1_TVL_URLAUB_KUE     s16    °C  0-50   r/w    2
    HEAT_CIRC_1_OPERATION_MODE       = 56157   # HK1_FIX_MODE           s16               r/w    2
    HEAT_CIRC_1_FIXED_HEAT_TARGET    = 56158   # HK1_FIXWERT_HZ         s16    °C  0-100  r/w    2
    HEAT_CIRC_1_FIXED_COOL_TARGET    = 56159   # HK1_FIXWERT_KUE        s16    °C  0-100  r/w    2
    HEAT_CIRC_1_HEAT_LIMIT           = 56160   # HK1_AT_HEIZGRENZE      f32    °C  0-100  r/w    2

    HEAT_CIRC_2_COOL_ROOM_TARGET     = 56175   # HK2_RAUMSOLL_KUE       f32    °C  0-50   r/w    2
    HEAT_CIRC_2_ROOM_ACTUAL          = 56177   # HK2_ACTUALROOMTEMP     f32    °C                2
    HEAT_CIRC_2_VACATION_STATUS      = 56179   # HK2_URLAUB             s16               r/w    2
    HEAT_CIRC_2_VACATION_HEAT_TARGET = 56180   # HK2_TVL_URLAUB_HZ      s16    °C  0-50   r/w    2
    HEAT_CIRC_2_VACATION_COOL_TARGET = 56181   # HK2_TVL_URLAUB_KUE     s16    °C  0-50   r/w    2
    HEAT_CIRC_2_OPERATION_MODE       = 56182   # HK2_FIX_MODE           s16               r/w    2
    HEAT_CIRC_2_FIXED_HEAT_TARGET    = 56183   # HK2_FIXWERT_HZ         s16    °C  0-100  r/w    2
    HEAT_CIRC_2_FIXED_COOL_TARGET    = 56184   # HK2_FIXWERT_KUE        s16    °C  0-100  r/w    2
    HEAT_CIRC_2_HEAT_LIMIT           = 56185   # HK2_AT_HEIZGRENZE      f32    °C  0-100  r/w    2

    HEAT_CIRC_3_COOL_ROOM_TARGET     = 56200   # HK3_RAUMSOLL_KUE       f32    °C  0-50   r/w    2
    HEAT_CIRC_3_ROOM_ACTUAL          = 56202   # HK3_ACTUALROOMTEMP     f32    °C                2
    HEAT_CIRC_3_VACATION_STATUS      = 56204   # HK3_URLAUB             s16               r/w    2
    HEAT_CIRC_3_VACATION_HEAT_TARGET = 56205   # HK3_TVL_URLAUB_HZ      s16    °C  0-50   r/w    2
    HEAT_CIRC_3_VACATION_COOL_TARGET = 56206   # HK3_TVL_URLAUB_KUE     s16    °C  0-50   r/w    2
    HEAT_CIRC_3_OPERATION_MODE       = 56207   # HK3_FIX_MODE           s16               r/w    2
    HEAT_CIRC_3_FIXED_HEAT_TARGET    = 56208   # HK3_FIXWERT_HZ         s16    °C  0-100  r/w    2
    HEAT_CIRC_3_FIXED_COOL_TARGET    = 56209   # HK3_FIXWERT_KUE        s16    °C  0-100  r/w    2
    HEAT_CIRC_3_HEAT_LIMIT           = 56210   # HK3_AT_HEIZGRENZE      f32    °C  0-100  r/w    2

    HEAT_CIRC_4_COOL_ROOM_TARGET     = 56225   # HK3_RAUMSOLL_KUE       f32    °C  0-50   r/w    2
    HEAT_CIRC_4_ROOM_ACTUAL          = 56227   # HK3_ACTUALROOMTEMP     f32    °C                2
    HEAT_CIRC_4_VACATION_STATUS      = 56229   # HK3_URLAUB             s16               r/w    2
    HEAT_CIRC_4_VACATION_HEAT_TARGET = 56230   # HK3_TVL_URLAUB_HZ      s16    °C  0-50   r/w    2
    HEAT_CIRC_4_VACATION_COOL_TARGET = 56231   # HK3_TVL_URLAUB_KUE     s16    °C  0-50   r/w    2
    HEAT_CIRC_4_OPERATION_MODE       = 56232   # HK3_FIX_MODE           s16               r/w    2
    HEAT_CIRC_4_FIXED_HEAT_TARGET    = 56233   # HK3_FIXWERT_HZ         s16    °C  0-100  r/w    2
    HEAT_CIRC_4_FIXED_COOL_TARGET    = 56234   # HK3_FIXWERT_KUE        s16    °C  0-100  r/w    2
    HEAT_CIRC_4_HEAT_LIMIT           = 56235   # HK3_AT_HEIZGRENZE      f32    °C  0-100  r/w    2
