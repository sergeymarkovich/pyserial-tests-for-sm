import serial
import time

# функция для подключения к маршрутизатору через последовательный порт
def connect_to_router(port, baudrate):
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = baudrate
    ser.timeout = 1
    ser.open()
    return ser

# функция для отправки команды в консоль маршрутизатора
def send_command(ser, command):
    ser.write(command.encode('utf-8'))
    # time.sleep(1)
    output = ser.read_all().decode('utf-8')
    print(output)
    return output

# функция для входа в консоль BMC
def enter_bmc(ser):
    while True:
        line = ser.readline().decode('utf-8')
        if 'Hit any key to stop autoboot' in line:
            ser.write(b'\x1b[B\n')
            time.sleep(1)
            ser.write(b'\x1b[B\n')
            time.sleep(1)
            ser.write(b'\x1b[B\n')
            time.sleep(1)
            ser.write(b'\r')
            time.sleep(1)
            break

# функция для отправки списка команд и сохранения вывода в файл
def send_commands(ser, commands):
    output = ''
    for command in commands:
        send_command(ser, command)
        while True:
            line = ser.readline().decode('utf-8')
            output += line
            print(line.strip())
            if '#' in line:
                break
            if 'Serial number:' in line:
                serial_number = line.split()[2]
    output_filename = 'output/' + serial_number + '_output.txt'
    with open(output_filename, 'w') as f:
        f.write(output)
    return serial_number

# функция для парсинга данных из output.txt файла и внесения ошибок в файл error.txt
def parse_output(output_filename, error_filename):
    error_count = 0
    input_str = ''
    with open(output_filename, 'r') as f:
        output = f.read()

    if 'BMC firmware version: 1.6' not in output:
        input_str += 'ERROR: version bmc not 1.6\n'
        error_count += 1
    if 'Fan is broken or not connected' in output:
        input_str += 'ERROR: fan tacho\n'
        error_count += 1    
    if 'ACK failed' in output:
        input_str += 'ERROR: i2c\n'
        error_count += 1
    if not(('U-Boot build: 1.2.1' in output) or ('U-Boot build: 1.2.2' in output)):
        input_str += 'ERROR: u-boot version not 1.2.1 or 1.2.2\n'
        error_count += 1
    if '2 USB Device' not in output:
        input_str += 'ERROR: usb\n'
        error_count += 1
    if 'nanoSSD 3ME3' not in output:
        input_str += 'ERROR: sata\n'
        error_count += 1
    if 'full duplex' not in output:
        input_str += 'ERROR: dhcp\n'
        error_count += 1

    if error_count == 0:
        input_str = '0 errors'
    else:
        input_str += '\nTotally ' + str(error_count) + ' ERRORS'
    
    with open(error_filename, 'w') as f:
        f.write(input_str)


def main():
    port = '/dev/ttyUSB0'  
    baudrate = 115200 
    ser = connect_to_router(port, baudrate)
    enter_bmc(ser)
    with open('input.txt') as f:
        commands = f.readlines()
    serial_number = send_commands(ser, commands)
    output_filename = 'output/' + serial_number + '_output.txt'
    error_filename = 'output/' + serial_number + '_error.txt'
    ser.close()
    parse_output(output_filename, error_filename)

if __name__ == '__main__':
    main()
