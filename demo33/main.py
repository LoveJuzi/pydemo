#!/usr/bin/python3

import heapq
from collections import deque

# 数字电路模拟器


#########################################################################################
class DigitalCircuitSimulator:
    agenda = None

    @staticmethod
    def initAgenda():
        DigitalCircuitSimulator.agenda = Agenda()

    @staticmethod
    def current_time():
        return DigitalCircuitSimulator.agenda.current_time()

    @staticmethod
    def reset_time():
        return DigitalCircuitSimulator.agenda.set_current_time(0)

    @staticmethod
    def after_delay(delay, func):
        DigitalCircuitSimulator.agenda.add_action(delay, func)

    @staticmethod
    def propagate():
        while not DigitalCircuitSimulator.agenda.is_empty_agenda():
            action = DigitalCircuitSimulator.agenda.first_action()
            action()
            DigitalCircuitSimulator.agenda.remove_first_action()


class Agenda:
    def __init__(self):
        self._time_list = []
        self._agenda = {}
        self._current_time = 0

    def is_empty_agenda(self):
        if not self._agenda:
            return True
        return False

    def add_action(self, time, action):
        time = self.current_time() + time
        if time not in self._agenda:
            heapq.heappush(self._time_list, time)
            self._agenda[time] = deque()
        self._agenda[time].append(action)
        return self

    def first_action(self):
        if self.is_empty_agenda():
            return None
        time = self._time_list[0]
        self.set_current_time(time)
        actions = self._agenda[time]
        return actions[0]

    def remove_first_action(self):
        if self.is_empty_agenda():
            return self
        actions = self._agenda[self.current_time()]
        actions.popleft()
        if not actions:
            del self._agenda[self.current_time()]
            heapq.heappop(self._time_list)
        return self

    def current_time(self):
        return self._current_time

    def set_current_time(self, time):
        self._current_time = time
        return self


#########################################################################################
class BasicUnit:
    inverter_delay = 2

    @staticmethod
    def inverter(in_wire, out_wire):
        def invert_input():
            new_sig = BasicUnit.logic_not(in_wire.get_signal())

            def set_signal():
                out_wire.set_signal(new_sig)

            DigitalCircuitSimulator.after_delay(BasicUnit.inverter_delay, set_signal)

        in_wire.add_action(invert_input)

    @staticmethod
    def logic_not(sig):
        if sig == 0:
            return 1
        return 0


class Wire:
    def __init__(self):
        self._sig = 0
        self._actions = Actions()

    def get_signal(self):
        return self._sig

    def set_signal(self, sig):
        if self._sig == sig:
            return self
        self._sig = sig
        self._actions.call_each()
        return self

    def add_action(self, action):
        self._actions.put(action)
        action()  # 需要运行一次，这个是为了初始化每个信号
        return self


class Actions:
    def __init__(self):
        self._actions = []

    def put(self, action):
        self._actions.append(action)
        return self

    def call_each(self):
        for action in self._actions:
            action()


#########################################################################################
def probe(name, wire):
    def display():
        print(
            f"\
{name} {DigitalCircuitSimulator.current_time()}, \
new value = {wire.get_signal()}"
        )

    wire.add_action(display)


#########################################################################################
def test_agenda():
    agenda = Agenda()
    assert agenda.is_empty_agenda()
    agenda.add_action(0, lambda: 0)
    agenda.add_action(0, lambda: 1)
    assert agenda.first_action()() == 0
    agenda.remove_first_action()
    assert agenda.first_action()() == 1


#########################################################################################


def main():
    test_inverter_v2()


def test_inverter():
    DigitalCircuitSimulator.initAgenda()
    in_wire = Wire()
    out_wire = Wire()

    probe("in", in_wire)
    probe("out", out_wire)

    BasicUnit.inverter(in_wire, out_wire)

    in_wire.set_signal(1)
    DigitalCircuitSimulator.propagate()


def test_inverter_v2():
    DigitalCircuitSimulator.initAgenda()
    in_wire = Wire()
    out_wire = Wire()
    c = Wire()

    probe("in", in_wire)
    probe("out", out_wire)

    BasicUnit.inverter(in_wire, c)
    BasicUnit.inverter(c, out_wire)

    print("=======>init")
    DigitalCircuitSimulator.propagate()

    print("=======>set_signal")
    DigitalCircuitSimulator.reset_time()
    in_wire.set_signal(1)
    DigitalCircuitSimulator.propagate()


if __name__ == "__main__":
    main()
