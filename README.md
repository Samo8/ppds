# ppds

## First assignment focused on threads

### Runs on Python 3.8.0

##### We have 3 uses of mutex lock, each is in separate main{number}.py file

##### main.py
In this approach we used mutex lock to lock code inside while loop, and we used unlock at the end of each
iteration. This solution uses mutex.lock()/mutex.unlock() as many times as we iterate in while loop.
We have to use mutex.unlock() also in condition when ending while loop, because we start iteration with 
mutex.lock(), so there is need to call mutex.unlock(). 

##### main2.py
In the second solution we used mutex lock to lock just critical part of do_count function, which is increasing
elms element value and increasing counter. mutex.lock()/mutex.unlock() is used in every while loop iteration.
We also need to increase size by one at line number 10, to avoid overflow. There is possible overflow when in
the last iteration both threads jump into the loop and the second thread increases value after reaching maximum
by first thread.

##### main3.py
In this solution we locked whole body of do_count function, to prevent second thread changing critical part 
of code. This solution is the most performant one, because we use mutex.lock()/mutex.unlock() just one time.