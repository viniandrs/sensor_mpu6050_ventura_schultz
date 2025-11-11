import time
import ustruct
from machine import Pin, I2C

# Configuração dos botões da BitDogLab V7
botao_a = Pin(10, Pin.IN, Pin.PULL_UP)  # Botão A - GPIO10
# Botão B (GPIO5) e C (GPIO6) também disponíveis

# Configuração I2C para MPU-6050
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

# Endereço do MPU-6050
MPU6050_ADDR = 0x68

# Registradores do MPU-6050
PWR_MGMT_1 = 0x6B
ACCEL_XOUT = 0x3B
GYRO_XOUT = 0x43

def init_mpu6050():
    """Inicializa o sensor MPU-6050"""
    try:
        # Acorda o sensor MPU-6050
        i2c.writeto_mem(MPU6050_ADDR, PWR_MGMT_1, b'\x00')
        time.sleep(0.1)
        print("MPU-6050 inicializado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao inicializar MPU-6050: {e}")
        return False

def read_sensor_data(start_time) -> dict[str, float] | None:
    """Lê os dados do acelerômetro e giroscópio"""
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
            'timestamp': time.ticks_diff(time.ticks_ms(), start_time),
            'accel_x': accel_x_g,
            'accel_y': accel_y_g,
            'accel_z': accel_z_g,
            'gyro_x': gyro_x_dps,
            'gyro_y': gyro_y_dps,
            'gyro_z': gyro_z_dps,
            'temperature': temp_c
        }
    except Exception as e:
        print(f"Erro ao ler sensor: {e}")
        return None

def collect_data_for_1s():
    """Coleta dados por 1 segundo"""
    print("Iniciando coleta de dados por 1 segundo...")
    data_points = []
    start_time = time.ticks_ms()
    
    while time.ticks_diff(time.ticks_ms(), start_time) < 1000:  # 1 segundo
        data = read_sensor_data(start_time)
        if data:
            data_points.append(data)
        time.sleep_ms(10)  # Amostragem a cada 10ms (~100Hz)

    print(f"Coleta concluída! {len(data_points)} amostras coletadas.")
    print("Ultimas 10 amostras:")
    for dp in data_points[-10:]:
        print(dp)
    return data_points

def save_to_csv(data_points):
    """Salva os dados em arquivo CSV"""
    filename = "mpu6050_data.csv"
    
    try:
        with open(filename, 'w') as f:
            # Cabeçalho do CSV
            f.write("timestamp_ms,accel_x_g,accel_y_g,accel_z_g,gyro_x_dps,gyro_y_dps,gyro_z_dps,temperature_c\n")
            
            # Dados
            for data in data_points:
                f.write(f"{data['timestamp']},{data['accel_x']:.4f},{data['accel_y']:.4f},{data['accel_z']:.4f},")
                f.write(f"{data['gyro_x']:.4f},{data['gyro_y']:.4f},{data['gyro_z']:.4f},{data['temperature']:.2f}\n")
        
        print(f"{len(data_points)} amostras salvas em '{filename}'")
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return False

def main():
    """Função principal"""
    print("=== BitDogLab V7 - MPU-6050 Data Logger ===")
    print("Conecte o MPU-6050: SCL->GP1, SDA->GP0, VCC->3.3V, GND->GND")
    print("Pressione o Botao A para iniciar a coleta de dados")
    
    # Inicializa o sensor
    if not init_mpu6050():
        print("Nao foi possível inicializar o MPU-6050. Verifique as conexoes.")
        return
    
    last_button_state = botao_a.value()
    
    while True:
        current_button_state = botao_a.value()
        
        # Detecta borda de descida (botão pressionado)
        if last_button_state == 1 and current_button_state == 0:
            print("\nBotao A pressionado!")
            
            # Coleta dados por 1 segundo
            data_points = collect_data_for_1s()
            
            # Salva em arquivo CSV
            if data_points:
                save_to_csv(data_points)
                print("Pronto! Pressione Botao A novamente para nova coleta.")
            else:
                print("Erro: Nenhum dado foi coletado.")
        
        last_button_state = current_button_state
        time.sleep(0.05)  # Pequena pausa para debounce

# Executa o programa
if __name__ == "__main__":
    main()