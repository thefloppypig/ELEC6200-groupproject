class SensorData:
    name = ""
    type = ""
    behaviour = ""
    data = []
    time = []

    def __init__(self, name, type, behaviour, data, time):
        self.name = name
        self.type = type
        self.behaviour = behaviour
        self.data = data
        self.time = time

    def insertItem(self, item):
        self.data.append(item)
