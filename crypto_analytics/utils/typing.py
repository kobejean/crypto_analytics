from typing import Optional, TypeVar, Union, Callable, cast

T = TypeVar('T')

RealNumber = Union[int, float]
Coalescable = Union[Callable[[], Optional[T]], Optional[T]]

def coalesce(*arg: Coalescable[T]) -> T:
    for element in arg:
        optional = element() if callable(element) else element
        if optional is not None:
            return cast(T, optional)
    raise ValueError('must have at least one non-None valued optional to coalesce')

def unwrap(optional: Optional[T]) -> T:
    if optional is not None:
        return cast(T, optional)
    raise ValueError('cannot unwrap optional because its value is None')
