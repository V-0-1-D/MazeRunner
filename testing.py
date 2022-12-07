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


# [low, high]
black_interval = [0, 200] # used for detecting walls
yellow_interval = [] # used for slow line-following
green_interval = [] # used for fast line-following
white_interval = [1300, 1500] # used for default driving surface


