import itertools
from execptions.interval_execptions import *
from graphics.colors import Colors


class ListAtl:
    def __init__(self):
        self._m_events_state = {item: set() for item in ('X', 'XX', 'XY', 'XYY', 'XYYX', 'XYX', 'XYXY', 'XXY', 'XXYY')}
        self.__m_events_functions = {'begin': [self.__xxy, self.__xy, self.__x],
                                     'end': [self.__xxyy, self.__xxy, self.__xyxy,
                                             self.__xyx, self.__xyyx, self.__xyy,
                                             self.__xy, self.__xx, self.__x]}
        self._m_time_point = 0

    def __str__(self):
        return f"[TIME POINT {self._m_time_point}]: {str(self._m_events_state).replace('set()', '{}')[1:-1]}"

    def interval_final_state(self):
        return f"{Colors.PURPLE}{Colors.BOLD}[FINAL]: " \
               f"XYXY: {self._m_events_state['XYXY']}, " \
               f"XYYX: {self._m_events_state['XYYX']}, " \
               f"XXYY: {self._m_events_state['XXYY']}{Colors.DEFAULT}".replace('set()', '{}')

    def event_update(self, i_type, i_interval):
        if self.__event_validation_check(i_type, i_interval):
            for event_function in self.__m_events_functions[i_type]:
                if event_function in [self.__x, self.__xy, self.__xxy]:
                    event_function(i_type, i_interval)
                else:
                    event_function(i_interval)
        self._m_time_point += 1

    def __event_validation_check(self, i_type, i_interval):

        if i_type == "begin":
            if i_interval in (self._m_events_state['X'].union(self._m_events_state['XX'])):
                raise MultipleBeginError(i_interval)
        elif i_type == "end":
            if i_interval in self._m_events_state['XX']:
                raise MultipleEndError(i_interval)
            elif i_interval not in self._m_events_state['X']:
                raise EndsBeforeBeginError(i_interval)
        else:
            raise BadEventValueError(i_type)

        return True

    def __x(self, i_type, i_interval):
        if i_type == 'begin':
            self._m_events_state['X'] = self._m_events_state['X'].union([i_interval])
        else:
            self._m_events_state['X'].remove(i_interval)

    def __xx(self, i_interval):
        self._m_events_state['XX'] = self._m_events_state['XX'].union([i_interval])

    def __xy(self, i_type, i_interval):
        if i_type == 'begin':
            self._m_events_state['XY'] = self._m_events_state['XY'].union(
                itertools.product(self._m_events_state['X'], [i_interval]))
        else:
            self._m_events_state['XY'] = {x for x in self._m_events_state['XY'] if i_interval not in x}

    def __xyy(self, i_interval):
        self._m_events_state['XYY'] = self._m_events_state['XYY'].union(
            {x for x in self._m_events_state['XY'] if i_interval == x[-1]})

    def __xyyx(self, i_interval):
        self._m_events_state['XYYX'] = self._m_events_state['XYYX'].union(
            {x for x in self._m_events_state['XYY'] if i_interval == x[0]})

    def __xyx(self, i_interval):
        self._m_events_state['XYX'] = self._m_events_state['XYX'].union(
            {x for x in self._m_events_state['XY'] if i_interval == x[0]})

    def __xyxy(self, i_interval):
        self._m_events_state['XYXY'] = self._m_events_state['XYX'].union(
            {x for x in self._m_events_state['XYX'] if i_interval == x[-1]})

    def __xxy(self, i_type, i_interval):
        if i_type == 'begin':
            self._m_events_state['XXY'] = self._m_events_state['XXY'].union(
                itertools.product(self._m_events_state['XX'], [i_interval]))
        else:
            self._m_events_state['XXY'] = {x for x in self._m_events_state['XXY'] if i_interval != x[-1]}

    def __xxyy(self, i_interval):
        self._m_events_state['XXYY'] = self._m_events_state['XXYY'].union(
            {x for x in self._m_events_state['XXY'] if i_interval == x[-1]})