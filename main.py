from threading import Thread
from imdb import PureLink
from demo_pkg.db import create_table

if __name__ == "__main__":
    c = create_table()
    p = Thread(target=PureLink)
    p.start()
