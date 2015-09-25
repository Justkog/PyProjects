import RPi.GPIO as GPIO
import time
from RPIO import PWM
from Tkinter import *

def WaitPushAndMove(ButtonGPIORef, ServoPWM, ServoCycle):
    try:
        while not GPIO.input(ButtonGPIORef):
            time.sleep(0.1)
            
        if GPIO.input(ButtonGPIO) == True:
            print("button pressed / " + "cycle of " + str(ServoCycle))
            ServoPWM.ChangeDutyCycle(ServoCycle)
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("input interrupted")
    return True

def WaitPushAndMoveRPIO(ButtonGPIORef, ServoPWM, ServoCycle):
    try:
        while not GPIO.input(ButtonGPIORef):
            time.sleep(0.1)
            
        if GPIO.input(ButtonGPIO) == True:
            print("button pressed / " + "cycle of " + str(ServoCycle))
            ServoPWM.set_servo(18, ServoCycle)
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("input interrupted")
    return True

class RPIOHelper:
    def WaitAndMoveRPIO(WaitTime, ServoPWM, ServoCycle):
        time.sleep(WaitTime)

        print("time waited / " + "cycle of " + str(ServoCycle))
        ServoPWM.set_servo(18, ServoCycle)
        time.sleep(0.25)
        return True
    WaitAndMoveRPIO = staticmethod(WaitAndMoveRPIO)

class MotorController:

    def __init__(self, PWMOutput, MinCycle, MaxCycle):

        self.minCycle = MinCycle
        self.maxCycle = MaxCycle
        self.output = PWMOutput
        RPIOHelper.WaitAndMoveRPIO(0, self.output, self.minCycle)
        RPIOHelper.WaitAndMoveRPIO(1, self.output, self.maxCycle)
        RPIOHelper.WaitAndMoveRPIO(1, self.output, self.minCycle)
        self.currentCycle = self.minCycle
        

GPIO.setmode(GPIO.BOARD)
##
##LedGPIO = 11
ButtonGPIO = 18
##ServoGPIO = 12
##ButtonGPIOstate = False
##
##loopIterations = input("please chose a number : ")
##
##print(loopIterations + " selected")
##
##GPIO.setup(LedGPIO, GPIO.OUT)
GPIO.setup(ButtonGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
##GPIO.setup(ServoGPIO, GPIO.OUT)
##PServo = GPIO.PWM(ServoGPIO, 50)
##
##GPIO.output(LedGPIO, GPIO.LOW)
##
##PServo.start(0.5)

servo = PWM.Servo()

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        scale = Scale(frame, from_=100, to=195,
                      orient=HORIZONTAL, command=self.update,
                      length=250)
        scale.grid(row=0)

    def update(self, angle):
##        duty = (float(angle) / 10 + 2.5) / 2
##        PServo.ChangeDutyCycle(duty)
        RPIOduty = float(angle) / 100 * 1000
        servo.set_servo(18, RPIOduty)

root = Tk()
root.wm_title('Servo Control')
app = App(root)
root.geometry("500x50+0+0")
##root.mainloop()

print("Waiting for button input")

motorController = MotorController(servo, 1000, 2000)
##WaitPushAndMoveRPIO(ButtonGPIO, servo, 1000)
##WaitPushAndMoveRPIO(ButtonGPIO, servo, 2000)
##WaitPushAndMoveRPIO(ButtonGPIO, servo, 1000)
##WaitPushAndMoveRPIO(ButtonGPIO, servo, 2000)
##WaitPushAndMoveRPIO(ButtonGPIO, servo, 600)

root.mainloop()

servo.stop_servo(18)

##try:
##    while not GPIO.input(ButtonGPIO):
##        time.sleep(0.1)
##except KeyboardInterrupt:
##    print("input interrupted")
    
##try:
##    while not GPIO.input(ButtonGPIO):
##        time.sleep(0.1)
##        
##    if GPIO.input(ButtonGPIO) == True:
##        print("button pressed / " + "cycle of " + "10")
##        PServo.start(10)
##        time.sleep(0.5)
##except KeyboardInterrupt:
##    print("input interrupted")

##WaitPushAndMove(ButtonGPIO, PServo, 7.5)

##WaitPushAndMove(ButtonGPIO, PServo, 1)
##
##WaitPushAndMove(ButtonGPIO, PServo, 2)
##
##WaitPushAndMove(ButtonGPIO, PServo, 2.5)
##
##WaitPushAndMove(ButtonGPIO, PServo, 5)
##
##WaitPushAndMove(ButtonGPIO, PServo, 30)
##
##WaitPushAndMove(ButtonGPIO, PServo, 40)
##
##WaitPushAndMove(ButtonGPIO, PServo, 45)
##
##WaitPushAndMove(ButtonGPIO, PServo, 47.5)
##
##WaitPushAndMove(ButtonGPIO, PServo, 50)
##
##WaitPushAndMove(ButtonGPIO, PServo, 51)

##for i in range(int(loopIterations), int(loopIterations) + 10):
##    WaitPushAndMove(ButtonGPIO, PServo, i)

##for i in range(int(loopIterations)):
##    GPIO.output(LedGPIO, 1)
##    print("led on")
##    time.sleep(0.3)
##    GPIO.output(LedGPIO, 0)
##    print("led off")
##    time.sleep(0.3)
##    GPIO.output(LedGPIO, 1)
##    PServo.ChangeDutyCycle(5 + (i))

##PServo.stop()
GPIO.cleanup()
PWM.cleanup()
