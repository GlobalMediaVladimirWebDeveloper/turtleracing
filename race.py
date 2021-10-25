import os
from time import sleep
from random import randint
import uuid


import turtle
from webcolors import rgb_to_name, css3_hex_to_names, hex_to_rgb

WIDTH, HEIGHT = 700, 600

MIN_RACERS = 2
MAX_RACERS = 10


RACERS_SHAPE = ["Square", "Arrow", "Circle", "Turtle", "Triangle", "Classic",]
RACERS_SHAPE_LENGTH = len(RACERS_SHAPE) - 1
RACERS_COLORS = []
_RACERS = {}
"""
	# RACERS 
	{
		UUID('8b92310e-5417-46a7-8412-ac36adc32d4f'): 
		{
			'racer': <turtle.Turtle object at 0x0000022770E44C70>, 
			'color': ((214.0, 54.0, 191.0), (132.0, 22.0, 188.0))
		}
	}
"""


_MIN_RACE_DISTANCE = 1
_MAX_RACE_DISTANCE = 20


_START_BOTTOM_LINE = 60

MAX_RANDOM_COLOR_TRY = MAX_RACERS
_RACER_X_SPACING = 30







def init_turtle_window() -> turtle.Screen:
	screen = turtle.Screen()
	screen.setup(WIDTH, HEIGHT)
	screen.title('Turtle Racing!')
	screen.colormode(255)
	return screen

def clear_terminal():
	return os.system('cls' if os.name == 'nt' else 'clear')

def wait_and_repeat(msg: str, sleep_time:int = 5) -> bool:
	if not isinstance(sleep_time, int) and not isinstance(msg, str):
		msg = 'An error has occurred, please re-enter in 5 seconds.'
		sleep_time = 5
	clear_terminal()
	print(msg)
	sleep(sleep_time)
	return True


def get_number_of_racers():
	racers = 0
	while True:
		clear_terminal()
		racers = input(f"Enter the number of racers ({MIN_RACERS} - {MAX_RACERS}): ")
		if racers.isdigit():
			racers = int(racers)
		else:
			wait_and_repeat('Input is not numeric... Try again in 4 seccond after.',4)
			continue
		if racers in range(MIN_RACERS, MAX_RACERS + 1):
			return racers
		else:
			wait_and_repeat(f"Number of racers is not in range ({MIN_RACERS} - {MAX_RACERS}).",4)

def get_random_rgb_color() -> tuple:
	return ((randint(0,255),randint(0,255),randint(0,255)))

def closest_colour(requested_colour):
	min_colours = {}
	for key, name in css3_hex_to_names.items():
		r_c, g_c, b_c = hex_to_rgb(key)
		rd = (r_c - requested_colour[0]) ** 2
		gd = (g_c - requested_colour[1]) ** 2
		bd = (b_c - requested_colour[2]) ** 2
		min_colours[(rd + gd + bd)] = name
	return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour: tuple) -> str:

	requested_colour = tuple([int(color) for color in requested_colour])
	color = ''

	try:
		color = rgb_to_name(requested_colour)
	except ValueError:
		color = closest_colour(requested_colour)
	return color



def is_unique_color(color: [str, tuple]) -> bool:
	if color in RACERS_COLORS: 
		return False
	else:
		return True

def make_turtle_color(color_mode: tuple = 'random'):
	color = ''


	if isinstance(color_mode, str) and color_mode == 'random':
		for i in range(MAX_RANDOM_COLOR_TRY):
			get_random_color = get_random_rgb_color()

			if i == MAX_RANDOM_COLOR_TRY - 1:
				color = get_random_color

			if is_unique_color(get_random_color):
				color = get_random_color
			else:
				continue

	elif isinstance(color_mode, tuple):
		color = color_mode if is_unique_color(get_random_color) else get_random_rgb_color()
	else:
		color = color_mode if is_unique_color(get_random_color) else get_random_rgb_color()

	return color


def create_racer(shape: str = 'random', shape_color: tuple = 'random', pen_color: tuple = 'random', fill_color: tuple = 'random', shape_speed: int = 2, position: int = 1, racer_x_spacing: int = 80) -> turtle.Turtle:
	new_racer = turtle.Turtle()

	if shape == 'random':
		new_racer.shape(RACERS_SHAPE[randint(0,RACERS_SHAPE_LENGTH)].lower())
	else:
		new_racer.shape(RACERS_SHAPE[randint(0,RACERS_SHAPE_LENGTH)].lower())

	new_racer.color(make_turtle_color(shape_color))

	new_racer.pencolor(make_turtle_color(pen_color))

	new_racer.fillcolor(make_turtle_color(fill_color))

	new_racer.speed(shape_speed)

	new_racer.left(90)

	new_racer.penup()

	new_racer.setpos(-WIDTH // 2 + (position + 1) * racer_x_spacing, -HEIGHT // 2 + _START_BOTTOM_LINE)

	new_racer.pendown()


	return new_racer


def create_racers(racer_x_spacing, racers: int = 2) -> dict:
	for racer_idx in range(racers):
		next_racer = create_racer(position=racer_idx, racer_x_spacing=racer_x_spacing)
		_RACERS[uuid.uuid4()] = {
			'racer': next_racer,
			'color': next_racer.color()
		}
	return _RACERS

def race(racers):
	while True:
		for racer_idx, racer in racers.items():
			current_racer = racer['racer']
			distance = randint(_MIN_RACE_DISTANCE,_MAX_RACE_DISTANCE)
			current_racer.forward(distance)

			racer_x, racer_y = current_racer.pos()

			if racer_y >= HEIGHT // 2 - 10:
				return [racer_idx, current_racer.color()]


def main():
	max_number_of_racers = get_number_of_racers()
	_RACER_X_SPACING = WIDTH // (max_number_of_racers + 1)
	screen = init_turtle_window()
	racers = create_racers(_RACER_X_SPACING, max_number_of_racers)
	new_race = race(racers)
	print(f"The winner is '{new_race[0]}', with color '{get_colour_name(new_race[1][1])}'.")
	sleep(5)

if __name__ == '__main__':
	main()