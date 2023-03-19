# flake8: noqa

from collections import defaultdict
from typing import Dict

from cereal import car
from selfdrive.car import dbc_dict

Ecu = car.CarParams.Ecu
NetworkLocation = car.CarParams.NetworkLocation
TransmissionType = car.CarParams.TransmissionType
GearShifter = car.CarState.GearShifter

class CarControllerParams:
  HCA_STEP = 2                   # HCA_01 message frequency 50Hz
  LDW_STEP = 10                  # LDW_02 message frequency 10Hz
  GRA_ACC_STEP = 3               # GRA_ACC_01 message frequency 33Hz

  GRA_VBP_STEP = 100             # Send ACC virtual button presses once a second
  GRA_VBP_COUNT = 16             # Send VBP messages for ~0.5s (GRA_ACC_STEP * 16)

  # Observed documented MQB limits: 3.00 Nm max, rate of change 5.00 Nm/sec.
  # Limiting rate-of-change based on real-world testing and Comma's safety
  # requirements for minimum time to lane departure.
  STEER_MAX = 300                # Max heading control assist torque 3.00 Nm
  STEER_DELTA_UP = 4             # Max HCA reached in 1.50s (STEER_MAX / (50Hz * 1.50))
  STEER_DELTA_DOWN = 10          # Min HCA reached in 0.60s (STEER_MAX / (50Hz * 0.60))
  STEER_DRIVER_ALLOWANCE = 80
  STEER_DRIVER_MULTIPLIER = 3    # weight driver torque heavily
  STEER_DRIVER_FACTOR = 1        # from dbc

class CANBUS:
  pt = 0
  cam = 2

class DBC_FILES:
  audi_b8 = "audi_b8"  # Used for Audi A5 B8 and B8.5
  
DBC = defaultdict(lambda: dbc_dict(DBC_FILES.audi_b8, None))  # type: Dict[str, Dict[str, str]]

BUTTON_STATES = {
  "accelCruise": False,
  "decelCruise": False,
  "cancel": False,
  "setCruise": False,
  "resumeCruise": False,
  "gapAdjustCruise": False
}

MQB_LDW_MESSAGES = {
  "none": 0,                            # Nothing to display
  "laneAssistUnavailChime": 1,          # "Lane Assist currently not available." with chime
  "laneAssistUnavailNoSensorChime": 3,  # "Lane Assist not available. No sensor view." with chime
  "laneAssistTakeOverUrgent": 4,        # "Lane Assist: Please Take Over Steering" with urgent beep
  "emergencyAssistUrgent": 6,           # "Emergency Assist: Please Take Over Steering" with urgent beep
  "laneAssistTakeOverChime": 7,         # "Lane Assist: Please Take Over Steering" with chime
  "laneAssistTakeOverSilent": 8,        # "Lane Assist: Please Take Over Steering" silent
  "emergencyAssistChangingLanes": 9,    # "Emergency Assist: Changing lanes..." with urgent beep
  "laneAssistDeactivated": 10,          # "Lane Assist deactivated." silent with persistent icon afterward
}

# Check the 7th and 8th characters of the VIN before adding a new CAR. If the
# chassis code is already listed below, don't add a new CAR, just add to the
# FW_VERSIONS for that existing CAR.
# Exception: SEAT Leon and SEAT Ateca share a chassis code

class CAR:
  AUDI_A5_B8 = "AUDI A5 B8"                         # Chassis 8T/8K, Audi A4/A5 B8/B8.5 and variants

# All supported cars should return FW from the engine, srs, eps, and fwdRadar. Cars
# with a manual trans won't return transmission firmware, but all other cars will.
#
# The 0xF187 SW part number query should return in the form of N[NX][NX] NNN NNN [X[X]],
# where N=number, X=letter, and the trailing two letters are optional. Performance
# tuners sometimes tamper with that field (e.g. 8V0 9C0 BB0 1 from COBB/EQT). Tampered
# ECU SW part numbers are invalid for vehicle ID and compatibility checks. Try to have
# them repaired by the tuner before including them in openpilot.

FINGERPRINTS = {
  CAR.AUDI_A5_B8: [{
    64: 8, 134: 8, 159: 8, 256: 8, 257: 8, 259: 8, 260: 8, 261: 8, 262: 8, 264: 8, 265: 8, 266: 8, 267: 4, 268: 8, 279: 8, 286: 8, 294: 8, 776: 8, 778: 8, 779: 8, 780: 8, 782: 8, 785: 4, 810: 8, 914: 8, 919: 8, 959: 8, 960: 4, 994: 8, 1312: 8, 1318: 8, 1413: 8, 1440: 5, 1520: 5, 1605: 8, 1714: 8, 1716: 8, 1720: 8
  }],
  
#FW_VERSIONS = {
#  CAR.AUDI_Q3_MK2: {
#    (Ecu.engine, 0x7e0, None): [
#      b'\xf1\x8705E906018N \xf1\x899970',
#      b'\xf1\x8783A906259  \xf1\x890001',
#      b'\xf1\x8783A906259  \xf1\x890005',
#    ],
#    (Ecu.transmission, 0x7e1, None): [
#      b'\xf1\x8709G927158CN\xf1\x893608',
#      b'\xf1\x870GC300046F \xf1\x892701',
#    ],
#    (Ecu.srs, 0x715, None): [
#      b'\xf1\x875Q0959655BF\xf1\x890403\xf1\x82\x1321211111211200311121232152219321422111',
#      b'\xf1\x875Q0959655CC\xf1\x890421\xf1\x82\x131111111111120031111237116A119321532111',
#    ],
#    (Ecu.eps, 0x712, None): [
#      b'\xf1\x875Q0910143C \xf1\x892211\xf1\x82\x0567G6000300',
#      b'\xf1\x875Q0910143C \xf1\x892211\xf1\x82\x0567G6000800',
#   ],
#    (Ecu.fwdRadar, 0x757, None): [
#      b'\xf1\x872Q0907572R \xf1\x890372',
#      b'\xf1\x872Q0907572T \xf1\x890383',
#    ],
#  },
}
