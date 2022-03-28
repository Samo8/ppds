# ppds

## Sixth assignment focused on barbershop problem

Our implementation is in ```main.py``` file. In our problem we crate ```MAX_CUSTOMERS``` threads
for customers and one tread for barber. ```N``` represents maximum number of customers who can be 
in barbershop. If ```MAX_CUSTOMERS``` if bigger than ```N```, we could simulate that customer can't 
get into barbershop and leaves. Only one customer can have a haircut at the time. We simulate haircut by
2 functions ```get_hair_cut``` on customer side and ```cut_hair``` on barber side. In ```Shared``` class 
we have ```Semaphore``` for customer - representing customer, customer_done - representing that customer is done 
and barber_done - representing that barber finished haircut. We do not use FIFO Semaphore, so we implemented 
queue of barbers for each customer, so that first customer who came to barbershop would get haircut. 
Also we have to use ```Mutex``` to protect critical part, which is increasing/decreasing number of customers and 
adding/removing from barbers queue. We added function ```grow_hair``` to simulate hair growing. Function helps us 
to prevent that if we have more customer Threads than spaces in barbershop, so there wouldn't be customers tyring 
to get into barbershop all the time. When barber is "sleeping" we wake him up with customer Semaphore.