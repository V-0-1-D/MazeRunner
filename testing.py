'''
MazeRunner.py

Programmers: Jeremy Juckett, 

Modified:
    Jeremy Juckett (11-25-2022), started main(), started line_follow();

    Jeremy Juckett (11-28-2022), started test_rgbi_reading();

    Jeremy Juckett (11-29-2022), finished test_rgbi_reading(),
    defined color-interval lists, in_interval(), add simple_line_follow();

'''

from spike import ColorSensor, PrimeHub, LightMatrix, Motor, MotorPair, DistanceSensor
from spike.control import wait_for_seconds
from math import pi, ceil

'''
Initialize module-level variable.
Pins are subject to change.
'''
WHEEL_RADIUS = 3 # cm
WALL_DISTANCE = 10 # cm
SLOW_SPEED = 25
FAST_SPEED = 75

hub = PrimeHub()
lm = LightMatrix()
right_distance_sensor = DistanceSensor('A')
forward_distance_sensor = DistanceSensor('B')
left_color_sensor = ColorSensor('F')
right_color_sensor = ColorSensor('E')
mp = MotorPair('C', 'D')
left_motor = Motor('C')
right_motor = Motor('D')

left_motor.set_default_speed(-50)
right_motor.set_default_speed(50)


# [low, high]
black_interval = [200, 400] # Used for default speed line following
red_interval = [1300, 1499] # goal
yellow_interval = [1700, 1999] # used for slow line-following
green_interval = [1100, 1400] # used for fast line-following
white_interval = [2000, 2100] # used for default driving surface
orange_interval = [1500, 1699]
purple_interval = [500, 700]


'''
magnitude(vector)

Computes and returns the magnitude of the given collection of values.

Jeremy Juckett, 
'''
def magnitude(vector):
    sum = 0
    for v in vector:
        sum = sum + v ** 2
    return sum ** (1/2)


'''
simple_line_follow()

This method is only for reference purposes. It should not be used
in the actual program.

Jeremy Juckett, 
'''
def simple_line_follow():
    loop = True
    while loop:
        left_magnitude = magnitude(left_color_sensor.get_rgb_intensity())
        right_magnitude = magnitude(right_color_sensor.get_rgb_intensity())

        # line on left
        if (
            in_interval(left_magnitude, black_interval) and
            not in_interval(right_magnitude, black_interval)
        ):
            left_motor.start(0)
            right_motor.start()

        # line on right
        elif (
            not in_interval(left_magnitude, black_interval) and
            in_interval(right_magnitude, black_interval)
        ):
            left_motor.start()
            right_motor.start(0)

        # line on both sides
        elif (
            in_interval(left_magnitude, black_interval) and
            in_interval(right_magnitude, black_interval)
        ):
            left_motor.start()
            right_motor.start()

        # no lines
        else:
            loop = False


'''
complex_line_follow()

Jeremy Juckett, 
'''
def line_follow():
    loop = True
    while loop:
        left_magnitude = magnitude(left_color_sensor.get_rgb_intensity())
        right_magnitude = magnitude(right_color_sensor.get_rgb_intensity())

        # slow line on left
        if (
            in_interval(left_magnitude, purple_interval) and
            in_interval(right_magnitude, white_interval)
        ):
            left_motor.start(0)
            right_motor.start(SLOW_SPEED)

        # fast line on left
        elif (
            in_interval(left_magnitude, green_interval) and
            in_interval(right_magnitude, white_interval)
        ):
            left_motor.start(0)
            right_motor.start(FAST_SPEED)
        
        # slow line on right
        elif (
            in_interval(left_magnitude, white_interval) and 
            in_interval(right_magnitude, purple_interval)
        ):
            # check line speed color on right sensor
            left_motor.start(SLOW_SPEED)
            right_motor.start(0)

        # fast line on right
        elif (
            in_interval(left_magnitude, white_interval) and 
            in_interval(right_magnitude, green_interval)
        ):
            # check line speed color on right sensor
            left_motor.start(FAST_SPEED)
            right_motor.start(0)

        # slow line on both sides
        elif (
            in_interval(left_magnitude, purple_interval) and 
            in_interval(right_magnitude, purple_interval)
        ):
            left_motor.start(SLOW_SPEED)
            right_motor.start(SLOW_SPEED)

        # fast line on both sides
        elif (
            in_interval(left_magnitude, green_interval) and 
            in_interval(right_magnitude, green_interval)
        ):
            left_motor.start(FAST_SPEED)
            right_motor.start(FAST_SPEED)

        # no lines
        else:
            loop = False


'''
in_interval(value, interval)

Determine whether the given value is within the given intervale.
The interval should be a list containing exactly two value: the second
value should be greater than the first.

Returns True if the value does exist in the interval; Otherwise, returns False.

Jeremy Juckett, 
'''
def in_interval(value, interval):
    return value >= interval[0] and value <= interval[1]


'''
test_rgbi_reading()

The rgbi magnitudes for the color sensors are computed with each press of the
left button on the PrimeHub. This will loop until the right button on the
PrimeHub is pressed.

In order for the results to print to the console, the robot must be connected
via USB.

Jeremy Juckett,
'''
def test_rgbi_reading():
    while not hub.right_button.is_pressed():
        if hub.left_button.is_pressed():
            hub.speaker.beep(60, 0.5)
            left_magnitude = magnitude(left_color_sensor.get_rgb_intensity())
            right_magnitude = magnitude(right_color_sensor.get_rgb_intensity())
            print("L: " + str(left_magnitude))
            print("R: " + str(right_magnitude))
            print()
    
    hub.speaker.beep(60, 0.5)

'''
exists_right_corner()

Jeremy Juckett,
'''
def exists_right_corner():
    right_distance = right_distance_sensor.get_distance_cm()

    # if there is a wall to the immediate right, then there is no corner
    if not right_distance is None and right_distance <= WALL_DISTANCE:
        return False
    
    # move ahead a bit to avoid rotating into a wall
    left_motor.start(-50)
    right_motor.start(50)
    wait_for_seconds(0.5)
    left_motor.stop()
    right_motor.stop()

    # rotate -90 degrees
    mp.move_tank(amount=(pi * WHEEL_RADIUS), unit='cm', left_speed=50, right_speed=-50)
    wait_for_seconds(0.5)

    # move a head a bit
    left_motor.start(-50)
    right_motor.start(50)
    wait_for_seconds(0.5)
    left_motor.stop()
    right_motor.stop()
    wait_for_seconds(0.5)

    # scan for a wall on the right, returning True if a wall exists
    right_distance = right_distance_sensor.get_distance_cm()
    if not right_distance is None and right_distance <= WALL_DISTANCE:
        return True
    
    # undo the previous motions if there is no wall, return False
    left_motor.start(50)
    right_motor.start(-50)
    wait_for_seconds(0.5)
    left_motor.stop()
    right_motor.stop()

    mp.move_tank(amount=(pi * WHEEL_RADIUS), unit='cm', left_speed=-50, right_speed=50)

    left_motor.start(50)
    right_motor.start(-50)
    wait_for_seconds(0.5)
    left_motor.stop()
    right_motor.stop()

    return False

'''
wall_follow()

Jeremy Juckett,
'''
def wall_follow():
    heading = None
    loop = True
    while loop:
        left_color_magnitude = magnitude(left_color_sensor.get_rgb_intensity())
        right_color_magnitude = magnitude(right_color_sensor.get_rgb_intensity())
        right_distance = right_distance_sensor.get_distance_cm()
        forward_distance = forward_distance_sensor.get_distance_cm()

        # handle goal detected
        if (
            in_interval(left_color_magnitude, red_interval) or
            in_interval(right_color_magnitude, red_interval)
        ):
            left_motor.stop()
            right_motor.stop()
            loop = False

        # handle wall ahead ****SETH******
        elif forward_distance_sensor <= WALL_DISTANCE: #may have to increase wall distance
            # turn left
            # heading += 90
            
            #right_motor.set_default_speed(-10)
            #left_motor.move(-5, 'cm', 0, -5)

            #move to the left
            left_motor.start()
            right_motor.start()
            mp.move_tank(amount=(pi * WHEEL_RADIUS), unit='cm', left_speed=-50, right_speed=50)

            #heading is in the positive 90 direction
            heading += 90
            wait_for_seconds(1)

            #makes sure that heading is not 360 and if so sets it to 0 again
            if( heading == 360):
               wait_for_seconds(.5)
               heading == 0
                    
            
            pass

        # handle right corner ***SETH*****
        elif exists_right_corner():
            # if heading is 0, move foraward
            # else, turn right and heading -= 90

            if (heading == 0):
                left_motor.start()
                right_motor.start()

            elif (heading != 0):
                mp.move_tank(amount=(pi * WHEEL_RADIUS), unit='cm', left_speed=50, right_speed=-50)
                heading -= 90
                left_motor.start()
                right_motor.start()
            pass

        # handle wall on right ***SETH***
        elif right_distance <= WALL_DISTANCE:
            # continue forward
            #should have an indication if its getting to close to the wall next to it...adjust very slightly to the left
            #something like left_speed = for .1 seconds is less than right
            #added a beep to tell the range when to close to wall
            hub.speaker.beep()
            right_motor.start()
            left_motor.start()
            pass
        
        else:
            # continue forward
            right_motor.start()
            left_motor.start()
            pass


def test_exists_right_corner():
    while not hub.right_button.is_pressed():
        if hub.left_button.is_pressed():
            hub.speaker.beep(60, 0.5)
            result = exists_right_corner()
            lm.write(str(result))
    
    hub.speaker.beep(60, 0.5)

'''
main()

The robot will drive in the known direction of the goal.

Iteratively, the bot will run the line_follow() method. If there are no lines
to follow, control is simply returned back to main().

...

If no lines or walls are detected, the robot will drive in the known direction
of the end goal.

Jeremy Juckett, 
'''
def main():
    goal = False
    while not goal:
        # drive in direction of goal
        left_motor.start()
        right_motor.start()

        # check for wall

        #wall_follow()

        # line follow
        line_follow()
        

#main()

#wall_follow()
test_exists_right_corner()
#test_rgbi_reading()