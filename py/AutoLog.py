import datetime
import logging
import time


class AutoLog:
	def __init__(self, log_level, enter_msg_lambda, exit_msg_lambda):
		print('init')
		self.log_level = log_level
		self.enter_msg = enter_msg_lambda
		self.exit_msg = exit_msg_lambda

	def __del__(self):
		print('del')

	def __enter__(self) -> 'AutoLog':
		# determine if should log and skip if not
		self.ts = datetime.datetime.now()
		print(f'about to log at {self.ts.strftime("%Y-%m-%d %H:%M:%S")}: ', self.enter_msg())
		logging.log(self.log_level, self.enter_msg())
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		# only if enter determined that it should log; else skip
		print(f'about to log elapsed {datetime.datetime.now() - self.ts}: ', self.exit_msg())
		logging.log(self.log_level, self.exit_msg())


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

x = 1
print('before compute x', x)


def enter_func():
	print('enter func')
	return f'starting work with {x} ...'


def exit_func():
	print('exit func')
	return f'work is done; result {x} ...'


with AutoLog(logging.INFO, lambda: f'starting work with {x} ...', lambda: f'work is done; result {x}.'):
#with AutoLog(logging.INFO, enter_func, exit_func):
	print('computing ...')
	time.sleep(1)
	x = 2

with AutoLog(logging.INFO, lambda: f'starting work with {x} ...', lambda: f'work is done; result {x}.'):
	x = 3

print('after compute x', x)

print('before sleep')
time.sleep(3)
print('after sleep')
