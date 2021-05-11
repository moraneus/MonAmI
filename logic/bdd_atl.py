try:
    from dd import cudd as _bdd
except ImportError:
    from dd import autoref as _bdd
from execptions.execptions import *
from graphics.io import IO


class BddAtl():
    def __init__(self, i_variables, i_interval_size=3, i_debug=True):
        self._m_bdd_manager = _bdd.BDD()
        self.__m_property_variables = i_variables
        self._m_interval_size = i_interval_size
        self._m_data_size = i_interval_size
        self.__m_debug = i_debug
        self.__declare_variables(i_variables, i_interval_size)
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
            bdds_state.append(f'[{bdd_name}]: '
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

    @property
    def bdd_manager(self):
        """
        Returns the BDD manager.

        Returns
        -------
        Current bdd_manager state

        """

        return self._m_bdd_manager

    ###################################################################################################################
    # Here are the functions which initialize the data when the BddAtl object created.
    #   * BDD Manager <- Variables
    #   * Created an empty BDDs according the algorithm.
    #   * Declare the updated function with the right order upon new event.
    ###################################################################################################################

    def __declare_variables(self, i_variables: list, i_num_of_variables: int):
        """
        Declare the variables which are valid in the BDD manager.
        It also set the order of the variable in the BDD ('X0', 'X1', ..., 'Y0', 'Y1', ...)

        Parameters
        ----------
        i_num_of_variables : The number of variable in full assignment formula.
        i_variables : The rest of property variables should be declared.

        Returns
        -------
        None

        """

        # Creating the algorithm variables should be declare on the BDD manager
        x_variables = [f'_X{i}' for i in range(i_num_of_variables)]
        y_variables = [f'_Y{i}' for i in range(i_num_of_variables)]
        d_variables = [f'_D{i}' for i in range(i_num_of_variables)]

        # Creating the property variables should be declare on the BDD manager
        property_variables = []
        for variable in i_variables:
            if variable in ['_X', '_Y', '_D']:
                raise BadPropertyVariables(variable)
            property_variables += [f'{variable}{i}' for i in range(i_num_of_variables)]

        self._m_bdd_manager.declare(*(x_variables + y_variables + d_variables + property_variables))

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

    ###################################################################################################################
    # This is the main part of the class which build the BDDs
    # For every new event, the event_update function manage the whole process (from validating until creating new BDDs).
    # We can see here also function which responsible to the BDDs updating.
    ###################################################################################################################

    def event_update(self, i_type: str, i_interval, i_interval_bitstring: str, i_interval_data_mapping: dict):
        """
        Primary update function that executes in every event.

        Parameters
        ----------
        i_type : 'begin'/'end' event.
        i_interval : The interval variable before it converted into bitstring.
        i_interval_bitstring : The representation of the interval in bitstring.
        i_interval_data_mapping : Mapping between intervals to related data.

        Returns
        -------
        None

        """

        # In a case when the BDDs need to update upon growth of the interval bitstrings.
        if len(i_interval_bitstring) > self._m_interval_size:
            self.__bdd_manager_variable_expansion_update('Interval', len(i_interval_bitstring))

        # In a case when BDD[XD] need to update upon growth of the data bitstrings.
        if len(i_interval_data_mapping["data_bitstring"]) > self._m_data_size:
            self.__bdd_manager_variable_expansion_update('Data', len(i_interval_bitstring))

        # Print the current event
        if self.__m_debug:
            event_details = f'{i_type}({i_interval}, {i_interval_data_mapping["data"]})' \
                if i_interval_data_mapping["data"] is not None else f'{i_type}({i_interval})'
            IO.event_header(event_details)

        # Converts the bitstring into an assignment.
        self.__assignment_update(i_interval_bitstring, '_X')
        self.__assignment_update(i_interval_bitstring, '_Y')

        # Validates if the event is valid.
        # It could be few types of errors during the validation.
        if self.__event_validator(i_type, self.__m_bitstrings[i_interval_bitstring], i_interval):

            # Executes the relevant update function in the sequence determined.
            for event_function in self.__m_events_functions[i_type]:
                # self._m_bdd_manager.collect_garbage()  # Optional
                if event_function in [self.__x, self.__xy, self.__xxy]:
                    event_function(i_type, self.__m_bitstrings[i_interval_bitstring])
                else:
                    event_function(self.__m_bitstrings[i_interval_bitstring])

            # Update BDD[XD] at 'end' event.
            if i_type == 'end':

                # Converts the bitstring into an assignment.
                self.__assignment_update(i_interval_data_mapping["data_bitstring"], '_D')

                # Call to self.__xd function
                self.__m_events_functions['data'](self.__m_bitstrings[i_interval_bitstring]['_X'],
                                                  self.__m_bitstrings[i_interval_data_mapping["data_bitstring"]]['_D'])

            # Deletes the expression from the data structure when the interval comes to an 'end' event.
            if i_type == 'end':
                del self.__m_bitstrings[i_interval_bitstring]

            # Print a summerize of the BDDs current state.
            if self.__m_debug:
                for bdd_name in self._m_bdds.keys():
                    IO.bdd_state(bdd_name, self._sorted_bdd_assignments(bdd_name))


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
        bdd_helper = self._m_bdd_manager.cube(i_assignment['_X'])

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

    def __assignment_update(self, i_bitstring: str, i_variable: str):
        """
        Converts the bitstring into an assignment if not already created and update self.__m_bitstrings.

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
            self.__m_bitstrings[i_bitstring][i_variable] = self.__convert_bitstring_to_assignment(
                i_bitstring, i_variable)

    def __convert_bitstring_to_assignment(self, i_bitstring, i_variable):
        """
        Converts bitstring into an assignment.
        0 converted to False and 1 converted to True.

        Parameters
        ----------
        i_bitstring : The representation of the interval in bitstring.
        i_variable : The type of variable in the BDD (X, Y or D)

        Returns
        -------
        Dict which represent an bitstring assignment.

        """

        return {f'{i_variable}{index}': (False if bit == '0' else True) for index, bit in enumerate(i_bitstring)}


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
            self._m_bdds['X'] |= self._m_bdd_manager.cube(i_assignment['_X'])

        # BDD[X] = BDD[X] ∩ ~{z}
        else:
            bdd_helper_x = self._m_bdd_manager.cube(i_assignment['_X'])
            self._m_bdds['X'] &= ~bdd_helper_x

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
        self._m_bdds['XX'] |= self._m_bdd_manager.cube(i_assignment['_X'])

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

        bdd_helper_x = self._m_bdd_manager.cube(i_assignment['_X'])
        bdd_helper_y = self._m_bdd_manager.cube(i_assignment['_Y'])

        # BDD[XY] = BDD[XY] ∪ ((BDD[X] × {z}))
        if i_type == 'begin':
            self._m_bdds['XY'] |= (self._m_bdds['X'] & bdd_helper_y)

        # BDD[XY] = BDD[XY] ∩ ((BDD[U] × ~{z}) ∩ (~{z} × BDD[U]))
        else:
            self._m_bdds['XY'] &= ((self._m_bdd_manager.true & ~bdd_helper_x) &
                                   (self._m_bdd_manager.true & ~bdd_helper_y))

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

        bdd_helper_y = self._m_bdd_manager.cube(i_assignment['_Y'])

        # # BDD[XYY] = BDD[XYY] ∪ (BDD[XY] ∩ (BDD[U] × {z}))
        # self._m_bdds['XYY'] |= (self._m_bdds['XY'] & (self._m_bdd_manager.true & bdd_helper_y))

        # BDD[XYY] = (BDD[XYY] ∩ !BDD[XYYX]) ∪ (BDD[XY] ∩ (BDD[U] × {z}))
        self._m_bdds['XYY'] = (self._m_bdds['XYY'] & ~self._m_bdds['XYYX']) | \
                              (self._m_bdds['XY'] & (self._m_bdd_manager.true & bdd_helper_y))

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

        bdd_helper_x = self._m_bdd_manager.cube(i_assignment['_X'])

        # BDD[XYYX] = BDD[XYYX] ∪ (BDD[XYY] ∩ ({z} × BDD[U]))
        self._m_bdds['XYYX'] |= (self._m_bdds['XYY'] & (self._m_bdd_manager.true & bdd_helper_x))

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

        bdd_helper_x = self._m_bdd_manager.cube(i_assignment['_X'])

        # # BDD[XYX] = BDD[XYX] ∪ (BDD[XY] ∩ ({z} × BDD[U])
        # self._m_bdds['XYX'] |= (self._m_bdds['XY'] & (self._m_bdd_manager.true & bdd_helper_x))

        # BDD[XYX] = (BDD[XYX] ∩ !BDD[XYX]) ∪ (BDD[XY] ∩ ({z} × BDD[U])
        self._m_bdds['XYX'] = (self._m_bdds['XYX'] & ~self._m_bdds['XYXY']) | \
                              (self._m_bdds['XY'] & (self._m_bdd_manager.true & bdd_helper_x))

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

        bdd_helper_y = self._m_bdd_manager.cube(i_assignment['_Y'])

        # BDD[XYXY] = BDD[XYXY] ∪ (BDD[XYX] ∩ (BDD[U] × {z}))
        self._m_bdds['XYXY'] |= (self._m_bdds['XYX'] & (self._m_bdd_manager.true & bdd_helper_y))

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
        bdd_helper_y = self._m_bdd_manager.cube(i_assignment['_Y'])

        # BDD[XXY] = BDD[XXY] ∪ (BDD[XX] × {z})
        if i_type == 'begin':
            self._m_bdds['XXY'] |= (self._m_bdds['XX'] & bdd_helper_y)

        # BDD[XXY] = BDD[XXY] ∩(BDD[U] × {z})
        else:
            self._m_bdds['XXY'] &= (self._m_bdd_manager.true & ~bdd_helper_y)

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

        bdd_helper_y = self._m_bdd_manager.cube(i_assignment['_Y'])

        # BDD[XXYY] = BDD[XXYY] ∪ (BDD[XXY] ∩ (BDD[U] × {z}))
        self._m_bdds['XXYY'] |= (self._m_bdds['XXY'] & (bdd_helper_y & self._m_bdd_manager.true))

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

    def _sorted_bdd_assignments(self, i_bdd: str)->list:
        """
        Get the BDD assignments using dd internal function.
        Each assignment is sort by the dictionary keys.

        Parameters
        ----------
        i_bdd : The relevant BDD name.

        Returns
        -------
        Sorted BDD assignments.

        """

        key_order = ['_D', '_X', '_Y']
        bdd_assignments = list(self._m_bdd_manager.pick_iter(self._m_bdds[i_bdd]))
        return [dict(sorted(assignment.items(), key=lambda x: key_order)) for assignment in bdd_assignments]

    ###################################################################################################################
    # This part build and creates BDDs for checking the property with the current state of the execution.
    # Those function are called according to the specification formula shape.
    ###################################################################################################################

    def rename(self, i_bdd_name: str, *new_vars: str):
        """
        rename(B,X←X′,Y←Y′,...) Replaces the bits X1,....Xn with X′1,...,X′n,
        the bits Y1,...,Yn by Y′1,...,Y′n, etc. in the BDD.

        Parameters
        ----------
        i_bdd_name : The relevant BDD name.
        new_vars : The new vars of the returned BDD.

        Returns
        -------
        renamed BDD

        """
        old_variables = ['_X', '_Y']
        values = {}
        for i, new_var in enumerate(new_vars):
            values.update(self.__variables_rename(old_variables[i], new_var, 0, self._m_interval_size))

        return self._m_bdd_manager.let(values, self._m_bdds[i_bdd_name])

    def restrict(self, i_data: str, i_variable: str):
        """
        Returns a BDD with bits X1,...,Xn that results from the BDD of the form 'XD'.
        i.e., with bits X1,...,Xn D1,...,Dm, where the data value component D1,...,Dm is z.
        This involves applying the existential quantification on the bits D1,...,Dm.

        Parameters
        ----------
        i_data : The data should be checking against the interval.
        i_variable : The relevant variable.

        Returns
        -------
        Returns a BDD with bits X1,...,Xn that results from the BDD of the form 'XD'.

        """
        bdd_renamed = self.rename("XD", i_variable)
        bdd_helper = self._m_bdd_manager.cube(self.__convert_bitstring_to_assignment(i_data, '_D'))
        return self._m_bdd_manager.exist([f'_D{i}' for i in range(self._m_data_size)], bdd_renamed & bdd_helper)

    def exist(self, i_variables: list, i_bdd: str):
        """
        Execute an "exist" quantification over a BDD.

        Parameters
        ----------
        i_variables : List of variables.
        i_bdd : The relevant BDD.

        Returns
        -------
        BDD after execution the "exist" operation.

        """
        return self._m_bdd_manager.exist([f'{variable}{i}' for variable in i_variables
                                          for i in range(self._m_data_size if variable == '_D'
                                                         else self._m_interval_size)], i_bdd)

    def forall(self, i_variables: list, i_bdd: str):
        """
        Execute an "forall" quantification over a BDD.

        Parameters
        ----------
        i_variables : List of variables.
        i_bdd : The relevant BDD.

        Returns
        -------
        BDD after execution the "forall" operation.

        """

        return self._m_bdd_manager.forall([f'{variable}{i}' for variable in i_variables
                                          for i in range(self._m_data_size if variable == '_D'
                                                         else self._m_interval_size)], i_bdd)

    ###################################################################################################################
    # This part of code is executed when the bitstring size (Interval or Data) reaches to their max size limit.
    # In this case a few update should happen to keep the order and the BDDs already created.
    # First new variables should be added into the BDD manager and then reorder them.
    # Second, all current BDDs should be reorder so they fit to the new variables where added.
    # Also the formulas in them should be updated.
    ###################################################################################################################

    def __bdd_manager_variable_expansion_update(self, i_type: str, i_new_num_of_variables: int):
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
            length_diff = i_new_num_of_variables - self._m_interval_size

            # Updating the algorithm variables should be declare on the BDD manager
            x_variables = self.__define_new_variables('_X', self._m_interval_size, i_new_num_of_variables)
            y_variables = self.__define_new_variables('_Y', self._m_interval_size, i_new_num_of_variables)

            # Updating the property variables should be declare on the BDD manager
            property_variables = []
            for variable in self.__m_property_variables:
                property_variables += self.__define_new_variables(variable,
                                                                  self._m_interval_size,
                                                                  i_new_num_of_variables)

            old_length = self._m_interval_size
            self._m_interval_size = i_new_num_of_variables
            new_vars = x_variables + y_variables + property_variables

        # In a case of the bitstring data reach to his max size.
        else:
            length_diff = i_new_num_of_variables - self._m_data_size
            d_variables = self.__define_new_variables('_D', self._m_data_size, i_new_num_of_variables)
            old_length = self._m_data_size
            self._m_data_size = i_new_num_of_variables
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

        Create a list with the variables should be added upon bitstring expansion.

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

        sorted_variables = sorted(self._m_bdd_manager.vars)

        # This line instead of of the previous if work with autoref instead CUDD
        # sorted_variables = sorted(self._m_bdd_manager.vars.keys())

        # while 'D' in sorted_variables[0]:
        #     sorted_variables.append(sorted_variables.pop(sorted_variables.index(sorted_variables[0])))

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
            variables_rename = {**self.__variables_rename('_X', '_X', i_length_diff, self._m_interval_size),
                                **self.__variables_rename('_Y', '_Y', i_length_diff, self._m_interval_size)}
            bdds = self._m_bdds.keys()

        # In a case of the bitstring data reach to his max size.
        else:
            variables_rename = self.__variables_rename('_D', '_D', i_length_diff, self._m_data_size)
            bdds = ['XD']

        # Variables substitution
        for bdd_name in bdds:
            self._m_bdds[bdd_name] = self._m_bdd_manager.let(variables_rename, self._m_bdds[bdd_name])

    def __variables_rename(self, i_old_variable: str, i_new_variable: str,
                           i_length_diff: int, i_num_of_variable: int)->dict:
        """

        Rename the variables.
        It's like a shift to right process.
        Data in old variables need to move right to the new variables.

        Parameters
        ----------
        i_old_variable : The type of the variable family ('X', 'Y' or 'D').
        i_new_variable : The new variable instead the old one.
        i_length_diff : The difference between the new size and the old size.
        i_num_of_variable : The size of the variables.

        Returns
        -------

        """

        # Create a dict which map variables into their new ones
        # Example: dict(x='p', y='q') mapping 'x' to 'p' and 'y' to 'q'.
        return {f'{i_old_variable}{i %  i_num_of_variable}':
                f'{i_new_variable}{(i + i_length_diff) %  i_num_of_variable}'
                for i in range(i_num_of_variable)}

    def __bdd_assignments_updates(self, i_type: str, i_length_diff: int):
        """
        Update the BDDs assignments so they fit to the new order upon variables resize.

        Parameters
        ----------
        i_type : 'Interval'/'Data' type.
        i_length_diff : The difference between the new size and the old size.

        Returns
        -------
        None

        """

        # In a case of the bitstring interval reach to his max size.
        if i_type == "Interval":
            x_assignment_helper = {f'_X{i}': False for i in range(i_length_diff)}
            y_assignment_helper = {f'_Y{i}': False for i in range(i_length_diff)}
            assignment_helper = {'XY': {**x_assignment_helper, **y_assignment_helper}, '_X': x_assignment_helper}
            bdds = self._m_bdds.keys()

        # In a case of the bitstring data reach to his max size.
        else:
            # The key '_X' is denote for 'D'.

            assignment_helper = {'_X': {f'_D{i}': False for i in range(i_length_diff)}}
            bdds = ['XD']

        for bdd_name in bdds:
            # Set empty BDD for store all new updated assignments
            updated_bdd = self._m_bdd_manager.false

            # Run through all BDD assignments and update them.
            for assignment in self._m_bdd_manager.pick_iter(self._m_bdds[bdd_name]):
                if bdd_name in ['X', 'XX', 'XD']:
                    updated_bdd |= self._m_bdd_manager.cube({**assignment_helper['_X'], **assignment})
                else:
                    updated_bdd |= self._m_bdd_manager.cube({**assignment_helper['XY'], **assignment})

            # Save the new updated BDD
            self._m_bdds[bdd_name] = updated_bdd




