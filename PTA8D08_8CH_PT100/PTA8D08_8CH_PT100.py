from pymodbus.client.sync import ModbusSerialClient
import time


class PTA8D08_8CH_PT100:
    def __init__(
        self, com_port, data_bits=8, stop_bits=1, parity="N", unit_id=1, baud_rate=9600
    ):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.data_bits = data_bits
        self.stop_bits = stop_bits
        self.parity = parity
        self.unit_id = unit_id
        self.client = ModbusSerialClient(
            method="rtu",
            port=self.com_port,
            baudrate=self.baud_rate,
            bytesize=self.data_bits,
            stopbits=self.stop_bits,
            parity=self.parity,
            timeout=0.2,
        )
        # REGISTERS
        self.register_temperature = [0, 1, 2, 3, 4, 5, 6, 7]
        self.register_resistance = [32, 33, 34, 35, 36, 37, 38, 39]

        self.register_temperature_correction = [64, 65, 66, 67, 68, 69, 70, 71]
        self.register_resistance_correction = [96, 97, 98, 99, 100, 101, 102, 103]

        self.register_reset = 251
        self.reset_command = [0xFF, 0x06, 0x00, 0xFB, 0x00, 0x00, 0xED, 0xE5]

        self.debug = False

    def set_debug(self, value=True):
        self.debug = value

    def connect(self):
        if not self.client.connect():
            print("Unable to connect to device.")

    def disconnect(self):
        self.client.close()

    def read_all_temperatures(self):
        result_array = {}
        try:
            for i in self.register_temperature:
                response = self.client.read_holding_registers(i, 1, unit=self.unit_id)
                if response.isError():
                    if self.debug:
                        print(f"Error reading registers at address {i}: {response}")
                else:
                    data = float(response.registers[0]) / 10
                    result_array[i] = data
                    if self.debug:
                        print(f"Read temperature from address {i}: {data} °C.")
                time.sleep(0.2)
            return result_array
        except Exception as e:
            print(f"Error: {e}")

    def read_all_resistances(self):
        result_array = {}
        try:
            for i in self.register_resistance:
                response = self.client.read_holding_registers(i, 1, unit=self.unit_id)
                if response.isError():
                    if self.debug:
                        print(f"Error reading registers at address {i}: {response}")
                else:
                    data = float(response.registers[0]) / 10
                    result_array[i] = data
                    if self.debug:
                        print(f"Read resistance from address {i}: {data} ohm.")
                time.sleep(0.2)
            return result_array
        except Exception as e:
            print(f"Error: {e}")

    def get_temeperature(self, ch=0):
        response = self.client.read_holding_registers(
            self.register_temperature[ch], 1, unit=self.unit_id
        )
        if response.isError():
            if self.debug:
                print(
                    f"Error reading registers at address {self.register_temperature[ch]}: {response}"
                )
        else:
            data = float(response.registers[0]) / 10
            if self.debug:
                print(
                    f"Read temperature from address {self.register_temperature[ch]}: {data} °C."
                )
        return data

    def get_resistance(self, ch=0):
        response = self.client.read_holding_registers(
            self.register_resistance[ch], 1, unit=self.unit_id
        )
        if response.isError():
            if self.debug:
                print(
                    f"Error reading registers at address {self.register_temperature[ch]}: {response}"
                )
        else:
            data = float(response.registers[0]) / 10
            if self.debug:
                print(
                    f"Read resistance from address {self.register_temperature[ch]}: {data} ohm."
                )
        return data

    def set_temperature_correction(self, ch=0, temperature=0):
        temp_convert = temperature * 10
        if temp_convert >= 0 and temp_convert <= 65535:
            self.client.write_registers(
                self.register_temperature_correction[ch],
                temp_convert,
                unit=self.unit_id,
            )
        else:
            if self.debug:
                print("Temperature out of range")

    def set_resistance_correction(self, ch=0, resistance=0):
        res_convert = resistance * 10
        if res_convert >= 0 and res_convert <= 65535:
            self.client.write_registers(
                self.register_resistance_correction[ch],
                res_convert,
                unit=self.unit_id,
            )
        else:
            if self.debug:
                print("Resistance out of range")

    def factory_reset(self):
        for i in self.reset_command:
            self.client.write_registers(self.register_reset, i, unit=self.unit_id)
