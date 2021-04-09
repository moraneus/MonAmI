class BadEventValueError(Exception):
    def __init__(self, i_value):
        self.__m_message = f"JSON is not in the right format (Caused by value '{i_value}' in JSON file)"
        super().__init__(self.__m_message)


class IntervalDataError(Exception):
    def __init__(self, i_interval):
        self.__m_message = f"Data missing error (Caused by interval {i_interval})"
        super().__init__(self.__m_message)


class MultipleBeginError(Exception):
    def __init__(self, i_interval):
        self.__m_message = f"Multiple begins (Caused by interval {i_interval})"
        super().__init__(self.__m_message)


class MultipleEndError(Exception):
    def __init__(self, i_interval):
        self.__m_message = f"Multiple ends (Caused by interval {i_interval})"
        super().__init__(self.__m_message)


class EndsBeforeBeginError(Exception):
    def __init__(self, i_interval):
        self.__m_message = f"Interval ends before it begins (Caused by interval {i_interval})"
        super().__init__(self.__m_message)
