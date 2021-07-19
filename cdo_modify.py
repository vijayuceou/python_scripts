import os

xil_out32 = "Xil_Out32("

def open_data_file(file_name='demo.txt'):
    file_obj = open(file_name, 'r')
    data_list = file_obj.read().strip().split('\n')
    return data_list


def grep_data(address, path='config/*'):
    print (address, path)
    return os.popen('grep "{}" {}'.format(address, path)).read()


def parse_data(data_list):
    file_obj = open('demo_output.txt', 'w')
    for data in data_list:
        data = data.split(' ')[1:]
        data1, data2 = bitwise_and(data[0].upper().replace('X', 'x'))
        result = grep_data(data1)
        data1 = "( ( " +result.split('#define ')[1].split(' ')[0].strip() + " )"
        final_str =   data1 + ' + ' + data2
        result = grep_data(final_str)
        data1 = " " + result.split('#define ')[1].split(' ')[0].strip()
        final_str = xil_out32 + data1 + ',' + data[1] + ');\n'
        file_obj.write(final_str)
    file_obj.close()


def bitwise_and(data):
    data1 = hex(int(data, 16) & int('0xFFFF0000', 16)).upper().replace('X', 'x')
    data2 = hex(int(data, 16) & int('0x0000FFFF', 16)).upper().replace('X', 'x')
    if len(data2) < 10:
        data2 = '0x' + ('0' * (10 - len(data2))) + data2.replace('0x', '')
    if len(data1) < 10:
        data1 = data1 + ( '0' * (10 - len(data1)))
    return data1, data2


data = open_data_file()
parse_data(data)
