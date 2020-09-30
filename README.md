# Simple tabulation hashing with linear probing, doubling, and halving.

A simple tabulation hashing implementation.

# How to use it
You can either import the hash_table.py file and use the class' methods or run it by passsing a input file as argument.

If you choose to give it an input file. Make sure each line has one of the following commands:

INC:x (Inserts x)

REM:x (Removes x)

BUS:x (Searches for x)

Input file example:

```txt
INC:10
INC:20
REM:10
INC:15
INC:15
REM:17
BUS:42
INC:42
INC:43
```

Here's an example of how you can do it if your input file is named input.txt: 

`python3 hash_table.py input.txt`

A file named output.txt with hashing values and table positions will be generated once you run it.
