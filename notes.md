## Problem Statement and Inspiration
### From [CSE662 2018 page](https://odin.cse.buffalo.edu/teaching/cse-662/2018fa/index.html):
The aim of this seed is to design a lightweight wrapper around Python that: (1) Allows python code to be executed without risk to the underlying platform, (2) Allows computation inputs to be delivered to the executing python through some narrow interface, and (3) Allows computation results to be exported through some narrow interface. 

### From [Issue](https://github.com/VizierDB/web-api/issues/2) filed on VizierDB's Github:
If we're going to rely on Python as heavily as we do, it needs to be executed in a sandboxed context.

### From Oliver's [Project Seed Slides](https://odin.cse.buffalo.edu/slides/cse662fa2018/2018-08-29-Seeds.html#/5):
![Alt description](https://odin.cse.buffalo.edu/slides/cse662fa2018/graphics/2018-08-29-Sandbox-Real.svg). 

You get - 
* Python Code
* Inputs to the code (or a socket)

Your system produces
* Output for the code...
* without calling out of the sandbox. 

#### Things to Think About
What security guarantees are you providing?
How can you prove to yourselves that those guarantees are enforced?
What tooling can you use to wrap/execute python?

### From 1:1 with Oliver
* Emphasize on how to assure and prove that the sandboxing works correctly.
* Read further about PyPy's sandboxing
* Read about Codepad and other online code execution projects
* Happy to take "Run it within Docker" as a solution if turning up a docker is a sub-second task.

# Solutions/Discussions on the Web
https://wiki.python.org/moin/SandboxedPython  
https://stackoverflow.com/questions/3068139/how-can-i-sandbox-python-in-pure-python

# Interesting Existing Projects
* REPL it: https://repl.it/repls/AcclaimedQualifiedWordprocessing  
* EDX's CodeJail, uses AppArmor: https://github.com/edx/codejail
* restricted in py 2's stdlib: https://docs.python.org/2/library/restricted.html check if doable in py3. https://docs.python.org/3.6/reference/executionmodel.html?highlight=restricted
* RestrictedPython (seems 3rd party) https://restrictedpython.readthedocs.io/en/latest/upgrade/index.html
* PyPy's built in sandboxing: http://doc.pypy.org/en/latest/sandbox.html Using PyPy would be another open n shut solution but most users would want to stick to CPython (major audience is data scientists, most libs are built with CPython in mind)
* SecComp linux kernel level sandbox that limits syscalls: https://code.google.com/archive/p/seccompsandbox/wikis/overview.wiki
* Unexpected Py in the wild - PyCage https://pypi.org/project/PYCage/
