# ppds

## Fifth assignment focused on savages problem

We have 3 .py files. In main.py file is just code from lecture rewritten for purposes of learning for 
later. In main2.py file is savages 1 solution, rewritten from pseudocode. Both files have no documentation/
PEP8/PEP257.

main3.py is implementation of savages 2 task. Purpose of this task was to rewrite savages 1 task. Now we 
have more cooks, which are helping each other to cook meals for savages. Only one cook can add meals to pot.
We choose that last cook will put meals to pot. We make this work by using SimpleBarrier with some modifications. 
SimpleBarrier object is created with cooks_number cooks, who are cooking for savages. Inside wait()
function, we have counter which we increase by one on ich wait() call. When count is same as cooks_number - 
so the last cook called wait(), we signal that pot is full through full_pot Semaphore. This is work done by cooks 
inside cook() function. In savage() function we are checking if there are no servings left. If there are no 
servings inside the pot, savage signals through Event empty_pot, that pot is empty. This is how we make sure, 
that all cooks will start cooking, because there is wait() call on empty pot inside cook() function. Also 
savage who discovers that pot is empty, mus wait until cooks fulfil the pot by calling full_pot.wait(). In 
the main function we create N Threads representing savages, cooks_number Threads representing cooks. Cooks 
make M portion, and as mentioned earlier, only one cook (the last one) puts portions to pot.

Pseudo code:

```commandline
def init(m):
    mutex := Mutex()
    servings := m 
    empty_pot := Event()
    full_pot := Semaphore(0)
 
    b_cook := SimpleBarrier(cooks_number)
 
    for savage_id in [0, 1, 2, ..., N-1]:
        create_and_run_thread(savage, savage_id)
    for cook_id in [0, 1, 2, ..., cooks_number-1]:
        create_and_run_thread(cook, cook_id)
        
def eat(i):
    print('savage %2d: eat start', i)
    sleep(rand(50 to 200 ms))
    print('savage %2d: eat end', i)
 
def savage(savage_id):
    sleep(rand(10 to 100 ms))
    while True:
        mutex.lock()
        if servings == 0:
            print('savage %2d: empty pot', savage_id)
            empty_pot.signal()
            empty_pot.clear()
            full_pot.wait()
        print(savage %2d: take from pot', savage_id)
        sevings -= 1
        mutex.unlock()
        eat(i)
 
def cook():
    while True:
        empty_pot.wait()
        
        print('cook %2d cooking, i)
        sleep(50 ms)
        print('cook %2d servings --> pot, i)
        
        b_cook.wait(shared)
```