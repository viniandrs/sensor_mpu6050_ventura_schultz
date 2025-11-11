import time
import ustruct
from machine import Pin, I2C
import ssd1306

# Configuração I2C para MPU-6050 e OLED
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
i2c_oled = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)

# Configuração do display OLED (128x64)
def try_init_oled():
    global oled_connected, oled, width, height
    i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)  # BitDogLab v7
    try:
        import ssd1306 as ssd1306 
        oled = ssd1306.SSD1306_I2C(128, 64, i2c_oled, addr=0x3C)
        width, height = 128, 64
        oled_connected = True
        print("OLED successfully detected")
        return
    except Exception as e:
        print("SSD1306 error: ", e)

try_init_oled()

# Endereço do MPU-6050
MPU6050_ADDR = 0x68

# Registradores do MPU-6050
PWR_MGMT_1 = 0x6B
ACCEL_XOUT = 0x3B
GYRO_XOUT = 0x43
WHO_AM_I = 0x75

def init_mpu6050():
    """Inicializa e verifica o MPU-6050"""
    try:
        # Verifica se o sensor responde
        whoami = i2c.readfrom_mem(MPU6050_ADDR, WHO_AM_I, 1)[0]
        # if whoami != 0x68:
        #     return False, f"WHO_AM_I incorreto: {whoami:#04x}"
        
        # Acorda o sensor MPU-6050
        i2c.writeto_mem(MPU6050_ADDR, PWR_MGMT_1, b'\x00')
        time.sleep(0.1)
        return True, "MPU-6050 OK"
    except Exception as e:
        return False, f"Erro: {e}"

def read_sensor_data():
    """Lê os dados do acelerometro e giroscopio com verificação de erro"""
    try:
        # Lê 14 bytes (acelerômetro + temperatura + giroscópio)
        data = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_XOUT, 14)
        
        # Converte os dados (cada valor é 16-bit signed)
        accel_x = ustruct.unpack('>h', data[0:2])[0]
        accel_y = ustruct.unpack('>h', data[2:4])[0]
        accel_z = ustruct.unpack('>h', data[4:6])[0]
        temp = ustruct.unpack('>h', data[6:8])[0]
        gyro_x = ustruct.unpack('>h', data[8:10])[0]
        gyro_y = ustruct.unpack('>h', data[10:12])[0]
        gyro_z = ustruct.unpack('>h', data[12:14])[0]
        
        # Verifica se os valores estão dentro de limites razoáveis
        errors = []
        
        # Verifica acelerômetro (±2g = ±32768/2 = ±16384)
        accel_limits = 20000
        if abs(accel_x) > accel_limits:
            errors.append("ACCEL_X")
        if abs(accel_y) > accel_limits:
            errors.append("ACCEL_Y") 
        if abs(accel_z) > accel_limits:
            errors.append("ACCEL_Z")
            
        # Verifica giroscópio (±250°/s = ±32768/250 = ±131)
        gyro_limits = 30000
        if abs(gyro_x) > gyro_limits:
            errors.append("GYRO_X")
        if abs(gyro_y) > gyro_limits:
            errors.append("GYRO_Y")
        if abs(gyro_z) > gyro_limits:
            errors.append("GYRO_Z")
        
        # Converte para unidades físicas
        accel_scale = 16384.0  # para ±2g
        gyro_scale = 131.0     # para ±250°/s
        temp_c = (temp / 340.0) + 36.53
        
        accel_x_g = accel_x / accel_scale
        accel_y_g = accel_y / accel_scale
        accel_z_g = accel_z / accel_scale
        
        gyro_x_dps = gyro_x / gyro_scale
        gyro_y_dps = gyro_y / gyro_scale
        gyro_z_dps = gyro_z / gyro_scale
        
        return {
            'accel_x': accel_x_g,
            'accel_y': accel_y_g,
            'accel_z': accel_z_g,
            'gyro_x': gyro_x_dps,
            'gyro_y': gyro_y_dps,
            'gyro_z': gyro_z_dps,
            'temperature': temp_c,
            'errors': errors,
            'raw_valid': True
        }
    except Exception as e:
        return {
            'accel_x': 0, 'accel_y': 0, 'accel_z': 0,
            'gyro_x': 0, 'gyro_y': 0, 'gyro_z': 0,
            'temperature': 0,
            'errors': ["LEITURA"],
            'raw_valid': False
        }

def update_display(data):
    """Atualiza o display OLED com os dados do sensor"""
        
    oled.fill(0)  # Limpa o display
    
    # Cabeçalho
    oled.text("MPU6050 Test", 0, 0)
    
    # Acelerômetro
    if "ACCEL" in str(data['errors']):
        oled.text("ACCEL: ERRO!", 0, 10)
    else:
        # print it single line for better fit
        oled.text(f"A:({data['accel_x']:5.2f},{data['accel_y']:5.2f},", 0, 10)
        oled.text(f"{data['accel_z']:5.2f})", 0, 20)
    
    # Giroscópio
    if "GYRO" in str(data['errors']):
        oled.text("GYRO: ERRO!", 0, 30)
    else:
        # print gyroscope in the next line for better fit
        oled.text(f"G:({data['gyro_x']:6.1f},{data['gyro_y']:6.1f},", 0, 30)
        oled.text(f"{data['gyro_z']:6.1f})", 0, 40)
        pass
    
    # Temperatura
    oled.text(f"Temp: {data['temperature']:4.1f}C", 0, 50)
    
    oled.show()

def print_serial(data):
    """Imprime dados no monitor serial"""
    print("\n" + "="*50)
    print("BitDogLab V7 - Teste MPU-6050")
    print("-"*50)
    
    if data['errors']:
        print(f"ERROS: {data['errors']}")

    print("Acelerometro (g):")
    if "ACCEL" in str(data['errors']):
        print("  X: ERRO | Y: ERRO | Z: ERRO")
    else:
        print(f"  X: {data['accel_x']:7.3f} | Y: {data['accel_y']:7.3f} | Z: {data['accel_z']:7.3f}")
    
    print("Giroscopio (graus/s):")
    if "GYRO" in str(data['errors']):
        print("  X: ERRO | Y: ERRO | Z: ERRO")
    else:
        print(f"  X: {data['gyro_x']:7.1f} | Y: {data['gyro_y']:7.1f} | Z: {data['gyro_z']:7.1f}")
    
    print(f"Temperatura: {data['temperature']:5.1f} C")
    print("="*50)

def main():
    """Função principal do teste"""
    print("=== BitDogLab V7 - Teste MPU-6050 ===")
    
    # Inicializa o sensor
    sensor_ok, sensor_status = init_mpu6050()
    
    if not sensor_ok:
        print(f"Falha na inicializacao: {sensor_status}")
        if oled_connected:
            oled.fill(0)
            oled.text("MPU-6050 ERRO", 0, 0)
            oled.text(sensor_status, 0, 20)
            oled.text("Verifique conexoes", 0, 40)
            oled.show()
        return
    
    print("Sensor inicializado. Iniciando leitura...")
    
    # Loop principal de leitura
    read_count = 0
    error_count = 0
    
    while True:
        # Lê dados do sensor
        data = read_sensor_data()
        read_count += 1
        
        if data['errors']:
            error_count += 1
        
        update_display(data)
        
        # Imprime no serial (a cada 10 leituras para não sobrecarregar)
        if read_count % 10 == 0:
            print_serial(data)
        
        time.sleep(0.1)  # 10Hz de atualização

# Executa o programa
if __name__ == "__main__":
    main()