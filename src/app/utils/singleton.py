from threading import Lock, Thread


class Singleton(type):
    """
    Thread safe singleton metaclass
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(klass, *args, **kwargs):
        with klass._lock:
            if klass not in klass._instances:
                instance = super().__call__(*args, **kwargs)
                klass._instances[klass] = instance

        return klass._instances[klass]
