from myparser import myparser
from argparse import Namespace
import actions


def handler(args: Namespace) -> None:
    if args.name:
        result = actions.get_quotes_by_author(args.name)
        print(result)
    if args.tags:
        result = actions.get_quotes_by_tags(args.tags)
        print(result)
    if args.file:
        actions.json_to_mongo(args.file)


if __name__ == "__main__":
    handler(myparser.parse_args())
