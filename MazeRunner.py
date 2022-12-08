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

Returns True if a right corner is detected, and False if there is no corner.
Additionally, False is returned if a wall is detected to the immediate right of
the robot's initial position.

--- Procedure ---
Check if there is a wall to the right of the robot's initial position. If so,
return False; otherwise, continue to the next step.

Move forward enough distance so the bot does not hit the wall when it rotates.

Rotate 90 degrees to the right.

Move forward enough distance so that it, if another wall exists,
it can be detected.

Check for a wall on the right. If a wall exists return True. If a wall doesn't
exists, return the robot to its initial position and return False.

Jeremy Juckett,
'''
def exists_right_corner():
    right_distance = right_distance_sensor.get_distance_cm()

    # if there is a wall to the immediate right, then there is no corner
    if right_distance and right_distance <= WALL_DISTANCE:
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
    if right_distance and right_distance <= WALL_DISTANCE:
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

This method performs wall following by implementing the Pledge algorithm.
While following a wall, the bot should maintain a distance of 8 cm from the
wall to ensure that it does not deviate.

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

        # handle wall ahead
        elif forward_distance and forward_distance <= WALL_DISTANCE:
            # turn left
            # heading += 90
            pass

        # handle right corner
        elif exists_right_corner():
            # if heading is 0, move foraward
            # else, turn right and heading -= 90
            pass

        # handle wall on right
        elif right_distance and right_distance <= WALL_DISTANCE:
            # continue forward, maintaining a distance of 8 cm from wall
            pass
        
        else:
            # continue forward
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

        # line follow
        line_follow()
        

#main()

#wall_follow()
test_exists_right_corner()
#test_rgbi_reading()