# Object with sensor propperties and readings
class SensorData:
    name = "" # Name of the sensor? <- I think they also use type here by the way this object is created
    type = "" # Accelerometer_x_axis, Accelerometer_y_axis, Accelerometer_z_axis, Temperature, Humidity, Pressure, Altitude, All_Cores, Core 0, Core 1, Core 2, Core 3, Lux, Infrared, Visible, Full_Spectrum
    behaviour = "" # FreezerAttack, HeatAttack, OpenLidAttack, DrillAttack or Normal
    data = [] # Sensor reading data
    time = [] # Time at sensor reading data

    def __init__(self, name, type, behaviour, data, time):
        self.name = name
        self.type = type
        self.behaviour = behaviour
        self.data = data
        self.time = time

    def insertItem(self, item):
        self.data.append(item)
