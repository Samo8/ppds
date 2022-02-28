# ppds
## First assignment focused on barrier
### 🐍 Runs on Python 3.8.0 🐍

We have 2 .py files, main.py corresponds to task number 1 from practice 
and main2.py corresponds to task number 3.

### main.py
The purpose of this task was to change Semaphore to Event in context of using barrier sync tool.
In the wait() function we use mutex to lock critical part. There is almost no difference in use of
Semaphore of Event except of calling clear() while using event. clear() method allows us to reuse
event. After calling clear() all wait() calls would be blocking again until calling signal()/set() again.
All threads reaching wait() function waits until last tread reaching wait() function. Last thread calls signal()
function which "unblocks" all threads which called wait(). After all threads being unblocked we have to call clear()
to make next wait() calls being blocking again. The wait() call could be done only by last thread, I checked the implementation
and calling wait() only sets value of bool flag. We could implement same approach checking if we are at the last thread but from my
perspective this approach would be same from performance point of view.


### main2.py

The purpose of this task was to create function which will compute fibonacci sequence using Semaphore/Event.
Every number of fibonacci sequence should be computed after its predecessor has been computed. We should come up
with solution that runs with use of Semaphore or Event without change in code logic. We used sample code from lecture.
We moved list representing fibonacci sequence to Adt class, there we create list of size 2 + N(number of threads). First two
numbers are hard-coded to 0 and 1. Then we need N more elements, each one corresponding to one thread. Then we created N+1
Semaphores/Events. We need N+1 for the case of last thread calling signal() on i+1 semaphore in compute_fibonacci function.
All fibonacci numbers (except first two) are computed as sum of its two predecessors. The current index (i - goes from 0 to THREADS)
calls compute_fibonacci function. There we call wait() for Semaphore/Event at i index, compute i+2 fibonacci number and then call signal()
for next (i+1) Semaphore/Event, signaling that next fibonacci number can now be computed. We also have to call signal() on first element
of our Semaphores/Events list, to prevent "deadlock".


### Questions

1. In our solution there was need to use N+1(N being number of threads) Semaphores/Events. I explained the N+1 above. There was no need to 
use another sync. tool for example mutex.
2. We tried to come up with another solution as the one that is implemented, but probably lack of experience with
parallel programming leaded to no another functional solution.
Maybe there is chance of using barrier, but I'm not sure if in meaningful way.
I could image using barrier, and it would wait not for some count being reached as it is used most way, but for result of previous
fibonacci sequence numbers being computed.
```
