import argparse
import secrets

ascii_chars: str = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
odl_chars: str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

parser = argparse.ArgumentParser()
parser.add_argument("-l", type=int, required=False, default=13,
			help='length')
parser.add_argument("-o", action='store_true', required=False, default=False,
			help='only digits and letters (default is ascii 33-126)')
parser.add_argument("-chars", type=str, required=False, default=ascii_chars,
			help='characters')
args = parser.parse_args()
#print(args)
characters: str = odl_chars if args.o else ascii_chars
#print(characters)


if __name__ == '__main__':
	for idx in range(args.l):
		print(secrets.choice(characters), end='')
	print()
