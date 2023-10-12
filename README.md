# PyT1000
Python scriptable serial analyzer VT100 compatible


## Display mode

### Log mode

In this mode, RX/TX data are timestamped an displayed without any interpretation

#### HEX mode

Data are displayed in hexadecimal

#### Ascii mode

Data are displayedas text

### VT100 mode

Display is launched as a VT100 terminal

## Command line

Call _py pyT1000.py_ followed by arguments

### Mode

Default is log mode in hexadecimal format

#### ASCII log mode

arg : _-ascii_

#### VT100 mode

arg : _-vt100_

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

#### Log output

arg: _-L_

values : directory

Select output directory for log files

exemple : 
```
 -L ../../my/best/logs
```

#### Run script

arg: _-s_

values : script file

Run script file

exemple : 
```
 -s ../../my/best/script.yml
```

## Script file structure


```
# List of request
reqs: 
    # request title (MANDATORY)
    - title: reboot 
    # request sequence (MANDATORY)
      seq: 7E A5 15 10 0E 0B 7E
    # manual hit key ID 1-4 ( OPTIONAL )
      key: 1
    # periodic auto send in ms ( OPTIONAL )
      period: 1000

# List of attempted response        
resps: 
    # response title (MANDATORY)
    - title: startup
    # request sequence (MANDATORY)
      seq: 7E A5 08 10 00 E7 63 7E
    # request to run on response found (OPTIONAL)
      run: getconfig
    # delay before sending response in ms (OPTIONAL)
      delay: 500
```


A *response* without *run* request is used to add automatic info in log to allow fast read and debug.