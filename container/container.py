import typing

def test_type(obj, cls):
    if isinstance(cls, typing._GenericAlias):
        if getattr(cls, "__origin__") == typing.Union:
            available = getattr(cls, "__args__")

            for i in available:
                if isinstance(obj, i):
                    return True
            
            return False


        if hasattr(typing, "Literal"):
            # Version python3.8+
            if getattr(cls, "__origin__") == typing.Literal:
                return obj in cls.__args__

    if isinstance(cls, typing._SpecialForm):
        if cls == typing.Any:
            return True

    if isinstance(obj, cls):
        return True

    return False

def get_annotations(cls):
    if hasattr(cls, "__annotations__"):
        d = {**cls.__annotations__}
    else:
        d = {}
    for i in cls.__bases__:
        d = {**d, **get_annotations(i)}
    return d

def get_dict(cls):
    if hasattr(cls, "__dict__"):
        d = {**cls.__dict__}
    else:
        d = {}
    for i in cls.__bases__:
        d = {**d, **get_dict(i)}
    return d

class BaseContainer:
    def __init__(self, **kwargs):

        nkwargs = kwargs.copy()
        for k, v in kwargs.items():
            expected_type = get_annotations(self.__class__).get(k)
            if expected_type is not None:

                if not test_type(v, expected_type):
                    raise InitTypeError(key=k, expected_type=expected_type, got_type=type(v))

            nkwargs.pop(k)
            setattr(self, k, v)



        super().__init__(**nkwargs)


class FillMixin:
    def __init__(self, **kwargs):

        # Get all the attributes that haven't been specified
        ann = get_annotations(self.__class__)
        not_specified = {k: ann[k] for k in set(ann) - set(self.__dict__)}
        for k, v in not_specified.items():
            if test_type(None, v):
                setattr(self, k, None)
                continue
            else:
                raise NonOptionalAttributeError(key=k, expected_type=v)

        super().__init__(**kwargs)

class DefaultMixin:
    def __init__(self, **kwargs):
        # Get all the attributes that have been defaulted in class
        specified_in_class = {}
        d = get_dict(self.__class__)

        for k in d.keys():
            if not hasattr(self, k):
                setattr(self, k, d[k])
            else:
                # Filter out magic attributes such as __module__
                if k.startswith("__") and k.endswith("__"):
                    continue
                if k not in self.__dict__:
                    setattr(self, k, getattr(self, k))



        super().__init__(**kwargs)


class Container(BaseContainer, DefaultMixin, FillMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class NonOptionalUnionError(TypeError, Container):
    key: str
    expected_type: typing._GenericAlias
    def __init__(self, **kwargs):
        Container.__init__(self, **kwargs)

    def __str__(self):
        return "Attribute <{key}> must be set".format(**self.__dict__)

                
class NonOptionalAttributeError(TypeError, Container):
    key: str
    expected_type: type
    def __init__(self, **kwargs):
        Container.__init__(self, **kwargs)

    def __str__(self):
        return "Attribute <{key}> must be set".format(**self.__dict__)

                
class InitTypeError(TypeError, Container):
    key: str
    expected_type: type
    got_type: type
    def __init__(self, **kwargs):
        Container.__init__(self, **kwargs)
        

    def __str__(self):
        return "Attribute <{key}> (of type {got_type}) is not an instance of {expected_type}".format(**self.__dict__)
