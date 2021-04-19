import numpy as np


class BitstringTable:
    def __init__(self, i_bitstring_length=3, i_expansion_length=2):
        self.__m_bitstring_table = {}
        self._m_bitstring_length = i_bitstring_length
        self.__m_number_of_growth = i_expansion_length
        self.__max_items_allowed = 2 ** i_bitstring_length

    def lookup(self, i_event_type: str, i_key)->str:
        """
        Lookup on the bitstring table. If the key already appear it returns it's value,
        otherwise it create new entry and return the value.

        Parameters
        ----------
        i_event_type : The type of the event ("begin", "end" or "data").
        i_key : The key variable before it converted into bitstring.

        Returns
        -------
        The representation of the key in bitstring.

        """

        # Update occur when it reached to bitstring length limit.
        # The new size is the old size with 2 more bits
        if i_event_type == 'begin' and len(self.__m_bitstring_table.keys()) >= self.__max_items_allowed:
            self.__length_update(self._m_bitstring_length + self.__m_number_of_growth)

        # Set the value of the bitstring to be equal to the number of new keys have been watched until now
        # The counting start from 0.
        if i_key not in self.__m_bitstring_table.keys():
            self.__m_bitstring_table[i_key] = np.binary_repr(len(self.__m_bitstring_table.keys()),
                                                             width=self._m_bitstring_length)
        return self.__m_bitstring_table[i_key]

    def lookup_no_update(self, i_key):
        """
        Lookup on the bitstring table without updating.
        Just query the dictionary.

        Parameters
        ----------
        i_key : The key variable before it converted into bitstring.

        Returns
        -------
        The representation of the key in bitstring if key exist, other wise False.

        """

        if i_key not in self.__m_bitstring_table.keys():
            return False
        return self.__m_bitstring_table[i_key]


    def __length_update(self, i_new_length: int):
        """
        Update bitstring length when a larger bitstring length is needed.

        Parameters
        ----------
        i_new_length : The size of the new bitstring length.

        Returns
        -------
        None

        """

        # Create 0's prefix padding in a szie of the defined growth.
        prefix = '0' * (i_new_length - self._m_bitstring_length)
        self._m_bitstring_length = i_new_length

        # Update all values seen with the prefix.
        for key, bitstring in self.__m_bitstring_table.items():
            self.__m_bitstring_table[key] = f'{prefix}{bitstring}'
        self.__max_items_allowed_update()

    def __max_items_allowed_update(self):
        """
        Update the maximal items allowed before the bitstring length should be updated.

        Returns
        -------
        None

        """
        self.__max_items_allowed = self._m_bitstring_length ** 2 - 1
