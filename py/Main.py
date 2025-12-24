import core
import core.my_logging as lg


if __name__ == '__main__':
	x: int = 1
	print(x)
	with lg.AutoLog(lg.ERROR, "work", lambda: f'start {x} ...', lambda: f'done; {x}.'):
		x = 3
		print(x)
