class CommonDescriptor:
    '''
    Дескриптор с валидацией данных
    '''

    @classmethod
    def verify_this(cls, value):
        raise NotImplementedError

    def __set_name__(self, owner, name):
        self.name = "__" + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.verify_this(value)
        instance.__dict__[self.name] = value


class NonNegative(CommonDescriptor):
    '''
    Дескриптор для работы с положительными ненулевыми числами
    '''

    @classmethod
    def verify_this(cls, number):
        if type(number) not in (int, float) or number <= 0:
            raise ValueError(
                "Параметр должен быть положительным числом больше нуля")
