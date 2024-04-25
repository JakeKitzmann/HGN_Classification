import time
timestamp = time.time()
while(True):
    
    current_time = time.time()
    elapsed_time = current_time - timestamp

    # Convert elapsed time to integer to truncate the decimal part
    elapsed_seconds = int(elapsed_time)

    print("Elapsed time in seconds:", elapsed_seconds)