from models import Author, Quote, Tag
import json
import connect_mongo
import redis
from redis_lru import RedisLRU
from thefuzz import fuzz

redis_client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(redis_client)


@cache
def get_quotes_by_author(name_string: str) -> str:
    result = "-------------------\n"
    authors = Author.objects(fullname__istartswith=name_string)
    for author in authors:
        # print(authors[0].to_mongo().to_dict())
        quotes = Quote.objects(author=author)
        result += f"{author.fullname}'s quotes:\n"
        for quote in quotes:
            result += f"{quote.quote}\n"
    return result.removesuffix("\n")


@cache
def get_quotes_by_tags(tags: list[str]) -> str:
    if len(tags) > 1:
        quotes = Quote.objects(tags__name__in=tags)
    else:
        quotes = Quote.objects(tags__name__istartswith=tags[0])
    result = f"Quotes with '{', '.join(tags)}' tags:\n"
    for quote in quotes:
        result += f"{quote.quote}\n"
    return result.removesuffix("\n")


@cache
def author_from_mongo(name: str) -> Author:
    author = Author.objects(fullname__iexact=name)
    return author[0]


@cache
def author_closest_match(name_query: str) -> Author:
    authors = Author.objects()
    names = [author.fullname for author in authors]
    scores = [fuzz.partial_ratio(name_query, name) for name in names]
    scores_sorted = sorted(zip(scores, names), key=lambda x: x[0], reverse=True)
    best_match = scores_sorted[0][1]
    return Author.objects(fullname__iexact=best_match)[0]


def json_to_mongo(filename: str) -> None:
    data = None
    try:
        with open(filename, "r") as fn:
            data = json.load(fn)
    except FileNotFoundError as err:
        print(str(err))
    if data:
        if "fullname" in data[0]:
            print("JSON file with authors data")
            for author in data:
                author_mod = Author(
                    fullname=author["fullname"],
                    born_date=author["born_date"],
                    born_location=author["born_location"],
                    description=author["description"],
                ).save()
            print(f"{len(data)} authors added to mongo DB")

        elif "quote" in data[0]:
            print("JSON file with quotes data")
            for quote in data:
                # author must be present in DB before his quote can be added
                try:
                    author = author_from_mongo(quote["author"])
                    quote_mod = Quote(
                        quote=quote["quote"],
                        author=author,
                        tags=[Tag(name=tagname) for tagname in quote["tags"]],
                    ).save()
                except IndexError:
                    quote_s = quote["quote"][:20]
                    print(
                        f"[!] The author: '{quote['author']}' of a quote: {quote_s}...\" not found in DB\n[!] Looking for a closest match"
                    )
                    author = author_closest_match(quote["author"])
                    print(f"[!] Best match for '{quote['author']}' found")
                    print(
                        f"[!] Assigning quote to '{author.fullname}' -- please verify"
                    )
                    quote_mod = Quote(
                        quote=quote["quote"],
                        author=author,
                        tags=[Tag(name=tagname) for tagname in quote["tags"]],
                    ).save()

            print(f"{len(data)} quotes added to mongo DB")
        else:
            print("Wrong JSON file structure")
