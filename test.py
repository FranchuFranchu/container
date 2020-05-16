from container import Container
from enum import Enum
import typing

class Mood(Enum):
    HAPPY = 1
    SAD = 2


class Person(Container):
    mood: Mood = Mood.HAPPY
    age: int = 0
    name: str

    def smile(self):
        if self.mood == Mood.HAPPY:
            print(":)")
        elif self.mood == Mood.SAD:
            self.mood = Mood.HAPPY
            print(":)")

a = Person(mood=Mood.SAD, name = "John")
a.smile()
print(a.__dict__)