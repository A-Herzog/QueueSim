"""Base classes for event processing."""

import functools
from typing import Optional
from abc import abstractmethod
from time import perf_counter
from bisect import insort
from collections import deque
import heapq


__title__ = "queuesim"
__version__ = "1.0"
__author__ = "Alexander Herzog"
__email__ = "alexander.herzog@tu-clausthal.de"
__copyright__ = """
Copyright 2022 Alexander Herzog

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
__license__ = "Apache 2.0"


@functools.total_ordering
class Event:
    """Base class for all events."""
    __slots__ = ("__simulator", "__time", "__removed")

    def __init__(self, simulator, time: float) -> None:
        """Base class for all events.
        The event registers itself in the event list of the simulator specified here.

        Args:
            simulator (Simulator): Simulator object
            time (float): Scheduled execution time of the event
        """
        self.__simulator = simulator
        self.__time: float = time
        self.__removed: bool = False
        simulator.add_event(self)

    @abstractmethod
    def run(self) -> None:
        """This method is invoked by the simulator when the event is to be processed."""
        pass

    def remove(self) -> None:
        """Marks the event as removed. It will be ignored on execution time.
        """
        self.__removed = True

    @property
    def removed(self) -> bool:
        """Is the event active (False) or is it to be ignored (True)?

        Returns:
            bool: Is the event active (False) or is it to be ignored (True)?
        """
        return self.__removed

    @property
    def simulator(self):
        """Simulator object.

        Returns:
            Simulator: Simulator object
        """
        return self.__simulator

    @property
    def time(self) -> float:
        """Scheduled execution time of the event.

        Returns:
            float: Scheduled execution time of the event
        """
        return self.__time

    def __eq__(self, other) -> bool:
        if not isinstance(other, Event): return False
        return self.__time == other.time

    def __lt__(self, other) -> bool:
        if not isinstance(other, Event): return False
        return self.__time < other.time


class _ListEventList:
    """Event list to manage the events during the simulation."""
    __slots__ = ("__events")

    def __init__(self) -> None:
        """Event list to manage the events during the simulation."""
        self.__events: list[Event] = []

    def add(self, event: Event) -> None:
        """Adds an event to the event list.

        Args:
            event (Event): Event to be added to the list
        """
        l: list[Event] = self.__events
        size: int = len(l)

        if size == 0:
            l.append(event)
        else:
            newEventTime: float = event.time
            if newEventTime < l[0].time:
                l.insert(0, event)
                return
            if newEventTime > l[size - 1].time:
                self.__events.append(event)
                return
            insort(l, event)

    def pop(self) -> Optional[Event]:
        """Returns the next event to be executed in chronological order.
        The event will be removed from the list.

        Returns:
            Event: Next event or None if there are no more events
        """
        if not self.__events: return None
        return self.__events.pop(0)

    def remove(self, event: Event) -> bool:
        """Removes an event from the list.

        Args:
            event (Event): Event to be removed

        Returns:
            bool: Returns True if the event was contained in the list and could be removed
        """
        if not event in self.__events: return False
        self.__events.remove(event)
        return True


class _DequeEventList:
    """Event list to manage the events during the simulation."""
    __slots__ = ("__events")

    def __init__(self) -> None:
        """Event list to manage the events during the simulation."""
        self.__events: deque = deque()

    def add(self, event: Event) -> None:
        """Adds an event to the event list.

        Args:
            event (Event): Event to be added to the list
        """
        l: deque = self.__events
        size: int = len(l)

        if size == 0:
            l.append(event)
        else:
            newEventTime: float = event.time
            if newEventTime < l[0].time:
                l.appendleft(event)
                return
            if newEventTime > l[size - 1].time:
                self.__events.append(event)
                return
            insort(l, event)

    def pop(self) -> Optional[Event]:
        """Returns the next event to be executed in chronological order.
        The event will be removed from the list.

        Returns:
            Event: Next event or None if there are no more events
        """
        if not self.__events: return None
        return self.__events.popleft()

    def remove(self, event: Event) -> bool:
        """Removes an event from the list.

        Args:
            event (Event): Event to be removed

        Returns:
            bool: Returns True if the event was contained in the list and could be removed
        """
        if not event in self.__events: return False
        self.__events.remove(event)
        return True


class _HeapqEventList:
    """Event list to manage the events during the simulation."""
    __slots__ = ("__events")

    def __init__(self) -> None:
        """Event list to manage the events during the simulation."""
        self.__events = []
        heapq.heapify(self.__events)

    def add(self, event: Event) -> None:
        """Adds an event to the event list.

        Args:
            event (Event): Event to be added to the list
        """
        heapq.heappush(self.__events, event)

    def pop(self) -> Optional[Event]:
        """Returns the next event to be executed in chronological order.
        The event will be removed from the list.

        Returns:
            Event: Next event or None if there are no more events
        """
        if not self.__events: return None
        return heapq.heappop(self.__events)

    def remove(self, event: Event) -> bool:
        """Removes an event from the list.

        Args:
            event (Event): Event to be removed

        Returns:
            bool: Returns True if the event was contained in the list and could be removed
        """
        if not event in self.__events: return False
        event.remove()  # Do not remove event from heap but mark as removed
        return True

    def list_events(self) -> str:
        return ", ".join(str(round(e.time, 1)) for e in list(self.__events))


class Simulator:
    """Main system for running the simulation and managing the events."""
    __slots__ = ("__time", "__events", "__eventCount", "__nowEvent", "__runTime", "__initObjects")

    def __init__(self) -> None:
        """Main system for running the simulation and managing the events."""
        self.__time: float = 0
        self.__events: _ListEventList = _ListEventList()  # _ListEventList or _DequeEventList or _HeapqEventList can be used here; all of them are quite slow
        self.__eventCount: int = 0
        self.__runTime: float = 0
        self.__nowEvent: Optional[Event] = None
        self.__initObjects: list = []

    @property
    def time(self) -> float:
        """Current simulation time.

        Returns:
            float: Current simulation time
        """
        return self.__time

    def add_event(self, event: Event) -> None:
        """Adds an event to the internal event list.

        Args:
            event (Event): Event to be added to the list
        """
        if event.time == self.__time and self.__nowEvent is None:
            self.__nowEvent = event
        else:
            self.__events.add(event)

    def __pop_event(self) -> Optional[Event]:
        if self.__nowEvent is not None:
            event: Optional[Event] = self.__nowEvent
            self.__nowEvent = None
            return event

        event: Optional[Event] = self.__events.pop()
        if event is not None and not event.removed:
            assert self.__time <= event.time, "Event is earlier than previous event."
            self.__time = event.time
        return event

    def remove_event(self, event: Event) -> bool:
        """Removes an event from the internal list without executing it.

        Args:
            event (Event): Event to be removed

        Returns:
            bool: Returns True if the event was contained in the list and could be removed
        """
        if event is self.__nowEvent:
            self.__nowEvent = None
            return True
        else:
            return self.__events.remove(event)

    def run(self) -> None:
        """Runs the entire simulation."""

        # Initialization of the objects that create events, etc.
        for object in self.__initObjects: object.init()
        self.__initObjects.clear()

        startTime: float = perf_counter()

        # Start of the entire simulation
        event: Optional[Event] = self.__pop_event()
        while event is not None:
            if not event.removed:
                event.run()
                self.__eventCount += 1
            event = self.__pop_event()

        self.__runTime = perf_counter() - startTime

    def register_init(self, initObject: object):
        """Registers an object to be notified before the simulation starts.

        Args:
            initObject (object): Object, which must have an init() method
        """
        self.__initObjects.append(initObject)

    @property
    def event_count(self) -> int:
        """Number of events executed during the simulation.

        Returns:
            int: Number of events executed during the simulation
        """
        return self.__eventCount

    @property
    def run_time(self) -> float:
        """Runtime of the simulation in seconds.

        Returns:
            float: Runtime of the simulation in seconds
        """
        return self.__runTime
