from networktables import NetworkTable


class VisionTable:
    def __init__(self):
        print "Initializing NetworkTables..."
        NetworkTable.setClientMode()
        NetworkTable.setIPAddress("roborio-4761-frc.local")
        NetworkTable.initialize()
        self.table = NetworkTable.getTable("vision")
        print "NetworkTables initialized!"

    def write_dict(self, data):
        if not self.table.isConnected():
            print "Not connected to a NetworkTables server (nothing will actually be written)"
        for key in data.keys():
            self.table.putValue(key, data[key])

vision_table = VisionTable()