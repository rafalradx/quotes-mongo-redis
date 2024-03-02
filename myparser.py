import argparse

myparser = argparse.ArgumentParser(
    prog="mongoDB quote retriever",
    description="CLI for loading quotes and author data from json file into mongo DB and retrieving quotes",
)
myparser.add_argument(
    "-f",
    "--file",
    type=str,
    help="upload data from json FILE to mongoDB",
)

myparser.add_argument(
    "-n", "--name", type=str, help="return all quotes of a given author NAME"
)


myparser.add_argument(
    "-t", "--tags", nargs="+", type=str, help="return all quotes with given TAGS"
)
