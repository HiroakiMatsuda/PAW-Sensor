paw.py
======================
paw.py is parser of [PAW_Sensor Library][pawlib].
   
[PAW Sensor][mbed]: Please read this page about PAW Sensor and Library.

[pawlib]: http://developer.mbed.org/users/matsu/code/PAW_Sensor/   
[mbed]: http://developer.mbed.org/components/PAW-Snesor/  

Test Environment
------
Python:  
2.6.6  

[pySerial][serial]:  
2.6

[serial]: http://pyserial.sourceforge.net/index.html

OS:  
Windows 8.1 64bit

[PAW Sensor][paw]:  
Please get this sensor from [RT][store].

[paw]: http://www.rt-shop.jp/index.php?main_page=product_info&cPath=42&products_id=1303
[store]: http://www.rt-shop.jp/index.php?main_page=index&language=en



How to use
------
###1. Intall pySerial###
Please install [pySerial][serial].  

###2. Import PAW_Labrary on your mbed project###
Please import [PAW_Labrary][pawlib] on your mbed compiler.  
Then, you compile this project and write your mbed.

###3. Read PAW Sensor from mbed###
Please write code like below example.

```python  
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
```  
That's all! Good luck!

Licence
----------
Copyright &copy; 2014 Hiroaki Matsuda  
Licensed under the [Apache License, Version 2.0][Apache]  
Distributed under the [MIT License][mit].  
Dual licensed under the [MIT license][MIT] and [GPL license][GPL].  
 
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
[MIT]: http://www.opensource.org/licenses/mit-license.php
[GPL]: http://www.gnu.org/licenses/gpl.html