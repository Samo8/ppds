# ppds

## Seventh assignment focused on scheduling coroutines

Our implementation of problem is in ```main.py``` file. In ```main()``` function, we create 2 
coroutines (functions) ```foo()``` and ```bar()```. Both functions prints text to console and 
yields value. It runs in loop for ```iteration_number``` times. If no ```iteration_numbers``` 
is passed to ```main()```, it runs infinite number of times (```sys.maxsize``` - it's not true infinity 
but for demonstration purposes its enough). Then we pass both coroutines to created ```Scheduler``` instance. 
We pass it to list/queue, so our program is easily extensible for more coroutines. In ```Scheduler``` class 
we have ```run()``` function which gets first item from ```coroutines``` list/queue, calls ```send(None)``` 
which yields value. After this coprogram is again added to list/queue. This makes sure that coroutines change 
order.
In ```main.py``` we call ```run()``` function on ```Scheduler``` object. Also we catch ```StopIteration``` exception, 
which is raised when we stop iteration. For example if ```iteration_number``` is 4, we get 4 times printed 
```I'm foo``` and 4 times ```I'm bar```. After this ```StopIteration``` is raised and ```I have reached the end``` 
is printed.