class MealyError(Exception):
    pass

class raises:
    def __init__(self, exception):
        self.exception = exception

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            raise AssertionError(f"{self.exception.__name__} not raised")
        if issubclass(exc_type, self.exception):
            return True
        raise exc_value

# Пример использования
with raises(MealyError) as e:
    raise MealyError("This is a Mealy error")