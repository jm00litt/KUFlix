import os

class DirectorData:
    directors = {}

    @classmethod
    def check_file(cls):
        file_path = os.path.join(os.path.dirname(__file__), "data/director.txt")