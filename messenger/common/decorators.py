from inspect import stack


def log(logger):
    def wrap(func):
        def call(*args, **kwargs):
            message = f'Функция < {func.__name__} > вызвана из функции < {stack()[1][3]} > с аргументами {args, kwargs}'
            logger.debug(message)

            return func(*args, **kwargs)

        return call

    return wrap
