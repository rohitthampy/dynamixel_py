## Acknowledgement

Most of the source code and architecture used in this project was adapted from the [PyDynamixel_v2](https://github.com/TauraBots/PyDynamixel_v2/tree/more_robust) library made by the amazing members of [TauraBots](https://github.com/TauraBots).

## Usage

1) Clone this repository using `git clone https://github.com/rohitthampy/dynamixel_py.git`
2) Create a virtual environment and `pip install dynamixel-sdk`
3) Create your python project at the root of this repository.
4) To use it in your python file `from servos.XL330 import XL330Comm, XL330Ctrl`.
5) Have a look at the examples for inspiration.

## About this library

This is more of a python wrapper than a library.

It has three classes. 
- `DxlComm` is responsible for opening and starting a communication port like USB.
- `Servo` is responsible for controlling dynamixel motors. You can use it for things such as getting the position of the servo, sending to to a goal position etc.
- `ServoGroup` is responsible for sending commands and receiving data from servos with the same control table and protocol simultaneously.



