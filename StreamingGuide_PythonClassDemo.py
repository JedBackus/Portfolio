# Author: Jedidiah Backus
# Description: Three classes. One for storing movies, one for storing streaming services, and one to act as a streaming guide.


class Movie:
    """class for storing movie objects"""
    _allmovies = []

    def __init__(self, title, genre, director, year):
        """method for creating new objects in the Movie class"""
        self._title = title
        self._genre = genre
        self._director = director
        self._year = year
        self._allmovies.append(self)

    def get_title(self):
        """method for retrieving title of a movie object"""
        return self._title

    def get_genre(self):
        """method for retrieving genre of a movie object"""
        return self._genre

    def get_director(self):
        """method for retrieving director of a movie object"""
        return self._director

    def get_year(self):
        """method for retrieving year of a movie object"""
        return self._year

class StreamingService:
    """class for storing streaming service objects"""

    def __init__(self, name):
        """method for creating new objects in the Streaming service class"""
        self._name = name
        self._catalog = {}

    def get_name(self):
        """method for retrieving name of a streaming service object"""
        return self._name

    def get_catalog(self):
        """method for retrieving catalog of a streaming service object"""
        return self._catalog

    def add_movie(self, movie):
        """method for adding Movie objects to a Streaming service object"""
        self._catalog[movie.get_title()] = movie

    def delete_movie(self, movie):
        """method for deleting Movie objects from a Streaming service object"""
        self._catalog.pop(movie)

class StreamingGuide:
    """class for storing a list of steaming services"""

    def __init__(self):
        """method for creating a streaming guide"""
        self._guide = []

    def add_streaming_service(self, option):
        """method for adding streaming service objects to a streaming guide"""
        self._guide.append(option)

    def delete_streaming_service(self, option):
        """method for removing streaming service objects from a streaming guide"""
        for each in self._guide:
            if option in each.get_name():
                self._guide.remove(each)

    def who_streams_this_movie(self, film):
        """method for determining which streaming service contains a particular movie"""
        result = {"Title": "Not Found", "Year": "Not Found", "Services": []}
        available = []
        for each in Movie._allmovies:
            if film == each.get_title():
                result["Title"] = each.get_title()
                result["Year"] = each.get_year()
        for each in self._guide:
            for every in each.get_catalog():
                if film == each.get_catalog()[every].get_title():
                    result["Services"] += [each.get_name()]
                    available += [each.get_name()]
        if available == []:
            result["Services"] = "None"
        return result



