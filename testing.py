'''
MazeRunner.py

Programmers: Jeremy Juckett, 

Modified:
    Jeremy Juckett (11-25-2022), started main(), started line_follow();

    Jeremy Juckett (11-28-2022), started test_rgbi_reading();

    Jeremy Juckett (11-29-2022), finished test_rgbi_reading(),
    defined color-interval lists, in_interval(), add simple_line_follow();

'''

from spike import ColorSensor, PrimeHub, LightMatrix, Motor

'''
Initialize module-level variable.
Pins are subject to change.
'''
hub = PrimeHub()
lm = LightMatrix()
left_color_sensor = ColorSensor('F')
right_color_sensor = ColorSensor('E')

left_motor = Motor('C')
left_motor.set_default_speed(-50)
right_motor = Motor('D')
right_motor.set_default_speed(50)

slow_speed = 25
fast_speed = 75

# [low, high]
black_interval = [0, 200] # used for detecting walls
red_interval = [] # used for slow line-following
yellow_interval = []
green_interval = [] # used for fast line-following
white_interval = [1300, 1500] # used for default driving surface


'''
magnitude(vector)

Computes and returns the magnitude of the given collection of values.

Jeremy Juckett, 
'''
# def magnitude(vector):
#     sum = 0
#     for v in vector:
#         sum = sum + v ** 2
#     return sum ** (1/2)


# '''
# simple_line_follow()

# Jeremy Juckett, 
# '''
# def simple_line_follow():
#     loop = True
#     while loop:
#         left_magnitude = magnitude(left_color_sensor.get_rgb_intensity())
#         right_magnitude = magnitude(right_color_sensor.get_rgb_intensity())

#         # line on left
#         if (
#             in_interval(left_magnitude, black_interval) and
#             not in_interval(right_magnitude, black_interval)
#         ):
#             left_motor.start(0)
#             right_motor.start()

#         # line on right
#         elif (
#             not in_interval(left_magnitude, black_interval) and
#             in_interval(right_magnitude, black_interval)
#         ):
#             left_motor.start()
#             right_motor.start(0)

#         # line on both sides
#         elif (
#             in_interval(left_magnitude, black_interval) and
#             in_interval(right_magnitude, black_interval)
#         ):
#             left_motor.start()
#             right_motor.start()

#         # no lines
#         else:
#             loop = False


'''
complex_line_follow()

Jeremy Juckett, 
'''
def complex_line_follow():
    loop = True
    while loop:
        left_magnitude = magnitude(left_color_sensor.get_rgb_intensity())
        right_magnitude = magnitude(right_color_sensor.get_rgb_intensity())

        # slow line on left
        if (
            in_interval(left_magnitude, yellow_interval) and
            in_interval(right_magnitude, white_interval)
        ):
            left_motor.start(0)
            right_motor.start(slow_speed)

        # fast line on left
        elif (
            in_interval(left_magnitude, green_interval) and
            in_interval(right_magnitude, white_interval)
        ):
            left_motor.start(0)
            right_motor.start(fast_speed)
        
        # slow line on right
        elif (
            in_interval(left_magnitude, white_interval) and 
            in_interval(right_magnitude, yellow_interval)
        ):
            # check line speed color on right sensor
            left_motor.start(slow_speed)
            right_motor.start(0)

        # fast line on right
        elif (
            in_interval(left_magnitude, white_interval) and 
            in_interval(right_magnitude, green_interval)
        ):
            # check line speed color on right sensor
            left_motor.start(fast_speed)
            right_motor.start(0)

        # slow line on both sides
        elif (
            in_interval(left_magnitude, purple_interval) and 
            in_interval(right_magnitude, purple_interval)
        ):
            left_motor.start(slow_speed)
            right_motor.start(slow_speed)

        # fast line on both sides
        elif (
            in_interval(left_magnitude, green_interval) and 
            in_interval(right_magnitude, green_interval)
        ):
            left_motor.start(fast_speed)
            right_motor.start(fast_speed)

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
        simple_line_follow()
        

main()
#test_rgbi_reading()