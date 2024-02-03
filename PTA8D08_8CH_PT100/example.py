from PTA8D08_8CH_PT100 import PTA8D08_8CH_PT100

# PT1 = CH0
# PT2 = CH1
# PT3 = CH2
# PT4 = CH3
# PT5 = CH4
# PT6 = CH5
# PT7 = CH6
# PT8 = CH7


dev1 = PTA8D08_8CH_PT100("COM17")
dev1.connect()

# TEMPERATURES
temperatures = dev1.read_all_temperatures()
print(temperatures)
# RESISTANCES
# reistance = dev1.read_all_resistances()
# print(reistance)

# PT1 = CH0 -> TEMPERATURE
# channel_1_temperature = dev1.get_temeperature(ch=0)
# print(channel_1_temperature)

# # PT1 = CH0 -> RESISTANCE
# channel_1_get_resistance = dev1.get_resistance(ch=0)
# print(channel_1_get_resistance)

# RESET TO DEFAULT
# dev1.factory_reset()

dev1.disconnect()
