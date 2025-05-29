# Name: Jedidiah Backus
# Description: An implementation of an optimized hash map using open addressing for conflict resolution.
# Underlying data structure is a dynamic array, quadratic probing is used to find an open index for the hashed key.
# Included are methods to add or remove new elements, resize the underlying array as needed, determine the current
# number of empty buckets, get the value associated with a key, determine if a key is currently in the hash table or
# not, get an array of all key/value pairs, and clear the entire array. Also included is an iterator method that will
# ignore empty buckets, allowing for quicker iterations across the table.

# -------  CODE BETWEEN THIS LINE AND THE NEXT COMMENT LINE WERE PROVIDED FROM EXTERNAL SOURCES  ------- #

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------ CODE BELOW THIS LINE IS ORIGINAL TO ME ------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        A method for adding new key/value pairs to the hash map, if the key is already present in the hash map, the
        associated value is overwritten with the new value

        Arg: key - the key to be added
             value - the value associated with the passed key
        Returns: None
        """
        # first check the table load, if it's too high method automatically resizes the underlying array
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        # the index variable holds the index where the element should be stored
        index = self._hash_function(key) % self._capacity
        if not self._buckets.get_at_index(index) or self._buckets.get_at_index(index).is_tombstone:
            self._buckets.set_at_index(index, HashEntry(key, value))
            self._size += 1
        # if the key is already in the table, only the value is updated
        elif self._buckets.get_at_index(index).key == key:
            self._buckets.get_at_index(index).value = value
            return
        else:
            # the cr variable is used to carry out quadratic probing. the while statement loops through indexes until
            # an open one is found
            cr = 1
            index = (self._hash_function(key) + (cr ** 2)) % self._capacity
            while self._buckets.get_at_index(index) and not self._buckets.get_at_index(index).is_tombstone:
                if self._buckets.get_at_index(index).key == key:
                    self._buckets.get_at_index(index).value = value
                    return
                cr += 1
                index = (self._hash_function(key) + (cr ** 2)) % self._capacity
            self._buckets.set_at_index(index, HashEntry(key, value))
            self._size += 1


    def resize_table(self, new_capacity: int) -> None:
        """
        A method for resizing the underlying array of the hash table. If the attempted new size is smaller than the
        number of elements, method returns with no action.
        If the new size is more, it is first made prime (if that is not already the case) and that is used as the new
        size.
        All elements from the old array are rehashed and transferred to the new array

        Arg: new_capacity - the new size for the underlying array
        Returns: None
        """
        # first checks that the new capacity isn't too small for what's already in the table
        if new_capacity < self._size:
            return
        if self._is_prime(new_capacity):
            # temp is a hashmap with the new capacity, all elements are transferred over to it and then the array and
            # capacity are copied over the old ones updating self.
            temp = HashMap(new_capacity, self._hash_function)
            for bucket in range(self._buckets.length()):
                # if the tombstone is set, the element is ignored completing the removal of it
                if self._buckets.get_at_index(bucket) and not self._buckets.get_at_index(bucket).is_tombstone:
                    key = self._buckets.get_at_index(bucket).key
                    value = self._buckets.get_at_index(bucket).value
                    temp.put(key, value)
            self._buckets = temp._buckets
            self._capacity = temp._capacity
        else:
            actual_cap = self._next_prime(new_capacity)
            temp = HashMap(actual_cap, self._hash_function)
            for bucket in range(self._buckets.length()):
                if self._buckets.get_at_index(bucket) and not self._buckets.get_at_index(bucket).is_tombstone:
                    key = self._buckets.get_at_index(bucket).key
                    value = self._buckets.get_at_index(bucket).value
                    temp.put(key, value)
            self._buckets = temp._buckets
            self._capacity = temp._capacity

    def table_load(self) -> float:
        """
        A method for determining the current table load of the hash map. Calculated as "load factor" = "current
        elements" / "number of buckets"

        Arg: None
        Returns: a floating point number representing the current load factor
        """
        load = self._size / self._capacity
        return load

    def empty_buckets(self) -> int:
        """
        A method for determining how many empty buckets are in the hash table

        Arg: None
        Returns: An integer representing the number of empty buckets
        """
        # because there is only one element per index (as opposed to the chaining hash map), subtracting full buckets
        # from total buckets works for determining empty buckets.
        emptys = self._capacity - self._size
        return emptys

    def get(self, key: str) -> object:
        """
        A method for returning the value associated with a key in the hash table. If key is not present, method returns
        none

        Arg: key - the key to the value being requested
        Returns: The value associated with the key, if found. If not found, returns None
        """
        # index and cr variables are used to determine which index the requested key may be in. Loops through potential
        # indexes until it finds it or hits an empty
        index = self._hash_function(key) % self._capacity
        cr = 1
        while self._buckets.get_at_index(index):
            if self._buckets.get_at_index(index).key == key and not self._buckets.get_at_index(index).is_tombstone:
                return self._buckets.get_at_index(index).value
            else:
                index = (self._hash_function(key) + (cr ** 2)) % self._capacity
                cr += 1


    def contains_key(self, key: str) -> bool:
        """
        A method for determining if a particular key is present in the hash table. Works similar to the get method
        but returns True or False rather than a value

        Arg: key - the desired key
        Returns: True or False, depending on whether the key was found in the table or not
        """
        index = self._hash_function(key) % self._capacity
        cr = 1
        while self._buckets.get_at_index(index):
            if self._buckets.get_at_index(index).key == key:
                return True
            else:
                index = (self._hash_function(key) + (cr ** 2)) % self._capacity
                cr += 1
        return False

    def remove(self, key: str) -> None:
        """
        A method for removing an element from the hash map, element's tombstone is set and element will be overwritten
        by the next new element that could go in its index

        Arg: key - the key of the element to be removed
        Returns: None
        """
        index = self._hash_function(key) % self._capacity
        cr = 1
        while self._buckets.get_at_index(index):
            # rather than actually removing anything, the tombstone is set essentially marking it to be overwritten
            # and keeping an unexpected blank index from messing with finding or removing other elements
            if self._buckets.get_at_index(index).key == key and not self._buckets.get_at_index(index).is_tombstone:
                self._buckets.get_at_index(index).is_tombstone = True
                self._size -= 1
                return
            elif self._buckets.get_at_index(index).key == key and self._buckets.get_at_index(index).is_tombstone:
                return
            else:
                index = (self._hash_function(key) + (cr ** 2)) % self._capacity
                cr += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        A method for returning an array of all key/value pairs in the hash map

        Arg: None
        Returns: A dynamic array containing all the key/value pairs
        """
        final = DynamicArray()
        for bucket in range(self._buckets.length()):
            if self._buckets.get_at_index(bucket) and not self._buckets.get_at_index(bucket).is_tombstone:
                # the pair variable holds a tuple of the key and value for each element in the hash map
                pair = self._buckets.get_at_index(bucket).key, self._buckets.get_at_index(bucket).value
                final.append(pair)
        return final

    def clear(self) -> None:
        """
        A method to clear all the contents of the hash map without changing its capacity

        Arg: None
        Returns: None
        """
        # cycles through all indexes and removes all elements found
        for bucket in range(self._buckets.length()):
            if self._buckets.get_at_index(bucket):
                self._buckets.set_at_index(bucket, None)
        self._size = 0


    def __iter__(self):
        """
        An iterator method for the hash map.
        """
        self._index = 0

        return self

    def __next__(self):
        """
        A next method to be used with the iterator, allowing iteration through the hash map
        """
        try:
            # if there is no element at the index, it is advanced. Ensures the iterator only returns current elements
            while not self._buckets.get_at_index(self._index) or self._buckets.get_at_index(self._index).is_tombstone:
                self._index += 1
            element = self._buckets.get_at_index(self._index)
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return element


# ------------------- BASIC TESTING WAS PROVIDED FROM EXTERNAL SOURCES - NOT MY WORK ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        # print(m)
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
