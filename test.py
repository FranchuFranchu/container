from container import Container
from container.container import get_annotations

class A(Container):
    x: int = 3

class B(A):
    y: int

B(y=4)
