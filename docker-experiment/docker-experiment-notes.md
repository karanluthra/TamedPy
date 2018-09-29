## Exp 0
Try run https://github.com/christophetd/docker-python-sandbox as is.

Output:
```
{ timedOut: true,
  isError: true,
  stderr: '',
  stdout: '',
  combined: ''
}
```
TODO: Run on a linux box; because "It has also been reported that the library doesn't work properly on Mac for an unknown reason."

## Exp 1
Spin a single docker container programmatically from Python, run a trivial python code in container and shut it down. Note time taken for each stage.

1.1 Hello World packaged inside the docker image

First, ran using the normal python base

Dockerfile:
```
FROM python:3

ADD helloworld.py /

CMD [ "python", "./helloworld.py" ]
```
```
Karans-MacBook-Pro:docker-experiment luthrak$ docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
tamedpy                       latest              853dc8a4a51e        2 hours ago         923MB
```
```
import docker

client = docker.from_env()
print(client.containers.run("tamedpy"))
```

```
Karans-MacBook-Pro:docker-experiment luthrak$ time python docker-if.py
b'Hello World!\n'

real	0m1.464s
user	0m0.231s
sys	0m0.054s
Karans-MacBook-Pro:docker-experiment luthrak$ time python docker-if.py
b'Hello World!\n'

real	0m1.689s
user	0m0.289s
sys	0m0.099s
Karans-MacBook-Pro:docker-experiment luthrak$ time python docker-if.py
b'Hello World!\n'

real	0m1.514s
user	0m0.247s
sys	0m0.057s
Karans-MacBook-Pro:docker-experiment luthrak$ time python docker-if.py
b'Hello World!\n'

real	0m1.557s
user	0m0.241s
sys	0m0.054s
```

----------
Next, tried reducing docker image size by using `FROM python:3-alpine`

Image size reduced substantially, good!
```
Karans-MacBook-Pro:tamedpy-dockimg luthrak$ docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
tamedpy                       latest              bcc16ad04e1a        6 seconds ago       78.1MB
```

```
Karans-MacBook-Pro:docker-experiment luthrak$ time python docker-if.py
b'Hello World!\n'

real	0m1.852s
user	0m0.302s
sys	0m0.129s
Karans-MacBook-Pro:docker-experiment luthrak$ time python docker-if.py
b'Hello World!\n'

real	0m1.694s
user	0m0.269s
sys	0m0.088s
Karans-MacBook-Pro:docker-experiment luthrak$ time python docker-if.py
b'Hello World!\n'

real	0m2.126s
user	0m0.226s
sys	0m0.051s
Karans-MacBook-Pro:docker-experiment luthrak$ time python docker-if.py
b'Hello World!\n'

real	0m1.533s
user	0m0.231s
sys	0m0.056s
Karans-MacBook-Pro:docker-experiment luthrak$ time python docker-if.py
b'Hello World!\n'

real	0m1.493s
user	0m0.246s
sys	0m0.072s
```
----------------
Splitting `docker run` into `docker create` and `docker start -ai`
https://serverfault.com/questions/897619/docker-startup-time
```
Karans-MacBook-Pro:docker-experiment luthrak$ time docker create tamedpy
8b537019345e1743b26764931aad7f85f2417e526ee3a532cecadd478f8ba002

real	0m0.506s
user	0m0.081s
sys	0m0.121s
Karans-MacBook-Pro:docker-experiment luthrak$ docker ps -ql
8b537019345e
Karans-MacBook-Pro:docker-experiment luthrak$ time docker start -ai 8b537019345e
Hello World!

real	0m1.464s
user	0m0.084s
sys	0m0.115s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker start -ai 8b537019345e
Hello World!

real	0m1.114s
user	0m0.077s
sys	0m0.032s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker start -ai 8b537019345e
Hello World!

real	0m1.116s
user	0m0.072s
sys	0m0.033s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker start -ai 8b537019345e
Hello World!

real	0m1.131s
user	0m0.074s
sys	0m0.038s
```

`docker start` takes only ~1.1s  

--------------------
Running `docker run --network none` brings it down to ~1s too

```
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run --network none tamedpy
Hello World!

real	0m0.941s
user	0m0.079s
sys	0m0.029s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run --network none tamedpy
Hello World!

real	0m1.048s
user	0m0.089s
sys	0m0.028s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run --network none tamedpy
Hello World!

real	0m0.991s
user	0m0.071s
sys	0m0.037s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run --network none tamedpy
Hello World!

real	0m1.025s
user	0m0.098s
sys	0m0.034s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run --network none tamedpy
Hello World!

real	0m1.003s
user	0m0.080s
sys	0m0.031s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run --network none tamedpy
Hello World!

real	0m0.993s
user	0m0.075s
sys	0m0.035s
```

----------------------

Running with `-d` detatched mode brings it down much to 0.7-0.8s!

```
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run -d tamedpy
91a8a6c53b44e81f4454fa46564c6ba235f6d048fa39441f8eaf2abe93b3e25d

real	0m0.715s
user	0m0.078s
sys	0m0.031s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run -d tamedpy
de663b19cb92919512f7fbef3c91c2b1054408b07ad8cf48816e0dc877d9cb74

real	0m0.735s
user	0m0.079s
sys	0m0.030s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run -d tamedpy
f9ae74f1f2efe899a076a09eca59efce1964fd5047789cd832983382556160c5

real	0m0.751s
user	0m0.078s
sys	0m0.032s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run -d tamedpy
9511f62daa9c936f185ea4978de93cb0a08d50bb1524ba573c23d6c35f5ccf6d

real	0m0.729s
user	0m0.082s
sys	0m0.034s
Karans-MacBook-Pro:docker-experiment luthrak$ time docker run -d tamedpy
af4c4f516285d71b0841ce113c4c36887ad37a777eea99bd77afcbd088a39ad2

real	0m0.770s
user	0m0.084s
sys	0m0.030s
```
