from datetime import datetime, date, time
from dataclasses import dataclass, field
import uuid


@dataclass
class Reminder:
    date_time: datetime
    type: str

    EMAIL = "email"
    SYSTEM = "system"

    def __str__(self):
        return f"Reminder on {self.date_time} of type {self.type}"


@dataclass
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reminders: list = field(default_factory=list)

    def add_reminder(self, date_time, reminder_type):
        self.reminders.append(Reminder(date_time, reminder_type))

    def delete_reminder(self, index):
        if 0 <= index < len(self.reminders):
            del self.reminders[index]
        else:
            raise ValueError("Reminder not found")

    def __str__(self):
        return (f"ID: {self.id}\n"
                f"Event title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Time: {self.start_at} - {self.end_at}")


class Day:
    def __init__(self, date_):
        self.date_ = date_
        self.slots = {time(hour, minute): None for hour in range(24) for minute in range(0, 60, 15)}
    
    def _init_slots(self):
        self.slots = {time(hour, minute): None for hour in range(24) for minute in range(0, 60, 15)}

    def add_event(self, event_id, start_at, end_at):
        current_time = start_at
        while current_time < end_at:
            if self.slots[current_time] is not None:
                raise ValueError("Slot not available")
            self.slots[current_time] = event_id
            minute = (current_time.minute + 15) % 60
            hour = current_time.hour + (current_time.minute + 15) // 60
            current_time = time(hour, minute)

    def delete_event(self, event_id):
        for slot_time in self.slots:
            if self.slots[slot_time] == event_id:
                self.slots[slot_time] = None


class Calendar:
    def __init__(self):
        self.days = {}
        self.events = {}

    def add_event(self, title, description, date_, start_at, end_at):
        if date_ < date.today():
            raise ValueError("Cannot add events in the past")
        
        event = Event(title, description, date_, start_at, end_at)
        self.events[event.id] = event

        if date_ not in self.days:
            self.days[date_] = Day(date_)

        self.days[date_].add_event(event.id, start_at, end_at)
        return event.id

    def delete_event(self, event_id):
        if event_id in self.events:
            event = self.events[event_id]
            self.days[event.date_].delete_event(event_id)
            del self.events[event_id]

    def add_reminder(self, event_id, date_time, reminder_type):
        if event_id in self.events:
            self.events[event_id].add_reminder(date_time, reminder_type)

    def delete_reminder(self, event_id, index):
        if event_id in self.events:
            self.events[event_id].delete_reminder(index)

    def list_reminders(self, event_id):
        if event_id in self.events:
            return self.events[event_id].reminders

    def find_events(self, start_date, end_date):
        return {event_id: event for event_id, event in self.events.items()
                if start_date <= event.date_ <= end_date}

    def find_available_slots(self, date_):
        if date_ in self.days:
            return [time for time, event_id in self.days[date_].slots.items() if event_id is None]
        else:
            return []
