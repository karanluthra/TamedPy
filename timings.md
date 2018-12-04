```py
start = datetime.datetime.now()
driver = Driver()
driver.turnup()
print(driver.worker_queue)
ready = datetime.datetime.now()
test_basic_arith(driver)
test_basic_arith(driver)
test_basic_arith(driver)
done = datetime.datetime.now()
driver.turndown()
down = datetime.datetime.now()

print("to ready: {}".format(ready - start))
print("ready to done: {}".format(done - ready))
print("done to exit: {}".format(down - done))
```

```
(tamedpy_env) Karans-MacBook-Pro:TamedPy luthrak$ python src/driver/driver.py
new worker 9025146b-dd5a-4d42-a0f9-2fe2f3715492 coming up
<Container: 06f70a8479>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
[<__main__.Worker object at 0x10f8a4290>]
sending "START"
received "DONE"
Got Exec result from sandbox after  0:00:00.055108
sandbox execution success
connected! and ready
closing the connection, trigger sandbox cleanup
worker 9025146b-dd5a-4d42-a0f9-2fe2f3715492 cleaning up
worker 9025146b-dd5a-4d42-a0f9-2fe2f3715492 exiting
new worker af3ce554-1c05-4604-be49-f2424320f477 coming up
<Container: 626e00cfe3>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
worker 9025146b-dd5a-4d42-a0f9-2fe2f3715492 exited
[9025146b-dd5a-4d42-a0f9-2fe2f3715492] 16

sending "START"
received "DONE"
Got Exec result from sandbox after  0:00:00.036472
sandbox execution success
connected! and ready
closing the connection, trigger sandbox cleanup
worker af3ce554-1c05-4604-be49-f2424320f477 cleaning up
worker af3ce554-1c05-4604-be49-f2424320f477 exiting
new worker 84ef6196-d070-4444-818b-c1ea107dd3a1 coming up
<Container: 98c4621565>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
worker af3ce554-1c05-4604-be49-f2424320f477 exited
[af3ce554-1c05-4604-be49-f2424320f477] 16

driver turndown initiated
worker 84ef6196-d070-4444-818b-c1ea107dd3a1 turndown intiated
(tamedpy_env) Karans-MacBook-Pro:TamedPy luthrak$ clear
(tamedpy_env) Karans-MacBook-Pro:TamedPy luthrak$ python src/driver/driver.py
new worker f5ee3ac3-0032-427e-875c-290ebe52f5fd coming up
<Container: 8326b13eb2>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
[<__main__.Worker object at 0x10f0d9290>]
sending "START"
received "DONE"
Got Exec result from sandbox after  0:00:00.036934
sandbox execution success
connected! and ready
closing the connection, trigger sandbox cleanup
worker f5ee3ac3-0032-427e-875c-290ebe52f5fd cleaning up
worker f5ee3ac3-0032-427e-875c-290ebe52f5fd exiting
new worker 4bb6f233-8419-44ee-8728-c94a18f8f60a coming up
<Container: 852c8c3356>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
worker f5ee3ac3-0032-427e-875c-290ebe52f5fd exited
[f5ee3ac3-0032-427e-875c-290ebe52f5fd] 16

sending "START"
received "DONE"
Got Exec result from sandbox after  0:00:00.037778
sandbox execution success
connected! and ready
closing the connection, trigger sandbox cleanup
worker 4bb6f233-8419-44ee-8728-c94a18f8f60a cleaning up
worker 4bb6f233-8419-44ee-8728-c94a18f8f60a exiting
new worker 40b13263-19dd-4308-baf2-90a7e7520376 coming up
<Container: 5293607995>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
worker 4bb6f233-8419-44ee-8728-c94a18f8f60a exited
[4bb6f233-8419-44ee-8728-c94a18f8f60a] 16

sending "START"
received "DONE"
Got Exec result from sandbox after  0:00:00.035832
sandbox execution success
connected! and ready
closing the connection, trigger sandbox cleanup
worker 40b13263-19dd-4308-baf2-90a7e7520376 cleaning up
worker 40b13263-19dd-4308-baf2-90a7e7520376 exiting
new worker 545469d1-1ec9-4acd-9229-34ad81cb6673 coming up
<Container: 6cb845b05e>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
worker 40b13263-19dd-4308-baf2-90a7e7520376 exited
[40b13263-19dd-4308-baf2-90a7e7520376] 16

driver turndown initiated
worker 545469d1-1ec9-4acd-9229-34ad81cb6673 turndown intiated
to ready: 0:00:00.744232
ready to done: 0:00:35.734923
done to exit: 0:00:10.543997
```
After adding timeout value (0 sec) to docker.stop() (was 10 seconds by default)
More here: https://github.com/moby/moby/issues/3766

```
(tamedpy_env) Karans-MacBook-Pro:TamedPy luthrak$ python src/driver/driver.py
new worker 2e4925b8-9593-4565-8e3e-b71d38acef19 coming up
<Container: 5c61dd6e3f>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
[<__main__.Worker object at 0x104d73250>]
sending "START"
received "DONE"
Got Exec result from sandbox after  0:00:00.046184
sandbox execution success
connected! and ready
closing the connection, trigger sandbox cleanup
took 0:00:00.561710 for container.stop()
worker 2e4925b8-9593-4565-8e3e-b71d38acef19 cleaning up
worker 2e4925b8-9593-4565-8e3e-b71d38acef19 exiting
new worker ce0d98af-1161-407c-8186-c85a3924abdb coming up
<Container: d5439e8421>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
worker 2e4925b8-9593-4565-8e3e-b71d38acef19 exited
[2e4925b8-9593-4565-8e3e-b71d38acef19] 16

sending "START"
received "DONE"
Got Exec result from sandbox after  0:00:00.043019
sandbox execution success
connected! and ready
closing the connection, trigger sandbox cleanup
took 0:00:00.569350 for container.stop()
worker ce0d98af-1161-407c-8186-c85a3924abdb cleaning up
worker ce0d98af-1161-407c-8186-c85a3924abdb exiting
new worker 20120ad5-8b23-46c7-a2f3-6edddb8607b3 coming up
<Container: a325e2c2f9>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
worker ce0d98af-1161-407c-8186-c85a3924abdb exited
[ce0d98af-1161-407c-8186-c85a3924abdb] 16

sending "START"
received "DONE"
Got Exec result from sandbox after  0:00:00.045416
sandbox execution success
connected! and ready
closing the connection, trigger sandbox cleanup
took 0:00:00.680877 for container.stop()
worker 20120ad5-8b23-46c7-a2f3-6edddb8607b3 cleaning up
worker 20120ad5-8b23-46c7-a2f3-6edddb8607b3 exiting
new worker 06e006f8-7b3b-4610-aa54-d5bb17df1007 coming up
<Container: 99bb91efc1>
sending "HELLO"
received ""
closing socket
sending "HELLO"
received ""
closing socket
sending "HELLO"
received "READY"
sandbox is READY
connected! and ready
closing socket
worker 20120ad5-8b23-46c7-a2f3-6edddb8607b3 exited
[20120ad5-8b23-46c7-a2f3-6edddb8607b3] 16

driver turndown initiated
worker 06e006f8-7b3b-4610-aa54-d5bb17df1007 turndown intiated
to ready: 0:00:00.903686
ready to done: 0:00:05.728574
done to exit: 0:00:00.537034
```

Running the script with profiler `python -m cProfile src/driver/driver.py > profile.txt`
tells that the significant 5 seconds in executions are spent inside sleep -
```
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
5    0.513    0.103    0.513    0.103 {time.sleep}
```

exec_code_socket seems to be doing fine, timing wise.
Most of its time consumption is in on_container_finished, which can be offloaded to another thread/
```
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
3    0.000    0.000    5.526    1.842 driver.py:186(exec_code_socket)
3    0.000    0.000    3.769    1.256 driver.py:258(on_container_finished)
```
