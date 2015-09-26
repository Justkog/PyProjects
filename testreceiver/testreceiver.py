__author__ = 'justkog'

from os import environ
from Tkinter import *
import tkMessageBox
import Queue, threading

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

wampEventsQueue = Queue.Queue()
guiEventsQueue = Queue.Queue()
g_runner = reactor

class App:

    def __init__(self, master, runner):
        frame = Frame(master)
        frame.pack()
        self.root = master
        self.runner = runner
        g_runner = runner
        self.scale = Scale(frame, from_=100, to=195,
                      orient=HORIZONTAL, command=self.updateScale,
                      length=250)
        self.scale.grid(row=0)

        self.buttonConnect = Button(frame, text="Connect", command=self.clickButtonConnect)
        self.buttonConnect.grid(row=1)

    def updateScale(self, angle):
##        duty = (float(angle) / 10 + 2.5) / 2
##        PServo.ChangeDutyCycle(duty)
        guiEventsQueue.put("gui event triggered")
        RPIOduty = float(angle) / 100 * 1000
        # servo.set_servo(18, RPIOduty)

    def clickButtonConnect(self):
        #here we start a new thread handling the wamp connection
        self.wampQueue = wampEventsQueue
        self.runnerThread = threading.Thread(target=self.runner.run, args=(Component,))
        self.runnerThread.start()

        # this triggers the need of a queue to keep track of events from the wamp module
        self.poll()
        tkMessageBox._show(title="info", message="connection engaged")

    def poll(self):
        if self.wampQueue.qsize():
            # do something with the event
            self.wampQueue.get()
            tkMessageBox._show(title="info", message="we got a message")
        self.root.after(100, self.poll)


class Component(ApplicationSession):
    """
    An application component that subscribes and receives events, and
    stop after having received 5 events.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        self.received = 0
        sub = yield self.subscribe(self.on_event, u'com.example.onmotorslide')
        # We setup an external queue events listener
        # g_runner.callFromThread(self.poll, )
        self.poll()
        print("Subscribed to com.example.onmotorslide with {}".format(sub.id))

    def on_event(self, i):
        print("Got event: {}".format(i))
        self.received += 1
        wampEventsQueue.put("event received")
        # self.config.extra for configuration, etc. (see [A])
        if self.received > self.config.extra['max_events']:
            print("Received enough events; disconnecting.")
            self.leave()

    def onDisconnect(self):
        print("disconnected")
        if reactor.running:
            reactor.stop()

    def poll(self):
        print("poll function called")
        if guiEventsQueue.qsize():
            guiEventsQueue.get()
            # yield self.publish(u'com.example.onguievent', "gui event triggered")
            print("gui event received in wamp thread")
        g_runner.callLater(0.1, self.poll, )



if __name__ == '__main__':

    # sharedQueue = Queue.Queue()

    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"realm1",
        extra=dict(
            max_events=105,  # [A] pass in additional configuration
        ),
        debug_wamp=True,  # optional; log many WAMP details
        debug=True,  # optional; log even more details
    )

    root = Tk()
    root.wm_title('Servo Control')
    app = App(root, runner)
    root.geometry("500x300+0+0")

    root.mainloop()

    # runner.run(Component)