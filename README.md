# PyT1000
Python scriptable serial analyzer VT100 compatible

## Command line

Call _py pyT1000.py_ followed by arguments

### List available ports

arg : _-list_

result : 
```
 ['COM3', 'COM4', 'COM12']
```

### Serial port parameters

#### Port

arg: _-p_

exemple : 
```
 -p COM12
```

#### Baudrate

arg: _-baud_

default value : 115200

exemple : 
```
 -baud 115200
```

#### Parity

arg: _-par_

values : 
* NONE : no parity (dafault)
* ODD : odd parity
* EVEN : even parity


exemple : 
```
 -par ODD
```

#### Stop bits

arg: _-stp_

values : 
* STP1 : 1 stop bit ( default )
* STP1_5 : 1.5 stop bits
* STP2 : 2 stop bits

exemple : 
```
 -stp STP1_5
```
