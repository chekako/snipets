import core
import core.my_logging as lg
import core.config_reader as cr
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i", type=int, required=False, default=0,
			help='int')
parser.add_argument("-s", type=str, required=False, default="",
			help='str')
parser.add_argument("-log-level", type=str, required=False, default="DEBUG",
			help='str')
parser.add_argument("-config-ini", type=str, required=False, default="config.ini",
			help='str')
args = parser.parse_args()


if __name__ == '__main__':
	conf = cr.ConfigReader()
	ml = lg.MainLogger(True)
	ml.initialize()
	ml.log(core.L.INFO, lambda: f"{"howdy\n"}")
	s = conf.get_string("main", "k", "fall")
	print("k =", s)
	with lg.AutoLog(lg.INFO, "work", lambda: f'start {s} ...', lambda: f'done; {s}.'):
		s = "all done."
	print(s)
