import ctypes

"""
all data structure for udp packets
all values are encoded using Little Endian format
example of use in the data structure:
unit16 -> cyteps ushort
unit8 -> cytpes ubyte
unit32 -> cytpes uint
unit64 -> cyptes longlong


Packets details info was learning by topic of codemasters
https://forums.codemasters.com/topic/50942-f1-2020-udp-specification/
"""

class PacketHeader(ctypes.LittleEndianStructure):
    """data structure packet header
    """
    _pack_ = 1
    _fields_ = [
        ('m_packetFormat', ctypes.c_ushort), #version 2020
        ('m_gameMajorVersion', ctypes.c_ubyte), #Game major version - "X.00"
        ('m_gameMinorVersion', ctypes.c_ubyte), #Game minor version - "1.XX"
        ('m_packetVersion', ctypes.c_ubyte), #Version of this packet type, all start from 1
        ('m_packetId', ctypes.c_ubyte), #Identifier for the packet type, see below
        ('m_sessionUID', ctypes.c_longlong), #Unique identifier for the session
        ('m_sessionTime', ctypes.c_float), #Session timestamp
        ('m_frameIdentifier', ctypes.c_uint), #Identifier for the frame the data was retrieved on
        ('m_playerCarIndex', ctypes.c_ubyte) #Index of player's car in the array
    ]
    

#MOTION PACKET
"""
The motion packet gives physics data for all the cars being driven.
There is additional data for the car being driven with the goal of being able to drive a motion platform setup.
N.B. For the normalised vectors below,
to convert to float values divide by 32767.0f – 16-bit signed values are used to pack the data and on the assumption that direction values are always between -1.0f and 1.0f.
Frequency: Rate as specified in menus
Size: 1464 bytes
"""
class CarMotionData(ctypes.LittleEndianStructure):
    """data structure for a single car motion data
    """
    _pack_ = 1
    _fields_ = [
        ('m_worldPositionX', ctypes.c_float), # World space X position
        ('m_worldPositionY', ctypes.c_float), # World space Y position
        ('m_worldPositionZ', ctypes.c_float), # World space Z position
        ('m_worldVelocityX', ctypes.c_float), # Velocity in world space X
        ('m_worldVelocityY', ctypes.c_float), # Velocity in world space Y
        ('m_worldVelocityZ', ctypes.c_float), # Velocity in world space Z
        ('m_worldForwardDirX', ctypes.c_ushort), # World space forward X direction (normalised)
        ('m_worldForwardDirY', ctypes.c_ushort), # World space forward Y direction (normalised)
        ('m_worldForwardDirZ', ctypes.c_ushort), # World space forward Z direction (normalised)
        ('m_worldRightDirX', ctypes.c_ushort), # World space right X direction (normalised)
        ('m_worldRightDirY', ctypes.c_ushort), # World space right Y direction (normalised)
        ('m_worldRightDirZ', ctypes.c_ushort), # World space right Z direction (normalised)
        ('m_gForceLateral', ctypes.c_float), # Lateral G-Force component
        ('m_gForceLongitudinal', ctypes.c_float), # Longitudinal G-Force component
        ('m_gForceVertical', ctypes.c_float), # Vertical G-Force component
        ('m_yaw', ctypes.c_float), # Yaw angle in radians
        ('m_pitch', ctypes.c_float), # Pitch angle in radians
        ('m_roll', ctypes.c_float) # Roll angle in radians
    ]

class PacketMotionData(ctypes.LittleEndianStructure):
    """data structure for all car motion
    """
    
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader), # Header
        ('m_carsmotiondata', CarMotionData * 22), # Data for all cars on track (22 in myteam session)
        ('m_suspensionPosition', ctypes.c_float * 4), # Note: All wheel arrays have the following order:
        ('m_suspensionVelocity', ctypes.c_float * 4), # RL, RR, FL, FR
        ('m_suspensionAcceleration', ctypes.c_float * 4), # RL, RR, FL, FR
        ('m_wheelSpeed', ctypes.c_float * 4), # Speed of each wheel
        ('m_wheelSlip', ctypes.c_float * 4), # Slip ratio for each wheel
        ('m_localVelocityX', ctypes.c_float), # Velocity in local space
        ('m_localVelocityY', ctypes.c_float), # Velocity in local space
        ('m_localVelocityZ', ctypes.c_float), # Velocity in local space
        ('m_angularVelocityX', ctypes.c_float), # Angular velocity x-component
        ('m_angularVelocityY', ctypes.c_float), # Angular velocity y-component
        ('m_angularVelocityZ', ctypes.c_float), # Angular velocity z-component
        ('m_angularAccelerationX', ctypes.c_float), # Angular velocity x-component
        ('m_angularAccelerationY', ctypes.c_float), # Angular velocity y-component
        ('m_angularAccelerationZ', ctypes.c_float), # Angular velocity z-component
        ('m_frontWheelsAngle', ctypes.c_float) # Current front wheels angle in radians
    ]


#SESSION PACKET
"""
The session packet includes details about the current session in progress.
Frequency: 2 per second
Size: 251 bytes
"""
class MarshalZone(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_zoneStart', ctypes.c_float), # Fraction (0..1) of way through the lap the marshal zone starts
        ('m_zoneFlag', ctypes.c_byte) # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
    ]

class WeatherForecastSample(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_sessionType', ctypes.c_ubyte), # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = TT
        ('m_timeOffset', ctypes.c_ubyte), # Time in minutes the forecast is for
        ('m_weather', ctypes.c_ubyte), # Weather - 0 = clear, 1 = light cloud, 2 = overcast 3 = light rain, 4 = heavy rain, 5 = storm
        ('m_trackTemperature', ctypes.c_ubyte), # Track temp. in degrees celsius
        ('m_airTemperature', ctypes.c_ubyte) # Air temp. in degrees celsius
    ]

class PacketSessionData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader) # Header
        ('m_weather', ctypes.c_ubyte), # Weather - 0 = clear, 1 = light cloud, 2 = overcast 3 = light rain, 4 = heavy rain, 5 = storm
        ('m_trackTemperature', ctypes.c_ubyte), #Track temp. in degrees celsius
        ('m_airTemperature', ctypes.c_ubyte), #Air temp. in degrees celsius
        ('m_totalLaps', ctypes.c_ubyte), # Total number of laps in this race
        ('m_trackLength', ctypes.c_ushort), # Track length in metres
        ('m_sessionType', ctypes.c_ubyte), # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = TT
        ('m_trackId', ctypes.c_byte), # -1 for unknown, 0-21 for tracks, see appendix
        ('m_formula', ctypes.c_ubyte), # Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2, 3 = F1 Generic
        ('m_sessionTimeLeft', ctypes.c_ushort), # Time left in session in seconds
        ('m_sessionDuration', ctypes.c_ushort), # Session duration in seconds
        ('m_pitSpeedLimit', ctypes.c_ubyte), # Pit speed limit in kilometres per hour
        ('m_gamePaused', ctypes.c_ubyte), # Whether the game is paused
        ('m_isSpectating', ctypes.c_ubyte), # Whether the player is spectating
        ('m_spectatorCarIndex', ctypes.c_ubyte), # Index of the car being spectated
        ('m_sliProNativeSupport', ctypes.c_ubyte), # SLI Pro support, 0 = inactive, 1 = active
        ('m_numMarshalZones', ctypes.c_ubyte), # Number of marshal zones to follow
        ('m_marshalZones', MarshalZone * 21), # List of marshal zones – max 21List of marshal zones – max 21
        ('m_safetyCarStatus', ctypes.c_ubyte), # 0 = no safety car, 1 = full safety car, 2 = virtual safety car
        ('m_networkGame', ctypes.c_ubyte), # 0 = offline, 1 = online
        ('m_numWeatherForecastSamples', ctypes.c_ubyte), # Number of weather samples to follow
        ('m_weatherForecastSamples', WeatherForecastSample * 20) # Array of weather forecast samples
    ]

#LAP DATA PACKET
"""
The lap data packet gives details of all the cars in the session.
Frequency: Rate as specified in menus
Size: 1190 bytes
"""

class LapData(ctypes.LittleEndianStructure):
    """lap data packet gives details of all the cars in the session
    """
    _pack_ = 1
    _fields_ = [
        ('m_lastLapTime', ctypes.c_float), # Last lap time in seconds
        ('m_currentLapTime', ctypes.c_float), # Current time around the lap in seconds
        ('m_sector1TimeInMS', ctypes.c_ushort), # Sector 1 time in milliseconds
        ('m_sector2TimeInMS', ctypes.c_ushort), # Sector 2 time in milliseconds
        ('m_bestLapTime', ctypes.c_float), # Best lap time of the session in seconds
        ('m_bestLapNum', ctypes.c_ubyte), # Lap number best time achieved on
        ('m_bestLapSector1TimeInMS', ctypes.c_ushort), # Sector 1 time of best lap in the session in milliseconds
        ('m_bestLapSector2TimeInMS', ctypes.c_ushort), # Sector 2 time of best lap in the session in milliseconds
        ('m_bestLapSector3TimeInMS', ctypes.c_ushort), # Sector 3 time of best lap in the session in milliseconds
        ('m_bestOverallSector1TimeInMS', ctypes.c_ushort), # Best overall sector 1 time of the session in milliseconds
        ('m_bestOverallSector1LapNum', ctypes.c_byte), # Lap number best overall sector 1 time achieved on
        ('m_bestOverallSector2TimeInMS', ctypes.c_ushort), # Best overall sector 2 time of the session in milliseconds
        ('m_bestOverallSector2LapNum', ctypes.c_byte), # Lap number best overall sector 2 time achieved on
        ('m_bestOverallSector3TimeInMS', ctypes.c_ushort), # Best overall sector 3 time of the session in milliseconds
        ('m_bestOverallSector3LapNum', ctypes.c_byte), # Lap number best overall sector 3 time achieved on
        ('m_lapDistance', ctypes.c_float), # Distance vehicle is around current lap in metres – could be negative if line hasn’t been crossed yet
        ('m_totalDistance', ctypes.c_float), # Total distance travelled in session in metres – could be negative if line hasn’t been crossed yet
        ('m_safetyCarDelta', ctypes.c_float), # Delta in seconds for safety car
        ('m_carPosition', ctypes.c_ubyte), # Car race position
        ('m_currentLapNum', ctypes.c_ubyte), # Current lap number
        ('m_pitStatus', ctypes.c_ubyte), # 0 = none, 1 = pitting, 2 = in pit area
        ('m_sector', ctypes.c_ubyte), # 0 = sector1, 1 = sector2, 2 = sector3
        ('m_currentLapInvalid', ctypes.c_ubyte), # Current lap invalid - 0 = valid, 1 = invalid
        ('m_penalties', ctypes.c_ubyte), # Accumulated time penalties in seconds to be added
        ('m_gridPosition', ctypes.c_ubyte), # Grid position the vehicle started the race in
        ('m_driverStatus', ctypes.c_ubyte), # Status of driver - 0 = in garage, 1 = flying lap, 2 = in lap 3 = out lap, 4 = on track
        ('m_resultStatus', ctypes.c_ubyte) # Result status - 0 = invalid, 1 = inactive, 2 = active, 3 = finished 4 = disqualified, 5 = not classified, 6 = retired
    ]

class PacketLapData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader), # Header
        ('m_lapData', LapData * 22) # Lap data for all cars on track
    ]


#EVENTE PACKET
"""This packet gives details of events that happen during the course of a session.
Frequency: When the event occurs
Size: 35 bytes

The event details packet is different for each type of event.
Make sure only the correct type is interpreted
"""

