#! python2.6
#!/usr/bin/env python
#coding:utf-8
# ver. 1.41109
# This module has been tested on python ver.2.6.6
# pySerial(http://pyserial.sourceforge.net/) is need to use.
# (C) 2014 Matsuda Hiroaki

class Paw():

    def __init__(self, serial, paw_id, c_1, c_2, c_3, c_4):

        self.serial = serial
        self.paw_id = paw_id

        self.c_1 = c_1
        self.c_2 = c_2
        self.c_3 = c_3
        self.c_4 = c_4

        self.ch_1_z0 = 0
        self.ch_2_z0 = 0
        self.ch_3_z0 = 0
        self.ch_4_z0 = 0


        init = self._read_data()
        
        self.ch_1_z0 = init[1]
        self.ch_2_z0 = init[2]
        self.ch_3_z0 = init[3]
        self.ch_4_z0 = init[4]

    def _read_data(self):
        
        while 1:
            head = [ord(self.serial.read(1))]
            
            if head[0] == 0xFA:
                head.append(ord(self.serial.read(1)))
                
                if head[1] == 0xAF:
                    receive = self.serial.read(9)
                    data = [ord(temp) for temp in receive]
                    
                    if data[0] == self.paw_id:
                        return self.convert_data( data )

    def convert_data(self, data):
        ch_1 = (( data[2] << 8) & 0xFF00 ) | (data[1] & 0xFF )
        ch_2 = (( data[4] << 8) & 0xFF00 ) | (data[3] & 0xFF )
        ch_3 = (( data[6] << 8) & 0xFF00 ) | (data[5] & 0xFF )
        ch_4 = (( data[8] << 8) & 0xFF00 ) | (data[7] & 0xFF )

        if ch_1 > 32767:
            ch_1 *= -1
            
        if ch_2 > 32767:
            ch_2 *= -1

        if ch_3 > 32767:
            ch_3 *= -1

        if ch_4 > 32767:
            ch_4 *= -1
        
        ch_1 = ch_1 * 3.300 / 4095.0 - self.ch_1_z0
        ch_2 = ch_2 * 3.300 / 4095.0 - self.ch_2_z0
        ch_3 = ch_3 * 3.300 / 4095.0 - self.ch_3_z0
        ch_4 = ch_4 * 3.300 / 4095.0 - self.ch_4_z0
        
        return data[0], ch_1, ch_2, ch_3, ch_4

    def get_dh(self):
        paw_id, ch_1, ch_2, ch_3, ch_4 = self._read_data()
        
        dh_ch_1 = self.c_1[0] * ch_1 ** 4 + self.c_1[1] * ch_1 ** 3 + self.c_1[2] * ch_1 ** 2 + self.c_1[3] * ch_1

        dh_ch_2 = self.c_2[0] * ch_2 ** 4 + self.c_2[1] * ch_2 ** 3 + self.c_2[2] * ch_2 ** 2 + self.c_2[3] * ch_2

        dh_ch_3 = self.c_3[0] * ch_3 ** 4 + self.c_3[1] * ch_3 ** 3 + self.c_3[2] * ch_3 ** 2 + self.c_3[3] * ch_3
 
        dh_ch_4 = self.c_4[0] * ch_4 ** 4 + self.c_4[1] * ch_4 ** 3 + self.c_4[2] * ch_4 ** 2 + self.c_4[3] * ch_4

        return paw_id, dh_ch_1, dh_ch_2, dh_ch_3, dh_ch_4

                
if __name__ == '__main__':

    import serial

    myserial = serial.Serial()
    myserial.port = 'COM5'
    myserial.baudrate = 115200
    myserial.parity = serial.PARITY_NONE
    myserial.open()
    
    import paw
       
    c_1 = [13.33, 23.33, 7.39, -8.80]
    c_2 = [10.73, 19.44, 9.92, -8.69]
    c_3 = [13.41, 24.02, 8.40, -8.33]
    c_4 = [21.34, 32.55, 7.59, -10.71]

    sensor = paw.Paw( myserial, 0, c_1, c_2, c_3, c_4 )

    while 1:

        paw_id, dh_ch_1, dh_ch_2, dh_ch_3, dh_ch_4 = sensor.get_dh()
        print( "ID:%d ch1:%d, ch2:%d, ch3:%d, ch4:%d" ) % ( paw_id, dh_ch_1, dh_ch_2, dh_ch_3, dh_ch_4 )

    
