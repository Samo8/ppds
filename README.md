# ppds

## Fourth assignment focused on nuclear power plant problem

We have 3 .py files. In philosoph.py is just code from lecture rewritten for purposes of learning
for later, with no documentation/PEP8/PEP257.

main.py file is rewritten pseudocode from lecture of nuclear power plant 1 assignment. There we have 11
sensors which are writing its data to 2 monitors. Every sensor takes 10-15 ms to update its data.
Data on the monitors update every 500ms and updated data should be shown up to 200ms. Monitors show data
after at least one sensor writes data to storage.

main2.py file is implementation of nuclear power plant 2 assignment. There we have 3 sensors. 2 sensors update
data in range of 10-15ms and the third one in range of 20-25ms. Every sensor has its own data storage, so they
can't rewrite data of another sensor. Every sensor update data each 50-60ms. Then we have 9 monitors, which 
are showing data from sensors. Monitors are updating all the time and update of data takes 40-50ms. Monitors
should start to work after there are data in storage from all sensors. As we are using Lightswitch for sensors
and monitors which share one semaphore, this is what makes this possible. Only after third sensor calls unlock on
LS, semaphore in LS could be taken by LS in monitors. Also in our implementation, we used turnstile, to make
2 categories of objects (sensors, monitors) to work properly. There is always one category which has and advantage,
because there is no possibility to make both categories "same".
Current number of reading monitors is take from lock() function in LS object. there we return current counter value.

Pseudo code:

```commandline
def init():
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    valid_data = Event()
 
    for monitor_id in (0,7):
        create_and_run_thread(monitor, monitor_id)
    for sensor_id in (0,2):
        create_and_run_thread(sensor, sensor_id)
 
def monitor(monitor_id):
    valid_data.wait()
 
    while True:
        read_duration = rand(40 to 50 ms)
        sleep(read_duration)
 
        turnstile.wait()
        number_of_reading_monitors = ls_monitor(access_data).lock()
        turnstile.signal()
 
        print('monit "%02d": number_of_reading_monitors: %02d read_duration:%02d\n')
        ls_monitor(access_data).unlock()
 
def sensot(sensor_id):
    while True:
        sleep_time = rand(50 to 60 ms)
        sleep(sleep_time)
        
        turnstile.wait()
        number_of_writing_sensors = ls_sensor(acess_data).lock()
        turnstile.signal()
        
        if sensors_id is equal to 2
            write_duration = rand(20 to 25 ms)
        else
            write_duration = rand(10 to 20 ms)
 
        print('sensor "%02d":  number_of_writing_sensors=%02d, write_duration=%03d\n')
        sleep(write_duration)
        valid_data.signal()
        ls_sensor(access_data).unlock()
```

