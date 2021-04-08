from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate

led_light = bytes(0x00)
ID = 0


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr) 
        elif isNewData:
            print ("Received new data from", dev.addr)
    def handleNotification(self, cHandle, data):
        global ID
        ID = data


scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(3.0)
n = 0
for dev in devices:
    print(n, ": Device ",dev.addr, "(", dev.addrType, ")", ", RSSI= ", dev.rssi, " dB" )
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print(desc, "=", value)
number = input('Enter your device number: ')
print('Device', number)
print(list(devices)[int(number)].addr)
print("Connecting...")
dev = Peripheral(list(devices)[int(number)].addr, 'random')
dev.withDelegate(ScanDelegate())
print("Services...")
for svc in dev.services:
    print(str(svc))
try:
    testService = dev.getServiceByUUID(UUID(0xa000))
    for ch in testService.getCharacteristics():
        print(str(ch))
    testService = dev.getServiceByUUID(UUID(0xb000))
    for ch in testService.getCharacteristics():
        print(str(ch))
    but_ch = dev.getCharacteristics(uuid=UUID(0xa001))[0]
    cccd = but_ch.getHandle() + 1
    dev.writeCharacteristic(cccd, bytes([0x01, 0x00]))
    if (but_ch.supportsRead()):
        print(but_ch.read())
    led_ch = dev.getCharacteristics(uuid=UUID(0xb001))[0]
    if (led_ch.supportsRead()):
        print(led_ch.read())
        led_light = led_ch.read()
    while True:
        if(dev.waitForNotifications(1.0)):
            print(ID)
            ID = int.from_bytes(ID, byteorder='little')
            print(hex(ID))
            if(ID != 0):
                led_light = bytes([0x01])
            else:
                led_light = bytes([0x00])
            led_ch.write(led_light)
            continue
        print("Wait for notification")   
finally:
    dev.disconnect() 
