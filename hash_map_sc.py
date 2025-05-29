# Name: Jedidiah Backus
# Description: An implementation of an optimized hash map using chaining for conflict resolution. Underlying
# data structure is a dynamic array, with singly linked lists at each index. Implementation includes methods to add
# or remove elements from the hash map, resize, determine the table load, view the number of empty buckets,
# get the value for a key determine if the hash map contains a key, get an array comprised of all key-value pairs,
# and empty the entire hash map. also includes a function for finding the mode of a dynamic array utilizing the has
# map functionality.

# ------- CODE BETWEEN THIS LINE AND THE NEXT COMMENT LINE WERE PROVIDED FROM EXTERNAL SOURCES ------- #

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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

    # --------------------------- CODE BELOW THIS LINE IS ORIGINAL TO ME --------------------------------------- #

    def put(self, key: str, value: object) -> None:
        """
        A method for adding new key/value pairs to the hash map. If the key already exists, the value is overwritten
        with the new value.

        Arg: key - a string as the key in the key/value pair
             value - the value in the key/value pair
        Returns: None
        """
        # the bucket variable is calculated as the index where the key should be stored based on the hash function
        bucket = self._hash_function(key) % self._capacity
        # prior to any other action, the table load is checked and if it is 1 or more, the underlying array is resized
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)
            bucket = self._hash_function(key) % self._capacity
        # this if statement checks, if the key is already in the hash map, if so updates the value, if not adds it
        if self._buckets.get_at_index(bucket).contains(key):
            self._buckets.get_at_index(bucket).contains(key).value = value
        else:
            self._buckets.get_at_index(bucket).insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        A method to resize the current hash table when the load factor is becoming too large. Takes the desired new
        capacity and uses the next prime number as the actual new capacity

        Arg: new_capacity - the desired new capacity
        Returns: None
        """
        # first checks that the attempted new size is at least 1, if not returns without any changes
        if new_capacity < 1:
            return
        # this if statement checks if the new size is already a prime, if not finds the next closest prime to use
        if self._is_prime(new_capacity):
            # the temp variable will ultimately be the underlying array for the hash map
            temp = DynamicArray()
            # checks that the new capacity is big enough for current elements, builds the new array, and then transfers
            # all the elements from the old array
            while new_capacity < self._size:
                new_capacity = self._next_prime(new_capacity * 2)
            for each in range(new_capacity):
                temp.append(LinkedList())
            for bucket in range(self._capacity):
                if self._buckets.get_at_index(bucket).length() != 0:
                    for node in self._buckets.get_at_index(bucket):
                        temp.get_at_index(self._hash_function(node.key) % new_capacity).insert(node.key, node.value)
            self._buckets = temp
            self._capacity = new_capacity
        else:
            # the actual_cap variable is the next prime number after the passed new size. all other comments from above
            # apply below
            actual_cap = self._next_prime(new_capacity)
            temp = DynamicArray()
            while actual_cap < self._size:
                actual_cap = self._next_prime(actual_cap * 2)
            for each in range(actual_cap):
                temp.append(LinkedList())
            for bucket in range(self._capacity):
                if self._buckets.get_at_index(bucket).length() != 0:
                    for node in self._buckets.get_at_index(bucket):
                        temp.get_at_index(self._hash_function(node.key) % actual_cap).insert(node.key, node.value)
            self._buckets = temp
            self._capacity = actual_cap




    def table_load(self) -> float:
        """
        A method for calculating the current load factor of the hash table. Calculated as "load factor" = "current
        elements" / "number of buckets"

        Arg: None
        Returns: A floating point number, representing the current load factor
        """
        load = self._size / self._capacity
        return load

    def empty_buckets(self) -> int:
        """
        A method for determining how many buckets in the hash map are currently empty.

        Arg: None
        Returns: an integer representing the number of empty buckets
        """
        # final variable holds the count of empty buckets, for loop cycles through each index of the underlying array
        # checking the length of the linked lists
        final = 0
        for bucket in range(self._capacity):
            if self._buckets.get_at_index(bucket).length() == 0:
                final += 1
        return final

    def get(self, key: str):
        """
        A method for returning the value associated with a passed key.

        Arg: key - the key of the desired value
        Returns: the value associated with the passed key
        """
        # bucket variable is the index that the key would be stored at
        bucket = self._hash_function(key) % self._capacity
        # for loop cycles through nodes of the linked list at the proper index, if the key of one matches the passed key
        # the associated value is returned
        for node in self._buckets.get_at_index(bucket):
            if node.key == key:
                return node.value

    def contains_key(self, key: str) -> bool:
        """
        A method for determining if the hash map contains a certain key.

        Arg: key - the desired key
        Returns: True if the key is already in the hash map, False if not.
        """
        # first check that there are at least some values, if not, automatically returns
        if self._size == 0:
            return False
        # bucket variable is the index that the key would be stored at
        bucket = self._hash_function(key) % self._capacity
        # uses the contains method of the linked list to determine if the key is present, returns False if not
        if self._buckets.get_at_index(bucket).contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        A method for removing a key/value pair from the hash map. If the passed key does not exist in the hash map,
        method does nothing.

        Arg: key - the key to be removed
        Returns: None
        """
        # bucket variable is the index that the key would be stored at
        bucket = self._hash_function(key) % self._capacity
        # uses remove method of the linked list, if successful size is reduced
        if self._buckets.get_at_index(bucket).remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        A method for returning all the key/value pairs in the hash map. Places them in a Dynamic Array.

        Arg: None
        Returns: A dynamic array containing all the key/value pairs from the hash map
        """
        # final variable is a dynamic array that will contain all key/value pairs
        final = DynamicArray()
        for bucket in range(self._capacity):
            if self._buckets.get_at_index(bucket).length() != 0:
                # for loop cycles through each node in the bucket and adds the key and value to the element variable
                # before adding it to the final array
                for node in self._buckets.get_at_index(bucket):
                    element = node.key, node.value
                    final.append(element)
        return final
    def clear(self) -> None:
        """
        A method for clearing the hash map, removes all values without changing the capacity.

        Arg: None
        Returns: None
        """
        # for loop cycles through each bucket in the hash map and checks if the bucket contains nodes
        for bucket in range(self._capacity):
            # if the bucket isn't already empty, a new empty linked list is saved over the old one
            if self._buckets.get_at_index(bucket).length() != 0:
                self._buckets.set_at_index(bucket, LinkedList())
            self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    A function for finding the most commonly occurring element(s) in an array. Returns a tuple containing the element(s)
    and an integer representing the number of times the element was found.

    Arg: da - the array for which the mode is desired
    Returns: A tuple containing the most common element(s) and the number of times they were found
    """
    # map variable is a hashmap used to store the count of each element, elements from the array are keys the number of
    # times it was found is the associated value
    map = HashMap()
    for each in range(da.length()):
        if not map.contains_key(da.get_at_index(each)):
            count = 1
            map.put(da.get_at_index(each), count)
        else:
            count = map.get(da.get_at_index(each)) + 1
            map.put(da.get_at_index(each), count)
    final_key = DynamicArray()
    final_val = 0
    k_v = map.get_keys_and_values()
    # once all elements are added to the map, the map is gone through looking for the elements with the largest value
    for each in range(k_v.length()):
        if k_v.get_at_index(each)[1] > final_val:
            final_key = DynamicArray()
            final_key.append(k_v.get_at_index(each)[0])
            final_val = k_v.get_at_index(each)[1]
        elif k_v.get_at_index(each)[1] == final_val:
            final_key.append(k_v.get_at_index(each)[0])
    return final_key, final_val



# ------------------- BASIC TESTING BELOW THIS LINE WAS PROVIDED FROM EXTERNAL SOURCES ---------------------------------------- #

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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    print(m)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
