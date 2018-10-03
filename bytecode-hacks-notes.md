Question: Is there a way to Sandbox Python code by disallowing some bytecode instructions targeted for the Python VM?
"Sandboxing" required here is to catch+block any calls to the underlying system ("block native code"). Any kind of File I/O, network or reading/manipulating system state should be disallowed - only thing allowed would be compute. Example program that would run correctly - calculate PI.

As a next step, want to *filter* those calls instead of block them - allow File IO to specific files.

Sub-questions:
1. CALL_FUNCTION is one such interesting PyVM instruction. How to catch/block it.
2. Will blocking CALL_FUNCTION be blocking too much? Should still be able to do a program like calculate PI. What all other operations will still be possible after blocking CALL_FUNCTION.

Interesting sidenote:
```
>>> import dis
>>> dis.dis("print('hello')")
  1           0 LOAD_NAME                0 (print)
              2 LOAD_CONST               0 ('hello')
              4 CALL_FUNCTION            1
              6 RETURN_VALUE
>>> dis.dis("print('hello', 'buffalo')")
  1           0 LOAD_NAME                0 (print)
              2 LOAD_CONST               0 ('hello')
              4 LOAD_CONST               1 ('buffalo')
              6 CALL_FUNCTION            2
              8 RETURN_VALUE
```

```
>>> def hello_world(): print("hello world")
...
>>> hello_world()
hello world
>>> dis.dis(hello_world)
  1           0 LOAD_GLOBAL              0 (print)
              2 LOAD_CONST               1 ('hello world')
              4 CALL_FUNCTION            1
              6 POP_TOP
              8 LOAD_CONST               0 (None)
             10 RETURN_VALUE
>>> eval(hello_world.__code__)
hello world
```

```
>>> def unsafe():
...   f = open("f.txt", "w")
...   f.write("hello\n")
...   f.close()
...
>>> unsafe()
>>> dis.dis(unsafe)
  2           0 LOAD_GLOBAL              0 (open)
              2 LOAD_CONST               1 ('f.txt')
              4 LOAD_CONST               2 ('w')
              6 CALL_FUNCTION            2
              8 STORE_FAST               0 (f)

  3          10 LOAD_FAST                0 (f)
             12 LOAD_ATTR                1 (write)
             14 LOAD_CONST               3 ('hello\n')
             16 CALL_FUNCTION            1
             18 POP_TOP

  4          20 LOAD_FAST                0 (f)
             22 LOAD_ATTR                2 (close)
             24 CALL_FUNCTION            0
             26 POP_TOP
             28 LOAD_CONST               0 (None)
             30 RETURN_VALUE
>>>
```

Answers:
1. Look further into *modifying* code objects. Then it boils down to  

```
a) read dis.dis(func_obj) and find for CALL_FUNCTION
b) remove_CALL_FUNCTION(func_obj)
```

or even maybe just throw an exception if any CALL_FUNCTION seen in disassembler op
2. Yes. square() using primitive operations can be calculated but even something like PI requires math.sqrt. print() requires CALL_FUNCTION.
(In fact, print also requires writing to stdout i.e. a FILE!! seccomp sandboxing may allow because STDIN maybe an already open file for the process)
