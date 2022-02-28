# ppds
## First assignment focused on barrier
### Runs on Python 3.8.0

We have 2 .py files, main.py corresponds to task number 1 from practice 
and main2.py corresponds to task number 3.

##### main.py
The purpose of this task was to change Semaphore to Event in context of using barrier sync tool.
in the wait() function we use mutex to lock critical part. There is almost no difference in use of
Semaphore of Event except of calling clear() while using event. clear() method allows us to reuse
event. After calling clear() all wait() calls would be blocking again until calling signal()/set() again.
All threads reaching wait() function waits until last tread reaching wait() function. Last thread calls signal()
function which "unblocks" all threads which called wait(). After all threads being unblocked we have to call clear()
to make next wait() calls being blocking again. The wait() call could be done only by last thread, I checked the implementation
and calling wait() only sets value of bool flag. We could implement same approach checking if we are at the last thread but from my
perspective this approach would be same from performance point of view.