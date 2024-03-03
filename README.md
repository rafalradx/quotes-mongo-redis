**Usage**

- Clone this repository into a folder of choice on your local machine using the following command:
    ```
    git clone https://github.com/rafalradx/quotes-mongo-redis
    ```
- Navigate into the repo folder and create `config.ini` file with your login info to mongoDB. See connection string of your provider:
    ```
    [DB]
    USER=somebody
    PASS=somepassword
    APP_NAME=someapp
    DOMAIN=give.me.mongodb.please.net

    ```
- For caching DB queries start redis in docker on 6379 port:
     ```
     docker run --name redis-cache -p 6379:6379 redis
     ```
- To add quotes or authors data from json file use `-f/--file` parameter. See `authors.json` and `quotes.json` for reference:
     ```
     python3 main.py -f somefile.json
     ```
- To get all quotes of Albert Einstein use `-n/--name` (case-insensitive, two words = use quotes):
     ```
     python3 main.py -n "albert Einstein" 
     ```
     or you can specify just a few first letter of a name:
     ```
     python3 main.py -n albe
- To get all quotes with given tags use `-t/--tags` parameter (case-insensitive):
     ```
     python3 main.py -t life death world
     ```
     scirpt will return all quotes with at least one o the provided tags (or)
- You can combine `-n` and `-t` in one command:
     ```
     python3 main.py -t life death world -n albert
     ```