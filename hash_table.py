#halving when 1/4 of the table is being used
#universe = 18.446.744.073.709.551.615
import numpy as np
import random

class hash_table:

    def __init__(self, c, e):
        self.q = 64
        self.p = 13
        self.c = c
        self.e = e
        self.table = []
        self.tables = []

        table_size = 2**self.c
        for i in range(0, self.c):
            self.tables.append(random.sample(range(table_size), table_size))

    def __bin(self, key):
        b = [int(i) for i in list('{0:0b}'.format(key))]

        if len(b) < self.q:
            b = [0] * (self.q - len(b)) + b
        
        if len(b) > self.q:
            raise Exception("Invalid key size.")

        #Breaks binary array into chunks of size self.c
        b = [b[i:i + self.c] for i in range(0, len(b), self.c)]

        return b

    def __int(self, b_array):
        return sum(b<<index for index, b in enumerate(b_array[::-1]))

    def __xor(self, x, y):
        return x ^ y

    def __table(self, index, key):
        return self.tables[index][key]

    def hash(self, key):
        t = None
        m = len(self.table)

        if m == 0:
            t = 0
            self.table.append(key)
        else:
            #Checks if it needs doubling
            if m + 1 >= (1 + self.e)*m:
                print("Doubling")

            bin_array = self.__bin(key)

            for index, element in enumerate(bin_array):
                if index > 0:
                    t = self.__xor(t, self.__table(index, self.__int(element)))
                elif index == 0:
                    t = self.__int(element)

            h = t % m
            i = 1
            
            #Linear probing
            while self.table[h] != None:
                h = (t + i) % m
                i = i + 1

            self.table[h] = self.key

        return t

hashing = hash_table(8, 1)
print(hashing.hash(18446744073709551615))
