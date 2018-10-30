## Using UNIX sockets


## Using bindmounted exec folder
https://docs.docker.com/storage/bind-mounts/

Python on host machine runs within 0.06 seconds
```
Karans-MacBook-Pro:exec1 luthrak$ time python helloworld.py
Bello!
Done!
/usr/local/opt/python@2/bin:/Users/luthrak/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/luthrak/pkgs/ffmpeg-3.4.1-macos64-static/bin

real	0m0.048s
user	0m0.030s
sys	0m0.011s
Karans-MacBook-Pro:exec1 luthrak$ time python helloworld.py
Bello!
Done!
/usr/local/opt/python@2/bin:/Users/luthrak/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/luthrak/pkgs/ffmpeg-3.4.1-macos64-static/bin

real	0m0.061s
user	0m0.033s
sys	0m0.014s
Karans-MacBook-Pro:exec1 luthrak$ time python helloworld.py
Bello!
Done!
/usr/local/opt/python@2/bin:/Users/luthrak/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/luthrak/pkgs/ffmpeg-3.4.1-macos64-static/bin

real	0m0.055s
user	0m0.034s
sys	0m0.011s
Karans-MacBook-Pro:exec1 luthrak$ ls -lt
total 24
-rw-r--r--  1 luthrak  staff    6 Oct 30 11:31 out.txt
-rw-r--r--  1 luthrak  staff  213 Oct 30 11:29 helloworld.py
-rw-r--r--  1 luthrak  staff    6 Oct 15 21:48 input.txt
```
Python on bindmounted directory in container runs within 0.6 to 0.8 seconds
```
Karans-MacBook-Pro:exec1 luthrak$ time docker run -d -v /Users/luthrak/Projects/611/TamedPy/src/exec1:/tmp/py tamedpy-bindmounted
25b50890a21cf8bd8a9697e0db81efb593151b5bf51cb7b558bcd93dbfd3c4e9

real	0m0.680s
user	0m0.063s
sys	0m0.019s
Karans-MacBook-Pro:exec1 luthrak$ time docker run -d -v /Users/luthrak/Projects/611/TamedPy/src/exec1:/tmp/py tamedpy-bindmounted
9cedfc11f6706461183fbed65f4787c84ad3cc1c6382bdb766bf8c63f6cc8079

real	0m0.795s
user	0m0.070s
sys	0m0.028s
Karans-MacBook-Pro:exec1 luthrak$ time docker run -d -v /Users/luthrak/Projects/611/TamedPy/src/exec1:/tmp/py tamedpy-bindmounted
be0a304d5a313b3b6b46a30ab382f3335ebd0aeb9fef386f2f38cdd72b4896e3

real	0m0.777s
user	0m0.074s
sys	0m0.024s
Karans-MacBook-Pro:exec1 luthrak$ time docker run -d -v /Users/luthrak/Projects/611/TamedPy/src/exec1:/tmp/py tamedpy-bindmounted
50be521faad711b1f0a5e42ad4c18b10c16542bba0c650a1177d0c7ed9b63ba5

real	0m0.689s
user	0m0.063s
sys	0m0.018s
Karans-MacBook-Pro:exec1 luthrak$ time docker run -d -v /Users/luthrak/Projects/611/TamedPy/src/exec1:/tmp/py tamedpy-bindmounted
bde8457339633aa2f0c0b03e5c37fb5df4585db113351c8271856fc8d278e7ff

real	0m0.717s
user	0m0.081s
sys	0m0.020s
Karans-MacBook-Pro:exec1 luthrak$
Karans-MacBook-Pro:exec1 luthrak$ time docker run -d -v /Users/luthrak/Projects/611/TamedPy/src/exec1:/tmp/py tamedpy-bindmounted
1109c30c5370dc3bce13e5f0c77bf0b96fa90031e7fe7ee26276c8e6c738efab

real	0m0.743s
user	0m0.071s
sys	0m0.024s
```
Using `--network none` brings it down by another 0.1s
