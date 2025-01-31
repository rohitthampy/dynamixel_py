## Usage

1) Clone this repository using `git clone https://github.com/rohitthampy/dynamixel-py.git`
2) Create a virtual environment and `pip install dynamixel-sdk`
3) Create your python project at the root of this repository.
4) To use it in your python file `from servos.XL330 import XL330Comm, XL330Ctrl`.
5) Have a look at the examples for inspiration.

## About this library

This is more of a python wrapper than a library.

It has two classes. 
- `XL33Comm` is responsible for opening and starting a communication port like USB.
- `XL330Ctrl` is responsible for controlling dynamixel motors. You can use it for things such as getting the position of the servo, sending to to a goal position etc.


