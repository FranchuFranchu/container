# container

Python package to parse keyword arguments passed into __init__ into an object's attributes

## Code

Sample code:
    
    from container import Container
    from typing import Optional

    class Test(Container):
        x: int
        y: Optional[int]
        z: int = 1


    Test(x = 1).__dict__
    # {'x': 1, 'z': 1, 'y': None}
    Test(x = "Hello, world!").__dict__
    # container.container.InitTypeError: Attribute <x> (of type <class 'str'>) is not an instance of <class 'int'>
    Test().__dict__
    # container.container.NonOptionalAttributeError: Attribute <x> must be set