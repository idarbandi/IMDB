from threading import Thread, Lock
from imdb import PureLink
from demo_pkg.db import create_table

if __name__ == "__main__":
    c = create_table()
    crawler = PureLink()
    p = Thread(target=crawler.get)
    p.start()

