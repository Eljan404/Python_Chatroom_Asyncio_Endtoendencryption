import time
import random

def generate_random_id():
    current_time = int(time.time() * 1000) # get current time in milliseconds
    random_number = random.randint(0, 1000000) # generate a random number between 0 and 1,000,000
    random_id = str(current_time) + str(random_number) # concatenate the current time and random number as a string
    return random_id

def generate_user_id():
    return "client"+generate_random_id()

def generate_room_id():
    return "room"+generate_random_id()