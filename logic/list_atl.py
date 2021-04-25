import itertools
from execptions.execptions import *
from graphics.colors import Colors
from graphics.io import IO


class ListAtl:
    def __init__(self, i_debug=True):
        self._m_events_state = {item: set() for item in ('X', 'XX', 'XY', 'XYY', 'XYYX',
                                                         'XYX', 'XYXY', 'XXY', 'XXYY', 'XD')}
        self.__m_events_functions = {'begin': [self.__xxy, self.__xy, self.__x],
                                     'end': [self.__xxyy, self.__xxy, self.__xyxy,
                                             self.__xyx, self.__xyyx, self.__xyy,
                                             self.__xy, self.__xx, self.__x],
                                     'data': self.__xd}
        self.__m_debug = i_debug

    def __str__(self):
        set_state = []
        for set_name, set_data in self._m_events_state.items():
            set_state.append(f'{Colors.PURPLE}[{set_name}]: {set_data}')
        return '\n'.join(set_state)

    def interval_final_state(self):
        return f"{Colors.PURPLE}{Colors.BOLD}[FINAL]: " \
               f"XYXY: {self._m_events_state['XYXY']}, " \
               f"XYYX: {self._m_events_state['XYYX']}, " \
               f"XXYY: {self._m_events_state['XXYY']}{Colors.DEFAULT}".replace('set()', '{}')

    def event_update(self, i_type, i_interval, i_interval_data_dict=None):

        if self.__m_debug:
            IO.seperator(f'[EVENT]: {i_type}->{i_interval}')

        if self.__event_validation_check(i_type, i_interval):
            for event_function in self.__m_events_functions[i_type]:
                if event_function in [self.__x, self.__xy, self.__xxy]:
                    event_function(i_type, i_interval)
                else:
                    event_function(i_interval)

            if i_type == "end":
                self.__m_events_functions['data'] (i_interval, i_interval_data_dict["data"])

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

        if self.__m_debug:
            IO.bdd_state('X', f"{self._m_events_state['X']}".replace('set()', '{}'))

    def __xx(self, i_interval):
        self._m_events_state['XX'] = self._m_events_state['XX'].union([i_interval])
        if self.__m_debug:
            IO.bdd_state('XX', f"{self._m_events_state['XX']}".replace('set()', '{}'))

    def __xy(self, i_type, i_interval):
        if i_type == 'begin':
            self._m_events_state['XY'] = self._m_events_state['XY'].union(
                itertools.product(self._m_events_state['X'], [i_interval]))
        else:
            self._m_events_state['XY'] = {x for x in self._m_events_state['XY'] if i_interval not in x}

        if self.__m_debug:
            IO.bdd_state('XY', f"{self._m_events_state['XY']}".replace('set()', '{}'))

    def __xyy(self, i_interval):
        self._m_events_state['XYY'] = (self._m_events_state['XYY'] - self._m_events_state['XYYX']).union(
            {x for x in self._m_events_state['XY'] if i_interval == x[-1]})

        if self.__m_debug:
            IO.bdd_state('XYY', f"{self._m_events_state['XYY']}".replace('set()', '{}'))

    def __xyyx(self, i_interval):
        self._m_events_state['XYYX'] = self._m_events_state['XYYX'].union(
            {x for x in self._m_events_state['XYY'] if i_interval == x[0]})

        if self.__m_debug:
            IO.bdd_state('XYYX', f"{self._m_events_state['XYYX']}".replace('set()', '{}'))

    def __xyx(self, i_interval):
        self._m_events_state['XYX'] = (self._m_events_state['XYX'] - self._m_events_state['XYXY']).union(
            {x for x in self._m_events_state['XY'] if i_interval == x[0]})

        if self.__m_debug:
            IO.bdd_state('XYX', f"{self._m_events_state['XYX']}".replace('set()', '{}'))

    def __xyxy(self, i_interval):
        self._m_events_state['XYXY'] = self._m_events_state['XYX'].union(
            {x for x in self._m_events_state['XYX'] if i_interval == x[-1]})

        if self.__m_debug:
            IO.bdd_state('XYXY', f"{self._m_events_state['XYXY']}".replace('set()', '{}'))

    def __xxy(self, i_type, i_interval):
        if i_type == 'begin':
            self._m_events_state['XXY'] = self._m_events_state['XXY'].union(
                itertools.product(self._m_events_state['XX'], [i_interval]))
        else:
            self._m_events_state['XXY'] = {x for x in self._m_events_state['XXY'] if i_interval != x[-1]}

        if self.__m_debug:
            IO.bdd_state('XXY', f"{self._m_events_state['XXY']}".replace('set()', '{}'))

    def __xxyy(self, i_interval):
        self._m_events_state['XXYY'] = self._m_events_state['XXYY'].union(
            {x for x in self._m_events_state['XXY'] if i_interval == x[-1]})

        if self.__m_debug:
            IO.bdd_state('XXYY', f"{self._m_events_state['XXYY']}".replace('set()', '{}'))

    def __xd(self, i_interval, i_data):
        self._m_events_state['XD'].add((i_interval, i_data))

        if self.__m_debug:
            IO.bdd_state('XD', f"{self._m_events_state['XD']}".replace('set()', '{}'))
