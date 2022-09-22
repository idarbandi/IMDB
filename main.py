from multiprocessing import Process
from imdb import PureLink

if __name__ == "__main__":

    """ defined a Multi_Processing function to Perform The task"""

    p = Process(target=PureLink)
    p.start()
