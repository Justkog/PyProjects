__author__ = 'justkog'

from os import environ

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

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
        print("Subscribed to com.example.onmotorslide with {}".format(sub.id))

    def on_event(self, i):
        print("Got event: {}".format(i))
        self.received += 1
        # self.config.extra for configuration, etc. (see [A])
        if self.received > self.config.extra['max_events']:
            print("Received enough events; disconnecting.")
            self.leave()

    def onDisconnect(self):
        print("disconnected")
        if reactor.running:
            reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"realm1",
        extra=dict(
            max_events=105,  # [A] pass in additional configuration
        ),
        debug_wamp=True,  # optional; log many WAMP details
        debug=True,  # optional; log even more details
    )
    runner.run(Component)