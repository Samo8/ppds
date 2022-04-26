# ppds

## Ninth assignment focused on cuda programming

In this assignment we should demonstrate use of Cuda device.

In ```main.py``` file we have simple program which computes sums of lists. We generate ```256``` lists of numbers 
which contains numbers from ```1``` to ```random(8000, 10 000)```. We have ```8``` threads per block and ```32``` blocks. 
Results are saved in ```results``` list. After computing sums of list we print results to console. 