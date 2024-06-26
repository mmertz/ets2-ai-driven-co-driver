# https://github.com/RenCloud/scs-sdk-plugin/blob/V.1.12/scs-telemetry/inc/scs-telemetry-common.hpp
from .unpack import (ArraySruct, BasicStruct, BytesStruct, DictStruct,
                     StringStruct, struct_bool, struct_double, struct_float,
                     struct_int, struct_long_long, struct_unsigned_int,
                     struct_unsigned_long_long)

VERSION_NUMBER = 12
STRUCT_TELEMETRY_VERSION = BasicStruct("40xI")
SUBSTANCE_SIZE = 25
STRING_SIZE = 64

struct_trailer = DictStruct(
    # Start of 1st zone
    ("wheelSteerable", ArraySruct(struct_bool, 16)),
    ("wheelSimulated", ArraySruct(struct_bool, 16)),
    ("wheelPowered", ArraySruct(struct_bool, 16)),
    ("wheelLiftable", ArraySruct(struct_bool, 16)),
    ("wheelOnGround", ArraySruct(struct_bool, 16)),
    ("attached", struct_bool),
    (None, BytesStruct(3)),
    # End of 1st zone
    # Start of 2nd zone
    ("wheelSubstance", ArraySruct(struct_unsigned_int, 16)),
    ("wheelCount", struct_unsigned_int),
    # End of 2nd zone
    # Start of 3rd zone
    ("cargoDamage", struct_float),
    ("wearChassis", struct_float),
    ("wearWheels", struct_float),
    ("wearBody", struct_float),
    ("wheelSuspDeflection", ArraySruct(struct_float, 16)),
    ("wheelVelocity", ArraySruct(struct_float, 16)),
    ("wheelSteering", ArraySruct(struct_float, 16)),
    ("wheelRotation", ArraySruct(struct_float, 16)),
    ("wheelLift", ArraySruct(struct_float, 16)),
    ("wheelLiftOffset", ArraySruct(struct_float, 16)),
    ("wheelRadius", ArraySruct(struct_float, 16)),
    # End of 3rd zone
    # Start of 4th zone
    ("linearVelocityX", struct_float),
    ("linearVelocityY", struct_float),
    ("linearVelocityZ", struct_float),
    ("angularVelocityX", struct_float),
    ("angularVelocityY", struct_float),
    ("angularVelocityZ", struct_float),
    ("linearAccelerationX", struct_float),
    ("linearAccelerationY", struct_float),
    ("linearAccelerationZ", struct_float),
    ("angularAccelerationX", struct_float),
    ("angularAccelerationY", struct_float),
    ("angularAccelerationZ", struct_float),
    ("hookPositionX", struct_float),
    ("hookPositionY", struct_float),
    ("hookPositionZ", struct_float),
    ("wheelPositionX", ArraySruct(struct_float, 16)),
    ("wheelPositionY", ArraySruct(struct_float, 16)),
    ("wheelPositionZ", ArraySruct(struct_float, 16)),
    (None, BytesStruct(4)),
    # End of 4th zone
    # Start of 5th zone
    ("worldX", struct_double),
    ("worldY", struct_double),
    ("worldZ", struct_double),
    ("rotationX", struct_double),
    ("rotationY", struct_double),
    ("rotationZ", struct_double),
    # End of 5th zone
    # Start of 6th zone
    # 10 string below, scs-telemetry-common.hpp count 9 is not correct.
    ("id", StringStruct(STRING_SIZE)),
    ("cargoAcessoryId", StringStruct(STRING_SIZE)),
    ("bodyType", StringStruct(STRING_SIZE)),
    ("brandId", StringStruct(STRING_SIZE)),
    ("brand", StringStruct(STRING_SIZE)),
    ("name", StringStruct(STRING_SIZE)),
    ("chainType", StringStruct(STRING_SIZE)),
    ("licensePlate", StringStruct(STRING_SIZE)),
    ("licensePlateCountry", StringStruct(STRING_SIZE)),
    ("licensePlateCountryId", StringStruct(STRING_SIZE)),
    # End of 6th zone
)

struct_telemetry = DictStruct(
    # Start of 1st Zone
    ("sdkActive", struct_bool),
    (None, BytesStruct(3)),
    ("paused", struct_bool),
    (None, BytesStruct(3)),
    ("time", struct_unsigned_long_long),
    ("simulatedTime", struct_unsigned_long_long),
    ("renderTime", struct_unsigned_long_long),
    ("multiplayerTimeOffset", struct_long_long),
    # End of 1st zone
    # Start of 2nd zone
    ("telemetry_plugin_revision", struct_unsigned_int),
    ("version_major", struct_unsigned_int),
    ("version_minor", struct_unsigned_int),
    ("game", struct_unsigned_int), # actually 0 for unknown,1 for ets2 and 2 for ats
    ("telemetry_version_game_major", struct_unsigned_int),
    ("telemetry_version_game_minor", struct_unsigned_int),
    ("time_abs", struct_unsigned_int), # In game time in minutes
    ("gears", struct_unsigned_int),
    ("gears_reverse", struct_unsigned_int),
    ("retarderStepCount", struct_unsigned_int),
    ("truckWheelCount", struct_unsigned_int),
    ("selectorCount", struct_unsigned_int),
    ("time_abs_delivery", struct_unsigned_int),
    ("maxTrailerCount", struct_unsigned_int),
    ("unitCount", struct_unsigned_int),
    ("plannedDistanceKm", struct_unsigned_int),
    ("shifterSlot", struct_unsigned_int),
    ("retarderBrake", struct_unsigned_int),
    ("lightsAuxFront", struct_unsigned_int),
    ("lightsAuxRoof", struct_unsigned_int),
    ("truck_wheelSubstance", ArraySruct(struct_unsigned_int, 16)),
    ("hshifterPosition", ArraySruct(struct_unsigned_int, 32)),
    ("hshifterBitmask", ArraySruct(struct_unsigned_int, 32)),
    ("jobDeliveredDeliveryTime", struct_unsigned_int),
    ("jobStartingTime", struct_unsigned_int),
    ("jobFinishedTime", struct_unsigned_int),
    (None, BytesStruct(48)),
    # End of 2nd Zone
    # Start of 3rd Zone
    ("restStop", struct_int),
    ("gear", struct_int),
    ("gearDashboard", struct_int),
    ("hshifterResulting", ArraySruct(struct_int, 32)),
    ("jobDeliveredEarnedXp", struct_int),
    (None, BytesStruct(56)),
    # End of 3rd Zone
    # Start of 4th Zone
    ("scale", struct_float),
    ("fuelCapacity", struct_float),
    ("fuelWarningFactor", struct_float),
    ("adblueCapacity", struct_float),
    ("adblueWarningFactor", struct_float),
    ("airPressureWarning", struct_float),
    ("airPressurEmergency", struct_float),
    ("oilPressureWarning", struct_float),
    ("waterTemperatureWarning", struct_float),
    ("batteryVoltageWarning", struct_float),
    ("engineRpmMax", struct_float),
    ("gearDifferential", struct_float),
    ("cargoMass", struct_float),
    ("truckWheelRadius", ArraySruct(struct_float, 16)),
    ("gearRatiosForward", ArraySruct(struct_float, 24)),
    ("gearRatiosReverse", ArraySruct(struct_float, 8)),
    ("unitMass", struct_float),
    ("speed", struct_float),
    ("engineRpm", struct_float),
    ("userSteer", struct_float),
    ("userThrottle", struct_float),
    ("userBrake", struct_float),
    ("userClutch", struct_float),
    ("gameSteer", struct_float),
    ("gameThrottle", struct_float),
    ("gameBrake", struct_float),
    ("gameClutch", struct_float),
    ("cruiseControlSpeed", struct_float),
    ("airPressure", struct_float),
    ("brakeTemperature", struct_float),
    ("fuel", struct_float),
    ("fuelAvgConsumption", struct_float),
    ("fuelRange", struct_float),
    ("adblue", struct_float),
    ("oilPressure", struct_float),
    ("oilTemperature", struct_float),
    ("waterTemperature", struct_float),
    ("batteryVoltage", struct_float),
    ("lightsDashboard", struct_float),
    ("wearEngine", struct_float),
    ("wearTransmission", struct_float),
    ("wearCabin", struct_float),
    ("wearChassis", struct_float),
    ("wearWheels", struct_float),
    ("truckOdometer", struct_float),
    ("routeDistance", struct_float),
    ("routeTime", struct_float),
    ("speedLimit", struct_float),
    ("truck_wheelSuspDeflection", ArraySruct(struct_float, 16)),
    ("truck_wheelVelocity", ArraySruct(struct_float, 16)),
    ("truck_wheelSteering", ArraySruct(struct_float, 16)),
    ("truck_wheelRotation", ArraySruct(struct_float, 16)),
    ("truck_wheelLift", ArraySruct(struct_float, 16)),
    ("truck_wheelLiftOffset", ArraySruct(struct_float, 16)),
    ("jobDeliveredCargoDamage", struct_float),
    ("jobDeliveredDistanceKm", struct_float),
    ("refuelAmount", struct_float),
    ("cargoDamage", struct_float),
    (None, BytesStruct(28)),
    # End of 4th Zone
    # Start of 5th Zone
    ("truckWheelSteerable", ArraySruct(struct_bool, 16)),
    ("truckWheelSimulated", ArraySruct(struct_bool, 16)),
    ("truckWheelPowered", ArraySruct(struct_bool, 16)),
    ("truckWheelLiftable", ArraySruct(struct_bool, 16)),
    ("isCargoLoaded", struct_bool),
    ("specialJob", struct_bool),
    ("parkBrake", struct_bool),
    ("motorBrake", struct_bool),
    ("airPressureWarning", struct_bool),
    ("airPressureEmergency", struct_bool),
    ("fuelWarning", struct_bool),
    ("adblueWarning", struct_bool),
    ("oilPressureWarning", struct_bool),
    ("waterTemperatureWarning", struct_bool),
    ("batteryVoltageWarning", struct_bool),
    ("electricEnabled", struct_bool),
    ("engineEnabled", struct_bool),
    ("wipers", struct_bool),
    ("blinkerLeftActive", struct_bool),
    ("blinkerRightActive", struct_bool),
    ("blinkerLeftOn", struct_bool),
    ("blinkerRightOn", struct_bool),
    ("lightsParking", struct_bool),
    ("lightsBeamLow", struct_bool),
    ("lightsBeamHigh", struct_bool),
    ("lightsBeacon", struct_bool),
    ("lightsBrake", struct_bool),
    ("lightsReverse", struct_bool),
    ("lightsHazards", struct_bool),
    ("cruiseControl", struct_bool),
    ("truckWheelOnGround", ArraySruct(struct_bool, 16)),
    ("shifterToggle", ArraySruct(struct_bool, 2)),
    ("differentialLock", struct_bool),
    ("liftAxle", struct_bool),
    ("liftAxleIndicator", struct_bool),
    ("trailerLiftAxle", struct_bool),
    ("trailerLiftAxleIndicator", struct_bool),
    ("jobDeliveredAutoparkUsed", struct_bool),
    ("jobDeliveredAutoloadUsed", struct_bool),
    (None, BytesStruct(25)),
    # End of 5th zone
    # Start of 6th zone
    ("cabinPositionX", struct_float),
    ("cabinPositionY", struct_float),
    ("cabinPositionY", struct_float),
    ("headPositionX", struct_float),
    ("headPositionY", struct_float),
    ("headPositionZ", struct_float),
    ("truckHookPositionX", struct_float),
    ("truckHookPositionY", struct_float),
    ("truckHookPositionZ", struct_float),
    ("truckWheelPositionX", ArraySruct(struct_float, 16)),
    ("truckWheelPositionY", ArraySruct(struct_float, 16)),
    ("truckWheelPositionZ", ArraySruct(struct_float, 16)),
    ("lv_accelerationX", struct_float),
    ("lv_accelerationY", struct_float),
    ("lv_accelerationZ", struct_float),
    ("av_accelerationX", struct_float),
    ("av_accelerationY", struct_float),
    ("av_accelerationZ", struct_float),
    ("accelerationX", struct_float),
    ("accelerationY", struct_float),
    ("accelerationZ", struct_float),
    ("aa_accelerationX", struct_float),
    ("aa_accelerationY", struct_float),
    ("aa_accelerationZ", struct_float),
    ("cabinAVX", struct_float),
    ("cabinAVY", struct_float),
    ("cabinAVZ", struct_float),
    ("cabinAAX", struct_float),
    ("cabinAAY", struct_float),
    ("cabinAAZ", struct_float),
    (None, BytesStruct(60)),
    # End of 6th zone
    # Start of 7th zone
    ("cabinOffsetX", struct_float),
    ("cabinOffsetY", struct_float),
    ("cabinOffsetZ", struct_float),
    ("cabinOffsetrotationX", struct_float),
    ("cabinOffsetrotationY", struct_float),
    ("cabinOffsetrotationZ", struct_float),
    ("headOffsetX", struct_float),
    ("headOffsetY", struct_float),
    ("headOffsetZ", struct_float),
    ("headOffsetrotationX", struct_float),
    ("headOffsetrotationY", struct_float),
    ("headOffsetrotationZ", struct_float),
    (None, BytesStruct(152)),
    # End of 7th zone
    # Start of 8th zone
    ("coordinateX", struct_double),
    ("coordinateY", struct_double),
    ("coordinateZ", struct_double),
    ("rotationX", struct_double),
    ("rotationY", struct_double),
    ("rotationZ", struct_double),
    (None, BytesStruct(52)),
    # End of 8th zone
    # Start of 9th zone
    ("truckBrandId", StringStruct(STRING_SIZE)),
    ("truckBrand", StringStruct(STRING_SIZE)),
    ("truckId", StringStruct(STRING_SIZE)),
    ("truckName", StringStruct(STRING_SIZE)),
    ("cargoId", StringStruct(STRING_SIZE)),
    ("cargo", StringStruct(STRING_SIZE)),
    ("cityDstId", StringStruct(STRING_SIZE)),
    ("cityDst", StringStruct(STRING_SIZE)),
    ("compDstId", StringStruct(STRING_SIZE)),
    ("compDst", StringStruct(STRING_SIZE)),
    ("citySrcId", StringStruct(STRING_SIZE)),
    ("citySrc", StringStruct(STRING_SIZE)),
    ("compSrcId", StringStruct(STRING_SIZE)),
    ("compSrc", StringStruct(STRING_SIZE)),
    ("shifterType", StringStruct(16)),
    ("truckLicensePlate", StringStruct(STRING_SIZE)),
    ("truckLicensePlateCountryId", StringStruct(STRING_SIZE)),
    ("truckLicensePlateCountry", StringStruct(STRING_SIZE)),
    ("jobMarket", StringStruct(32)),
    ("fineOffence", StringStruct(32)),
    ("ferrySourceName", StringStruct(STRING_SIZE)),
    ("ferryTargetName", StringStruct(STRING_SIZE)),
    ("ferrySourceId", StringStruct(STRING_SIZE)),
    ("ferryTargetId", StringStruct(STRING_SIZE)),
    ("trainSourceName", StringStruct(STRING_SIZE)),
    ("trainTargetName", StringStruct(STRING_SIZE)),
    ("trainSourceId", StringStruct(STRING_SIZE)),
    ("trainTargetId", StringStruct(STRING_SIZE)),
    (None, BytesStruct(20)),
    # End of 9th zone
    # Start of 10th zone
    ("jobIncome", struct_unsigned_long_long),
    (None, BytesStruct(192)),
    # End of 10th zone
    # Start of 11th zone
    ("jobCancelledPenalty", struct_long_long),
    ("jobDeliveredRevenue", struct_long_long),
    ("fineAmount", struct_long_long),
    ("tollgatePayAmount", struct_long_long),
    ("ferryPayAmount", struct_long_long),
    ("trainPayAmount", struct_long_long),
    (None, BytesStruct(52)),
    # End of 11th zone
    # Start of 12th zone
    ("onJob", struct_bool),
    ("jobFinished", struct_bool),
    ("jobCancelled", struct_bool),
    ("jobDelivered", struct_bool),
    ("fined", struct_bool),
    ("tollgate", struct_bool),
    ("ferry", struct_bool),
    ("train", struct_bool),
    ("refuel", struct_bool),
    ("refuelPayed", struct_bool),
    (None, BytesStruct(90)),
    # End of 12th zone
    # Start of 13th zone
    ("substances", ArraySruct(StringStruct(STRING_SIZE), SUBSTANCE_SIZE)),
    # End of 13th zone
    # Start of 14th zone - Contains space for up to 10 trailers
    ("trailer", ArraySruct(struct_trailer, 10))
    # scs-telemetry-common.hpp wrong, end of 14th zone is 21600, not 21620
    # End of 14th zone
)

def get_version_number():
    return VERSION_NUMBER

def is_same_version(data):
    return STRUCT_TELEMETRY_VERSION.unpack_from(data) == VERSION_NUMBER

def parse_data(data):
    return struct_telemetry.unpack_from(data)
