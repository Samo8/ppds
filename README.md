# ppds

## Seventh assignment focused on scheduling coprograms

Our implementation of problem is in ```main.py``` file. In ```main()``` function, we create 2 
coprograms (functions) ```foo()``` and ```bar()```. Both functions prints text to console and 
yields value. It runs in loop for ```iteration_number``` times. If no ```iteration_numbers``` 
is passed to ```main()```, it runs infinite number of times (```sys.maxsize``` - it's not true infinity 
but for demonstration purposes its enough). Then we pass both coprograms to created ```Scheduler``` instance. 
We pass it to list/queue, so our program is easily extensible for more coprograms. In ```Scheduler``` class 
we have ```run()``` function which gets first item from ```coprograms``` list/queue, calls ```send(None)``` 
which yields value. After this coprogram is again added to list/queue. This makes sure that coprograms change 
order.
In ```main.py``` we call ```run()``` function on ```Scheduler``` object. Also we catch ```StopIteration``` exception, 
which is raised when we stop iteration. For example if ```iteration_number``` is 4, we get 4 times printed 
```I'm foo``` and 4 times ```I'm bar```. After this ```StopIteration``` is raised and ```I have reached the end``` 
is printed.