# ppds

## Eighth assignment focused on async programming

In this assignment we should choose problem, on which we would demonstrate sync/async programming/computation.
We have chosen to demonstrate this on computing sum of numbers. This program is very simple but shows difference between 
sync/async programming in nice way.

In ```main_sync.py``` file we have sync version and in ```main_async.py``` we have async version of our program.
We demonstrate longer time of computation of sum in ```compute_sum``` function byt calling ```sleep()``` in sync version
or ```asyncio.sleep()``` in async version. In ```sum_numbers``` function we print info about current sum being computed, 
and after we get result, we print it. In sync program we block computation of other sums after one of the sums is being 
computed ```total = compute_sum(numbers)```. In async program we defined function as ```async``` and we ```await``` for 
sum being computed ```total = await compute_sum(numbers)```. This allows us to compute sums faster, so one of the 
```compute_sum``` is not blocking and another one can be called. That's why for example ```medium``` sum is computed 
before ```big``` sum, even ```big``` is called first.

#### Sync version takes ```5.5 seconds``` to compute sums.
#### Async version takes about ```2.4 seconds``` to compute sums.

#### Sync program output:
![](../../../../../../var/folders/w0/6dqg01y144b142wmp_plfy8h0000gn/T/TemporaryItems/NSIRD_screencaptureui_W0j6lE/Screenshot 2022-04-19 at 09.25.22.png)

#### Async program output:
![](../../../../../../var/folders/w0/6dqg01y144b142wmp_plfy8h0000gn/T/TemporaryItems/NSIRD_screencaptureui_BtMrRF/Screenshot 2022-04-19 at 09.25.57.png)

In sync program we can see that next sum computation is called after result of previous is returned. In async program 
all the sums are called and result is being computed in async way. Medium sum is being computed before big sum, which 
is called before medium sum.