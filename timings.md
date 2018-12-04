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
