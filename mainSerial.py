import serial
import struct
import matplotlib.pyplot as plt
import numpy as np

porta = 'COM5'
#velocidade = 38400
#velocidade = 115200
#velocidade = 1850000
velocidade = 460800

bitvoltlow = 152e-6
bitvolthigh = 0.01
#bitvolthigh = 305e-6

conexao = serial.Serial(porta, velocidade)

mododeexecucao = 1 # 1 chama 0 espera a FAI 2 enter comand 3 Event report

if mododeexecucao == 1:
    opcao = "get.data"
    conexao.write(opcao.encode('ASCII'))
    conexao.write("\n".encode('ASCII'))
    leitura_serial = conexao.readline()
    print('Leitura: ', leitura_serial)
elif mododeexecucao == 2:
    leitura_serial = b'Comand not vailed\n'
    while leitura_serial == b'Comand not vailed\n':
        opcao = input("Enter comand:")
        conexao.write(opcao.encode('ASCII'))
        conexao.write("\n".encode('ASCII'))
        leitura_serial = conexao.readline()
        print('Leitura: ', leitura_serial)
elif mododeexecucao == 3:
    opcao = "Event report"
    conexao.write(opcao.encode('ASCII'))
    conexao.write("\n".encode('ASCII'))
    leitura_serial = conexao.readline()
    print('Leitura: ', leitura_serial)
    leitura_serial = conexao.readline()
    print('Leitura: ', leitura_serial)
else:
    opcao = "reset FAI"
    conexao.write(opcao.encode('ASCII'))
    conexao.write("\n".encode('ASCII'))
    leitura_serial = conexao.readline()
    print('Leitura: ', leitura_serial)
    leitura_serial = conexao.readline()
    print('Leitura: ', leitura_serial)

leitura_serial = conexao.readline()
datalength = int(leitura_serial)
print('data length: ', datalength)

leitura_serial = conexao.readline()
rangeADC = int(leitura_serial)
print('Range: ', rangeADC)

leitura_serial = conexao.readline()
ch_length = int(leitura_serial)
print('Channels number: ', ch_length)

rtcrtp = []
for i in range(0, 16, 1):
    leitura_serial = conexao.readline()
    rtcrtp.append(int(leitura_serial))
    print('rtcrtp: ', rtcrtp[i])

atpajuste = []
for i in range(0, 16, 1):
    leitura_serial = conexao.readline()
    atpajuste.append(int(leitura_serial)/1000)
    print('rtcrtp: ', atpajuste[i])

dados = []
j = 0
channels = ch_length
while ch_length > 0:
    leitura_serial = list(conexao.read(2*datalength))
    info = [leitura_serial[i:i + 2] for i in range(0, len(leitura_serial) - 1, 2)]
    dados.append(info)
    ch_length -= 1
    j += 1

leitura = conexao.readline()
print(leitura)



saida=[]
b=[]
'''
arquivo0 = open('Va.txt', 'w')
arquivo1 = open('Vb.txt', 'w')
arquivo2 = open('Vc.txt', 'w')
arquivo3 = open('Ia.txt', 'w')
arquivo4 = open('Ib.txt', 'w')
arquivo5 = open('Ic.txt', 'w')
arquivo6 = open('In.txt', 'w')
arquivo7 = open('In1.txt', 'w')
'''
for j in range(0, channels):
    aa = dados[j]
#    arquivo.write("\n%d\n" % j)
    print(aa)
    for i in range(0, len(info), 1):
        c = struct.unpack_from('>h', bytes(aa[i]))
        if rangeADC == 10:
            e = rtcrtp[j] * bitvolthigh * np.array(c) / atpajuste[j]
        else:
            e = rtcrtp[j] * bitvoltlow * np.array(c) / atpajuste[j]
        '''
        if j == 0:
            arquivo0.write(str(e))
            arquivo0.write("\n")
        if j == 1:
            arquivo1.write(str(e))
            arquivo1.write("\n")
        if j == 2:
            arquivo2.write(str(e))
            arquivo2.write("\n")
        if j == 3:
            arquivo3.write(str(e))
            arquivo3.write("\n")
        if j == 4:
            arquivo4.write(str(e))
            arquivo4.write("\n")
        if j == 5:
            arquivo5.write(str(e))
            arquivo5.write("\n")
        if j == 6:
            arquivo6.write(str(e))
            arquivo6.write("\n")
        if j == 7:
            arquivo7.write(str(e))
            arquivo7.write("\n")
        '''
        b.append(e)
#    arquivo.write("\n")
    saida.append(b)
    b=[]

'''
arquivo0.close()
arquivo1.close()
arquivo2.close()
arquivo3.close()
arquivo4.close()
arquivo5.close()
arquivo6.close()
arquivo7.close()
'''
plt.figure(1)
plt.plot(saida[0])
plt.plot(saida[1])
plt.plot(saida[2])
plt.figure(2)
plt.plot(saida[3])
plt.plot(saida[4])
plt.plot(saida[5])
plt.figure(3)
plt.plot(saida[6])
plt.plot(saida[7])
plt.plot(saida[8])
plt.show()

conexao.close()




