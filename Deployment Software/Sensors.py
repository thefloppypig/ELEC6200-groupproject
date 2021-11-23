
from subprocess import check_output
from message import sendmsg # imports sms module
from ISStreamer.Streamer import Streamer

def initialiseSensors():
	#imports in the function will prevent errors
	import board
	import busio
	import adafruit_adxl34x
	import adafruit_tsl2591
	import adafruit_tca9548a
	import adafruit_bme280
	from bmp280 import BMP280
	print("Starting Sensor Program")

	baseline_values = []
	baseline_size = 500

	print("Initiate I2C")
	#initiate I2C
	i2c=busio.I2C(board.SCL, board.SDA)
	#MUX
	try:
		tca=adafruit_tca9548a.TCA9548A(i2c)
	except 	ValueError:
		sendmsg(alert=1,message='I2C')
		print('I2C not detected')
	#LUX1
	try:
		tsl1=adafruit_tsl2591.TSL2591(tca[0])
	except 	ValueError:
		sendmsg(alert=1,message='LUX sensor 1')
		print('LUX1 not detected')
	
	#LUX2
	try:
		tsl2=adafruit_tsl2591.TSL2591(tca[2])
	except 	ValueError:
		sendmsg(alert=1,message='LUX sensor 2')
		print('LUX2 not detected')
	#Accelerometer
	try:
		acc=adafruit_adxl34x.ADXL345(tca[1])
	except 	ValueError:
		sendmsg(alert=1,message='Accelerometer')
		print('ACC not detected')
	#BME280
	try:
		bme280 = adafruit_bme280.Adafruit_BME280_I2C(tca[3])
	except 	ValueError:
		sendmsg(alert=1,message='BME280')
		print('BME280 not detected')

	print("BMP280")
	#BMP280
	try:
	    from smbus2 import SMBus
	except ImportError:
	    from smbus import SMBus
	bus = SMBus(2)
	bmp280 = BMP280(i2c_dev=bus)

	#BME280 sealevel assign
	adafruit_bme280.sea_level_pressure = 1013.25

	print("Setting Altitude")
	#setting altitude baseline
	print(baseline_size)
	for i in range(baseline_size):
	    pressure = bmp280.get_pressure()
	    baseline_values.append(pressure)
	    #time.sleep(0.2)
	    #print(i)
	print("Sensors Initialised")
	return bme280, i2c, tsl1, acc

def pollSensors(bme280, i2c, tsl1, acc):
	sensorData = {}
	#wait for
	#about 0.35sec refresh rate when sleep is 0.07 (because 5 sensors)

	#BMP280
	# temperature = bmp280.get_temperature()
	# pressure = bmp280.get_pressure()
	# baseline = sum(baseline_values[:-30]) / len(baseline_values[:-30])#Average of baseline
	# altitude = bmp280.get_altitude(qnh=baseline)#altitude function in library
	# print("TempBMP: {0}lux".format(temperature))
	# print("PressBMP: {0}".format(pressure))
	#print("Altitude: {0}".format(altitude))

	#Light sensor 2
	# lux2 = tsl2.lux
	# infrared2 = tsl2.infrared
	# visible2 = tsl2.visible
	# full_spectrum2 = tsl2.full_spectrum

	#Light sensor 1
	lux1 = tsl1.lux
	infrared1 = tsl1.infrared
	visible1 = tsl1.visible
	full_spectrum1 = tsl1.full_spectrum

	sensorData['Lux'] = lux1
	sensorData['Infrared'] = infrared1
	sensorData['Visible'] = visible1
	sensorData['Full_Spectrum'] = full_spectrum1

	#print("1. Total light: {0}lux".format(lux1))
	#print("1. Infrared light: {0}".format(infrared1))
	#print("1. Visible light: {0}".format(visible1))
	#print("1. Full spectrum (IR + visible) light: {0}".format(full_spectrum1))

	#Accelerometer
	(x, y, z)=acc.acceleration
	sensorData['Accelerometer_x_axis'] = x
	sensorData['Accelerometer_y_axis'] = y
	sensorData['Accelerometer_z_axis'] = z
	#print("X: {0}".format(x))
	#print("Y: {0}".format(y))
	#print("Z: {0}".format(z))

	#BME280
	BME_temperature = bme280.temperature
	BME_humidity = bme280.humidity
	BME_pressure = bme280.pressure
	sensorData['Temperature'] = BME_temperature
	sensorData['Humidity'] = BME_humidity
	sensorData['Pressure'] = BME_pressure

	#Core Usage
	data = check_output("./coreUsageTest.sh")
	#print("data: ", data)
	data = str(data)
	data = data[2:]
	data = data[:-3]
	data = data.replace(" ", "")
	#print("data: ", data)

	datachunk = data.split(',')

	allCores = float(datachunk[0])
	allCores = allCores + float(datachunk[1])
	allCores = allCores + float(datachunk[2])
	allCores = allCores + float(datachunk[3])
	allCores = allCores/4
	sensorData['All_Cores'] = allCores
	return sensorData
