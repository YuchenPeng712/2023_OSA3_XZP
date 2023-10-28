#arg
PORT = 12345
PATTERN = "happy"

start:
	@python3 assignment3.py -l $(PORT) -p $(PATTERN)