from dd import autoref as _bdd
from execptions.interval_execptions import *
from graphics.colors import Colors
from graphics.io import IO


class BddAtl:
    def __init__(self, i_num_of_variables=3, i_debug=True):
        self._m_bdd_manager = _bdd.BDD()
        self._m_interval_num_of_variables = i_num_of_variables
        self._m_data_num_of_variables = i_num_of_variables
        self.__m_debug = i_debug
        self.__declare_variables(i_num_of_variables)
        self._m_bdds = self.__init_bdds_state()
        self.__m_events_functions = self.__init_event_functions()
        self.__m_bitstrings = {}

    def __str__(self)->str:
        """
        Create a printed version of BDDs current state

        Returns
        -------
        String which contains the BDDs current state

        """

        bdds_state = []
        for bdd_name, bdd_data in self._m_bdds.items():
            bdds_state.append(f'{Colors.PURPLE}[{bdd_name}]: '
                              f'{self._sorted_bdd_assignments(bdd_name)}')
        return '\n'.join(bdds_state)

    @property
    def bdds(self)->dict:
        """
        Returns the BDDs current state.
        For testing purposes.

        Returns
        -------
        BDDs current state.

        """

        return {key: list(self._m_bdd_manager.pick_iter(bdd_data)) for key, bdd_data in self._m_bdds.items()}

    def __declare_variables(self, i_num_of_variables: int):
        """
        Declare the variables which are valid in the BDD manager.
        It also set the order of the variable in the BDD ('X0', 'X1', ..., 'Y0', 'Y1', ...)

        Parameters
        ----------
        i_num_of_variables : The number of variable in full assignment formula.

        Returns
        -------
        None

        """

        x_variables = [f'X{i}' for i in range(i_num_of_variables)]
        y_variables = [f'Y{i}' for i in range(i_num_of_variables)]
        d_variables = [f'D{i}' for i in range(i_num_of_variables)]
        self._m_bdd_manager.declare(*(x_variables + y_variables + d_variables))

    def __init_bdds_state(self)->dict:
        """
        Create and initialize to an empty set the BDDs that belong to the BDD manager.

        Returns
        -------
        Dictionary, which contains all 9 possible BDDs in the algorithm.

        """

        bdd_list = ['X', 'XX', 'XY', 'XYY', 'XYYX', 'XYX', 'XYXY', 'XXY', 'XXYY', 'XD']
        return {bdd_name: self._m_bdd_manager.false for bdd_name in bdd_list}

    def __init_event_functions(self)->dict:
        """
        Creates a dictionary that contains the updated rules for the 'begin'/'end' events or the 'data' BDD update rule.
        When the key type is 'begin', it will execute the sequence of the related functions.
        Same for key type 'end' and 'data'.

        Returns
        -------
        Dictionary with 'begin'/'end'/'data' keys.

        """

        return {'begin': [self.__xxy, self.__xy, self.__x],
                'end': [self.__xxyy, self.__xxy, self.__xyxy,
                        self.__xyx, self.__xyyx, self.__xyy,
                        self.__xy, self.__xx, self.__x],
                'data': self.__xd}

    def __bdd_manager_variable_extend_update(self, i_type: str, i_new_num_of_variables: int):
        """
        Update the supported variables in the BDD manager upon reaching to bitstring length limit (interval or data).

        Parameters
        ----------
        i_type : Indicate if interval or data should be extend.
        i_new_num_of_variables : The new size of the bitstring.

        Returns
        -------

        """

        # In a case of the bitstring interval reach to his max size.
        if i_type == 'Interval':
            length_diff = i_new_num_of_variables - self._m_interval_num_of_variables
            x_variables = self.__define_new_variables('X', self._m_interval_num_of_variables, i_new_num_of_variables)
            y_variables = self.__define_new_variables('Y', self._m_interval_num_of_variables, i_new_num_of_variables)
            old_length = self._m_interval_num_of_variables
            self._m_interval_num_of_variables = i_new_num_of_variables
            new_vars = x_variables + y_variables

        # In a case of the bitstring data reach to his max size.
        else:
            length_diff = i_new_num_of_variables - self._m_data_num_of_variables
            d_variables = self.__define_new_variables('D', self._m_data_num_of_variables, i_new_num_of_variables)
            old_length = self._m_data_num_of_variables
            self._m_data_num_of_variables = i_new_num_of_variables
            new_vars = d_variables

        # Adding new variables into the BDD manager.
        for new_var in new_vars:
            self._m_bdd_manager.add_var(new_var)

        # Setting the new order in the BDD manager.
        new_order_variable = {bdd_name: level for level, bdd_name in enumerate(self.__variable_sort())}
        _bdd.reorder(self._m_bdd_manager, new_order_variable)

        # Renaming the variables according to their new order.
        self.__variables_substitution(i_type, length_diff)

        # Update all the existing BDDs.
        self.__bdd_assignments_updates(i_type, length_diff)

        # Print info message of the bitstring update.
        if self.__m_debug:
            IO.seperator('INFO')
            IO.info(f'BDD variables {i_type} growth ({old_length} -> {i_new_num_of_variables})')

    def __define_new_variables(self, i_variable: str, i_start_index: int, i_end_index: int)->list:
        """

        Create a list with the variables should be added.

        Parameters
        ----------
        i_variable : The type of the variable family ('X', 'Y' or 'D').
        i_start_index : The starting index of the new variables.
        i_end_index : The ending index of the new variables.

        Returns
        -------
        A list which contains all the variables belong to i_variable type.

        """

        return [f'{i_variable}{i}' for i in range(i_start_index, i_end_index)]

    def __variable_sort(self)->list:
        """
        Sorting the variables in the order of 'X1', 'X2',...,'Y1', 'Y2',..., 'D1', 'D2',...

        Returns
        -------
        A custom sorted list in the order above.

        """

        sorted_variables = sorted(self._m_bdd_manager.vars.keys())
        while 'D' in sorted_variables[0]:
            sorted_variables.append(sorted_variables.pop(sorted_variables.index(sorted_variables[0])))

        return sorted_variables

    def __variables_substitution(self, i_variable: str, i_length_diff: int):
        """
        Rename the interval variables so they fit to the new order upon variables update.

        Returns
        -------
        None

        """

        # In a case of the bitstring interval reach to his max size.
        if i_variable == 'Interval':
            variables_rename = {**self.__variables_rename('X', i_length_diff, self._m_interval_num_of_variables),
                                **self.__variables_rename('Y', i_length_diff, self._m_interval_num_of_variables)}
            bdds = self._m_bdds.keys()

        # In a case of the bitstring data reach to his max size.
        else:
            variables_rename = self.__variables_rename('D', i_length_diff, self._m_data_num_of_variables)
            bdds = ['XD']

        # Variables substitution
        for bdd_name in bdds:
            self._m_bdds[bdd_name] = self._m_bdd_manager.let(variables_rename, self._m_bdds[bdd_name])

    def __variables_rename(self, i_variable: str, i_length_diff: int, i_num_of_variable: int)->dict:
        """

        Parameters
        ----------
        i_variable : The type of the variable family ('X', 'Y' or 'D').
        i_length_diff : The difference between the ne wsize and the old size.
        i_num_of_variable : The new size of the variables.

        Returns
        -------

        """

        # Create a dict which map variables into their new ones
        # Example: dict(x='p', y='q') mapping 'x' to 'p' and 'y' to 'q'.
        return {f'{i_variable}{i %  i_num_of_variable}':
                f'{i_variable}{(i + i_length_diff) %  i_num_of_variable}'
                for i in range(i_num_of_variable)}

    def __bdd_assignments_updates(self, i_type: str, i_length_diff: int):
        """
        Update the BDDs assignments so they fit to the new order upon variables update.

        Parameters
        ----------
        i_type :
        i_length_diff :

        Returns
        -------
        None

        """

        # In a case of the bitstring interval reach to his max size.
        if i_type == "Interval":
            x_assignment_helper = {f'X{i}': False for i in range(i_length_diff)}
            y_assignment_helper = {f'Y{i}': False for i in range(i_length_diff)}
            assignment_helper = {'XY': {**x_assignment_helper, **y_assignment_helper}, 'X': x_assignment_helper}
            bdds = self._m_bdds.keys()

        # In a case of the bitstring data reach to his max size.
        else:
            # The key 'X' is denote for 'D'.

            assignment_helper = {'X': {f'D{i}': False for i in range(i_length_diff)}}
            bdds = ['XD']

        for bdd_name in bdds:
            # Set empty BDD for store all new updated assignments
            updated_bdd = self._m_bdd_manager.false

            # Run through all BDD assignments and update them.
            for assignment in self._m_bdd_manager.pick_iter(self._m_bdds[bdd_name]):
                if bdd_name in ['X', 'XX', 'XD']:
                    updated_bdd |= self._m_bdd_manager.cube({**assignment_helper['X'], **assignment})
                else:
                    updated_bdd |= self._m_bdd_manager.cube({**assignment_helper['XY'], **assignment})

            # Save the new updated BDD
            self._m_bdds[bdd_name] = updated_bdd

    def event_update(self, i_type: str, i_interval, i_interval_bitstring: str, i_data_bitstring=None):
        """
        Primary update function that executes in every event.

        Parameters
        ----------
        i_type : 'begin'/'end' event.
        i_interval : The interval variable before it converted into bitstring.
        i_interval_bitstring : The representation of the interval in bitstring.
        i_data_bitstring : The representation of the interval data in bitstring (default set to None).

        Returns
        -------
        None

        """

        # In a case when the BDDs need to update upon growth ot the interval bitstrings.
        if len(i_interval_bitstring) > self._m_interval_num_of_variables:
            self.__bdd_manager_variable_extend_update('Interval', len(i_interval_bitstring))

        # In a case when BDD[XD] need to update upon growth ot the data bitstrings.
        if i_data_bitstring is not None:
            if len(i_data_bitstring) > self._m_data_num_of_variables:
                self.__bdd_manager_variable_extend_update('Data', len(i_interval_bitstring))

        if self.__m_debug:
            IO.seperator(f'[EVENT]: {i_type}->{i_interval}')

        # Converts the bitstring into an assignment.
        self.__interval_to_bdd_assignment(i_interval_bitstring, 'X')
        self.__interval_to_bdd_assignment(i_interval_bitstring, 'Y')

        # Validates if the event is valid.
        # It could be few types of errors during the validation.
        if self.__event_validator(i_type, self.__m_bitstrings[i_interval_bitstring], i_interval):

            # Executes the relevant update function in the sequence determined.
            for event_function in self.__m_events_functions[i_type]:
                self._m_bdd_manager.collect_garbage()  # Optional
                if event_function in [self.__x, self.__xy, self.__xxy]:
                    event_function(i_type, self.__m_bitstrings[i_interval_bitstring])
                else:
                    event_function(self.__m_bitstrings[i_interval_bitstring])

            # Create BDD[XD] when it relevant.
            if i_data_bitstring is not None:

                # Converts the bitstring into an assignment.
                self.__interval_to_bdd_assignment(i_data_bitstring, 'D')

                # Call to self.__xd function
                self.__m_events_functions['data'](self.__m_bitstrings[i_interval_bitstring]['X'],
                                                  self.__m_bitstrings[i_data_bitstring]['D'])

            # Deletes the expression from the data structure when the interval comes to an 'end' event.
            if i_type == 'end':
                del self.__m_bitstrings[i_interval_bitstring]

    def __event_validator(self, i_type: str, i_assignment: dict, i_interval: int)->bool:
        """
        Validates if the event is valid.
        It could be few types of errors during the validation.
        Parameters
        ----------
        i_type : 'begin'/'end' event.
        i_assignment : Converted bitstring into an assignment.
        i_interval : The interval variable before it converted into bitstring.

        Returns
        -------
        True if no errors founds.

        """
        # Create BDD helper for intersection operation.
        bdd_helper = self._m_bdd_manager.cube(i_assignment['X'])

        if i_type == "begin":
            # if {z} ∩ (BDD[X] ∪ BDD[XX]) != {}; then “Multiple begin”.
            if list(self._m_bdd_manager.pick_iter(bdd_helper & (self._m_bdds['X'] | self._m_bdds['XX']))):
                raise MultipleBeginError(i_interval)

        elif i_type == "end":
            # If {z} ∩ BDD[XX] != {}; then “Multiple end”.
            if list(self._m_bdd_manager.pick_iter(bdd_helper & self._m_bdds['XX'])):
                raise MultipleEndError(i_interval)

            # If {z} ∩ BDD[X] == {}; then “Intervals ends before it begins”.
            if not list(self._m_bdd_manager.pick_iter(bdd_helper & self._m_bdds['X'])):
                raise EndsBeforeBeginError(i_interval)

        else:
            # If key is not defined (not 'begin' or 'end').
            raise BadEventValueError(i_type)

        return True

    def __interval_to_bdd_assignment(self, i_bitstring: str, i_variable: str):
        """
        # Converts the bitstring into an assignment.

        Parameters
        ----------
        i_bitstring : The representation of the interval in bitstring.
        i_variable : The type of variable in the BDD (X, Y or D)

        Returns
        -------
        None

        """
        if i_bitstring not in self.__m_bitstrings.keys():
            self.__m_bitstrings[i_bitstring] = {}

        # Assignment conversion for X's (When the interval is left to relation).
        # Assignment conversion for Y's (When the interval is left to relation).
        # Assignment conversion for D's (When is interval data).
        if i_variable not in self.__m_bitstrings[i_bitstring].keys():
            self.__m_bitstrings[i_bitstring][i_variable] = \
                {f'{i_variable}{index}': (False if bit == '0' else True) for index, bit in enumerate(i_bitstring)}

    def __x(self, i_type: str, i_assignment: dict):
        """
        Update BDD[X] according algorithm.

        Parameters
        ----------
        i_type : 'begin'/'end' event.
        i_assignment : Converted bitstring into an assignment.

        Returns
        -------
        None

        """

        # BDD[X] = BDD[X] ∪ {z}
        if i_type == 'begin':
            self._m_bdds['X'] |= self._m_bdd_manager.cube(i_assignment['X'])

        # BDD[X] = BDD[X] ∩ ~{z}
        else:
            bdd_helper_x = self._m_bdd_manager.cube(i_assignment['X'])
            self._m_bdds['X'] &= ~bdd_helper_x

        if self.__m_debug:
            IO.bdd_state('X', self._sorted_bdd_assignments('X'))

    def __xx(self, i_assignment: dict):
        """
        Update BDD[XX] according algorithm.

        Parameters
        ----------
        i_assignment : Converted bitstring into an assignment.

        Returns
        -------
        None

        """

        # BDD[XX] = BDD[XX] ∪ {z}
        self._m_bdds['XX'] |= self._m_bdd_manager.cube(i_assignment['X'])

        if self.__m_debug:
            IO.bdd_state('XX', self._sorted_bdd_assignments('XX'))

    def __xy(self, i_type, i_assignment):
        """
        Update BDD[XY] according algorithm.

        Parameters
        ----------
        i_type : 'begin'/'end' event.
        i_assignment : Converted bitstring into an assignment.

        Returns
        -------
        None

        """

        bdd_helper_x = self._m_bdd_manager.cube(i_assignment['X'])
        bdd_helper_y = self._m_bdd_manager.cube(i_assignment['Y'])

        # BDD[XY] = BDD[XY] ∪ ((BDD[X] × {z}))
        if i_type == 'begin':
            self._m_bdds['XY'] |= (self._m_bdds['X'] & bdd_helper_y)

        # BDD[XY] = BDD[XY] ∩ ((BDD[U] × ~{z}) ∩ (~{z} × BDD[U]))
        else:
            self._m_bdds['XY'] &= ((self._m_bdd_manager.true & ~bdd_helper_x) &
                                   (self._m_bdd_manager.true & ~bdd_helper_y))

        if self.__m_debug:
            IO.bdd_state('XY', self._sorted_bdd_assignments('XY'))

    def __xyy(self, i_assignment):
        """
        Update BDD[XYY] according algorithm.

        Parameters
        ----------
        i_assignment : Converted bitstring into an assignment.

        Returns
        -------
        None

        """

        bdd_helper_y = self._m_bdd_manager.cube(i_assignment['Y'])

        # # BDD[XYY] = BDD[XYY] ∪ (BDD[XY] ∩ (BDD[U] × {z}))
        # self._m_bdds['XYY'] |= (self._m_bdds['XY'] & (self._m_bdd_manager.true & bdd_helper_y))

        # BDD[XYY] = (BDD[XYY] ∩ !BDD[XYYX]) ∪ (BDD[XY] ∩ (BDD[U] × {z}))
        self._m_bdds['XYY'] = (self._m_bdds['XYY'] & ~self._m_bdds['XYYX']) | \
                              (self._m_bdds['XY'] & (self._m_bdd_manager.true & bdd_helper_y))

        if self.__m_debug:
            IO.bdd_state('XYY', self._sorted_bdd_assignments('XYY'))

    def __xyyx(self, i_assignment):
        """
        Update BDD[XYYX] according algorithm.

        Parameters
        ----------
        i_assignment : Converted bitstring into an assignment.

        Returns
        -------
        None

        """

        bdd_helper_x = self._m_bdd_manager.cube(i_assignment['X'])

        # BDD[XYYX] = BDD[XYYX] ∪ (BDD[XYY] ∩ ({z} × BDD[U]))
        self._m_bdds['XYYX'] |= (self._m_bdds['XYY'] & (self._m_bdd_manager.true & bdd_helper_x))

        if self.__m_debug:
            IO.bdd_state('XYYX', self._sorted_bdd_assignments('XYYX'))

    def __xyx(self, i_assignment):
        """
        Update BDD[XYX] according algorithm.

        Parameters
        ----------
        i_assignment : Converted bitstring into an assignment.

        Returns
        -------
        None

        """

        bdd_helper_x = self._m_bdd_manager.cube(i_assignment['X'])

        # # BDD[XYX] = BDD[XYX] ∪ (BDD[XY] ∩ ({z} × BDD[U])
        # self._m_bdds['XYX'] |= (self._m_bdds['XY'] & (self._m_bdd_manager.true & bdd_helper_x))

        # BDD[XYX] = (BDD[XYX] ∩ !BDD[XYX]) ∪ (BDD[XY] ∩ ({z} × BDD[U])
        self._m_bdds['XYX'] = (self._m_bdds['XYX'] & ~self._m_bdds['XYXY']) | \
                              (self._m_bdds['XY'] & (self._m_bdd_manager.true & bdd_helper_x))

        if self.__m_debug:
            IO.bdd_state('XYX', self._sorted_bdd_assignments('XYX'))

    def __xyxy(self, i_assignment):
        """
        Update BDD[XYXY] according algorithm.

        Parameters
        ----------
        i_assignment : Converted bitstring into an assignment.

        Returns
        -------
        None

        """

        bdd_helper_y = self._m_bdd_manager.cube(i_assignment['Y'])

        # BDD[XYXY] = BDD[XYXY] ∪ (BDD[XYX] ∩ (BDD[U] × {z}))
        self._m_bdds['XYXY'] |= (self._m_bdds['XYX'] & (self._m_bdd_manager.true & bdd_helper_y))

        if self.__m_debug:
            IO.bdd_state('XYXY', self._sorted_bdd_assignments('XYXY'))

    def __xxy(self, i_type, i_assignment):
        """
        Update BDD[XXY] according algorithm.

        Parameters
        ----------
        i_type : 'begin'/'end' event.
        i_assignment : Converted bitstring into an assignment.

        Returns
        -------
        None

        """
        bdd_helper_y = self._m_bdd_manager.cube(i_assignment['Y'])

        # BDD[XXY] = BDD[XXY] ∪ (BDD[XX] × {z})
        if i_type == 'begin':
            self._m_bdds['XXY'] |= (self._m_bdds['XX'] & bdd_helper_y)

        # BDD[XXY] = BDD[XXY] ∩(BDD[U] × {z})
        else:
            self._m_bdds['XXY'] &= (self._m_bdd_manager.true & ~bdd_helper_y)

        if self.__m_debug:
            IO.bdd_state('XXY', self._sorted_bdd_assignments('XXY'))

    def __xxyy(self, i_assignment):
        """
        Update BDD[XXYY] according algorithm.

        Parameters
        ----------
        i_assignment : Converted bitstring into an assignment.

        Returns
        -------
        None

        """

        bdd_helper_y = self._m_bdd_manager.cube(i_assignment['Y'])

        # BDD[XXYY] = BDD[XXYY] ∪ (BDD[XXY] ∩ (BDD[U] × {z}))
        self._m_bdds['XXYY'] |= (self._m_bdds['XXY'] & (bdd_helper_y & self._m_bdd_manager.true))

        if self.__m_debug:
            IO.bdd_state('XXYY', self._sorted_bdd_assignments('XXYY'))

    def __xd(self, i_assignment_x: str, i_assignmet_d: str):
        """
        Update BDD[XD] according algorithm.

        Parameters
        ----------
        i_assignment_x : Converted interval bitstring into an assignment.
        i_assignmet_d : Converted data bitstring into an assignment.

        Returns
        -------

        """
        bdd_helper_x = self._m_bdd_manager.cube(i_assignment_x)
        bdd_helper_d = self._m_bdd_manager.cube(i_assignmet_d)

        # BDD[XD] = BDD[XD] ∪ {z, d}
        self._m_bdds['XD'] |= (bdd_helper_x & bdd_helper_d)

        if self.__m_debug:
            IO.bdd_state('XD', self._sorted_bdd_assignments('XD'))

    def _sorted_bdd_assignments(self, i_bdd: str)->list:
        """
        Get the BDD assignments using dd internal function.
        Each assignment is sort buy the dictionary keys.

        Parameters
        ----------
        i_bdd : The relevant BDD name.

        Returns
        -------
        Sorted BDD assignments.

        """

        key_order = ['D', 'X', 'Y']
        bdd_assignments = list(self._m_bdd_manager.pick_iter(self._m_bdds[i_bdd]))
        return [dict(sorted(assignment.items(), key=lambda x: key_order)) for assignment in bdd_assignments]




