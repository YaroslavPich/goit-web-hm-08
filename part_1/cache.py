import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379)
cache = RedisLRU(client)


@cache
def find_by_author(author: str):
	author = Author.objects(fullname__iregex=author)
	result = []
	for a in author:
		quotes = Quote.objects(author=a)
		result.extend([q.quote for q in quotes])
	return result


@cache
def find_by_tag(tag_: str):
	quotes = Quote.objects(tags__iregex=tag_)
	result = [q.quote for q in quotes]
	return result


if __name__ == '__main__':
	while True:
		while True:
			user_input = input("Enter command: ")
			if user_input:
				break
			else:
				print("You don't enter command!")
		command = user_input

		try:
			find_param, command_param = command.split(':', 1)
		except ValueError:
			print("Invalid command.")
			continue

		if find_param in "exit":
			print("Goodbye!")
			break
		elif find_param == 'name':
			quotes_find = find_by_author(command_param.strip())
			for quote in quotes_find:
				print(quote)
		elif find_param == 'tag':
			quotes_find = find_by_tag(command_param.strip())
			for quote in quotes_find:
				print(quote)
		elif find_param == 'tags':
			tags = command_param.split(',')
			all_quotes = []
			for tag in tags:
				quotes_find = find_by_tag(tag.strip())
				all_quotes.extend(quotes_find)
			all_quotes = set(all_quotes)
			for quote in all_quotes:
				print(quote)
		else:
			print("Invalid command.")
