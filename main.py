from flask import Flask, render_template, request, redirect, url_for, session
import re
import time
import base64
import os
import random
import requests
import json
import pytz
import urllib.request
from collection import col_list
from werkzeug.exceptions import HTTPException
import threading
import datetime

app = Flask(__name__, template_folder='site', static_folder='assets')

#TMDB DATABASE SETUP
from tmdbv3api import TMDb, Movie, Person, Discover, TV, Season

tmdb = TMDb()
tmdb.api_key = os.environ['apikey']
genres = [{
    "id":
    '28',
    "name":
    "Action",
    "url":
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9dmastuNWJRCmSYhsFuWUey8S-Yx0ZnyzuZbFJnEMih_Uqle9dhB8z9fei0PciMrafUI&usqp=CAU"
}, {
    "id":
    '12',
    "name":
    "Adventure",
    "url":
    "https://unitingartists.org/wp-content/uploads/2020/06/Adventure-Genre-800x445.jpg"
}, {
    "id":
    '16',
    "name":
    "Animation",
    "url":
    "https://4.bp.blogspot.com/-7f0Ull4tk2U/WxrZhyHjI5I/AAAAAAABN4U/h6z6iuVV_ssZHt_iDoJ8DLldjS01QReQwCLcBGAs/s1600/Spider-Man-Into-the-Spiderverse-2018-trailer-10-1280x546.jpg"
}, {
    "id":
    '35',
    "name":
    "Comedy",
    "url":
    "https://static0.srcdn.com/wordpress/wp-content/uploads/2018/08/Ryan-Reynolds-in-Deadpool.jpg"
}, {
    "id":
    '80',
    "name":
    "Crime",
    "url":
    "https://img.mensxp.com/media/content/2017/Dec/the-top-10-crime-thriller-movies-of-20171400-1513772701.jpg"
}, {
    "id":
    '878',
    "name":
    "Science-Fiction",
    "url":
    "https://s.yimg.com/ny/api/res/1.2/iV700HRBI6XCFXvGUT_5TA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTM2MA--/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2020-02/564efb10-53c9-11ea-86fb-f4072beb20b2"
}, {
    "id":
    '14',
    "name":
    "Fantasy",
    "url":
    "https://bookstr.com/wp-content/uploads/2020/06/harry-potter-movies-on-netflix.jpg"
}, {
    "id":
    '27',
    "name":
    "Horror",
    "url":
    "https://www.commonsensemedia.org/sites/default/files/styles/ratio_16_9_small/public/video-thumbnails/it-thumb.jpg"
}, {
    "id":
    '9648',
    "name":
    "Mystery",
    "url":
    "https://thecinemaholic.com/wp-content/uploads/2021/01/ezgif.com-gif-maker-5.jpg"
}, {
    "id":
    '10749',
    "name":
    "Romance",
    "url":
    "https://cdn.onebauer.media/one/empire-images/features/5a84102108d1e196265a9d4f/38-titanic.jpg?format=jpg&quality=80&width=440&ratio=1-1&resize=aspectfit"
}, {
    "id":
    '10770',
    "name":
    "TV-Movie",
    "url":
    "https://c.files.bbci.co.uk/22AC/production/_118667880_ka_05_friendsreunion.jpg"
}, {
    "id":
    '53',
    "name":
    "Thriller",
    "url":
    "https://www.billboard.com/wp-content/uploads/stylus/109300-inception_617_409.jpg?w=617"
}]


def get_keep_watch(keep_watch_id):
    url = f"https://api.themoviedb.org/3/movie/{keep_watch_id}?api_key={os.environ['apikey']}"
    movie = requests.get(url).json()
    keep_watch = ({
        "id":
        str(movie['id']),
        'type':
        'movie',
        'title':
        movie['title'],
        'year':
        movie['release_date'][:4],
        'bio':
        movie['overview'],
        'adult':
        movie['adult'],
        'type':
        "Movie",
        'rating':
        str(movie['vote_average']),
        'img':
        "https://image.tmdb.org/t/p/w200" + movie['poster_path'],
        'img_hd':
        "https://image.tmdb.org/t/p/w1280/" + movie['backdrop_path']
    })
    return (keep_watch)


def get_keep_watch_tv(keep_watch_id):
    url = f"https://api.themoviedb.org/3/tv/{keep_watch_id}?api_key={os.environ['apikey']}"
    movie = requests.get(url).json()
    keep_watch = ({
        "id":
        str(movie['id']),
        'type':
        'tvshow',
        'title':
        movie['name'],
        'img':
        "https://image.tmdb.org/t/p/w200" + movie['poster_path'],
        'img_hd':
        "https://image.tmdb.org/t/p/w1280/" + movie['backdrop_path']
    })
    return (keep_watch)


def collection_maker():
    collection_id = [
        1241, 10, 556, 131292, 131296, 131295, 264, 435259, 645, 748, 151,
        87359, 9485, 295, 328
    ]
    collection = []
    for item in collection_id:
        url = f"https://api.themoviedb.org/3/collection/{item}?api_key={os.environ['apikey']}"
        b = (requests.get(url)).json()
        collection.append({
            'id':
            str(b['id']),
            'title': (b['name']),
            'movie_count':
            str(len(b['parts'])),
            'bio':
            b['overview'],
            'img':
            "https://image.tmdb.org/t/p/w300/" + b['poster_path']
        })
    return (collection)

def get_watch_src(type1, id):
	try:
		url = f"https://api.themoviedb.org/3/{type1}/{id}/watch/providers?api_key={os.environ['apikey']}"
		data = (requests.get(url)).json()
		if type1 =="tv":
			for item in ((data['results']['US']['flatrate'])):
				item['logo_path'] = "https://image.tmdb.org/t/p/w200" +item['logo_path']		 
			return ((data['results']['US']['flatrate']))
		if type1 =="movie":
			for item in ((data['results']['US']['buy'])):
				item['logo_path'] = "https://image.tmdb.org/t/p/w200" +item['logo_path']		 
			return ((data['results']['US']['buy']))
	except Exception:
		return []
	
def get_people_external(id):
    url = f"https://api.themoviedb.org/3/person/{id}/external_ids?api_key={os.environ['apikey']}"
    b = (requests.get(url)).json()
    external = {
        'insta': b['instagram_id'],
        'twitter': b['twitter_id'],
        'imdb': b["imdb_id"],
        "fb": b['facebook_id']
    }
    return external


def get_external(movie, id):
    if movie:
        a = f"https://api.themoviedb.org/3/movie/{id}/external_ids?api_key={os.environ['apikey']}"
    else:
        a = f"https://api.themoviedb.org/3/tv/{id}/external_ids?api_key={os.environ['apikey']}"
    b = (requests.get(a)).json()
    external = {
        'insta': b['instagram_id'],
        'twitter': b['twitter_id'],
        'imdb': b["imdb_id"],
        "fb": b['facebook_id']
    }
    return external


def get_movie_review(movie_id):
    movie_id = str(movie_id)
    b = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={os.environ['apikey']}&language=en-US&page=1"
    ).json()
    c = []
    for i in b['results']:
        try:
            if "http" not in i['author_details']['avatar_path']:
                c.append({
                    "updated_at": i['updated_at'],
                    "content": i['content'],
                    "author_details": {
                        "avatar_path":
                        "https://image.tmdb.org/t/p/w500/" +
                        i['author_details']['avatar_path'],
                        "username":
                        i['author_details']['username']
                    }
                })
            else:
                c.append({
                    "updated_at": i['updated_at'],
                    "content": i['content'],
                    "author_details": {
                        "avatar_path": i['author_details']['avatar_path'][1:],
                        "username": i['author_details']['username']
                    }
                })
        except Exception:
            pass
    return c


def get_tv_review(tv_id):
    tv_id = str(tv_id)
    b = requests.get(
        f"https://api.themoviedb.org/3/tv/{tv_id}/reviews?api_key={os.environ['apikey']}&language=en-US&page=1"
    ).json()
    c = []
    for i in b['results']:
        try:
            if "http" not in i['author_details']['avatar_path']:
                c.append({
                    "updated_at": i['updated_at'],
                    "content": i['content'],
                    "author_details": {
                        "avatar_path":
                        "https://image.tmdb.org/t/p/w500/" +
                        i['author_details']['avatar_path'],
                        "username":
                        i['author_details']['username']
                    }
                })
            else:
                c.append({
                    "updated_at": i['updated_at'],
                    "content": i['content'],
                    "author_details": {
                        "avatar_path": i['author_details']['avatar_path'][1:],
                        "username": i['author_details']['username']
                    }
                })
        except Exception:
            pass
    return c


def get_tv_clips(id):
    a = f"https://api.themoviedb.org/3/tv/{id}/videos?api_key={os.environ['apikey']}"
    b = (requests.get(a)).json()
    clip_data = []
    for item in b['results']:
        if item['type'] == "Trailer":
            clip_data.append({
                'title':
                item['name'],
                "id":
                str(item['key']),
                'link':
                "www.youtube.com/v/" + str(item['key']),
                'img':
                "https://img.youtube.com/vi/" + str(item['key']) +
                "/hqdefault.jpg",
                'icon':
                "film"
            })
        else:
            clip_data.append({
                'title':
                item['name'],
                "id":
                str(item['key']),
                'link':
                "www.youtube.com/v/" + str(item['key']),
                'img':
                "https://img.youtube.com/vi/" + str(item['key']) +
                "/hqdefault.jpg",
                'icon':
                "play"
            })
    return (clip_data)


def get_people_images(id):
    url = f"https://api.themoviedb.org/3/person/{id}/images?api_key={os.environ['apikey']}"
    movie = requests.get(url).json()
    images = []
    for item in movie['profiles']:
        images.append("https://image.tmdb.org/t/p/w500//" + item['file_path'])
    return (images)


def get_movie_clips(id):
    a = f"https://api.themoviedb.org/3/movie/{id}/videos?api_key={os.environ['apikey']}"
    b = (requests.get(a)).json()
    clip_data = []
    for item in b['results']:
        if item['type'] == "Trailer":
            clip_data.append({
                'title':
                item['name'],
                "id":
                str(item['key']),
                'link':
                "www.youtube.com/v/" + str(item['key']),
                'img':
                "https://img.youtube.com/vi/" + str(item['key']) +
                "/hqdefault.jpg",
                'icon':
                "film"
            })
        else:
            clip_data.append({
                'title':
                item['name'],
                "id":
                str(item['key']),
                'link':
                "www.youtube.com/v/" + str(item['key']),
                'img':
                "https://img.youtube.com/vi/" + str(item['key']) +
                "/hqdefault.jpg",
                'icon':
                "play"
            })
    return (clip_data)


def genre_movie(genre, type):
    movie = Discover()
    dico_movies = movie.discover_movies({
        'with_genres': str(genre),
        'sort_by': 'popularity.desc'
    })
    movies = []
    for movie in dico_movies:
        movies.append({
            "id":
            str(movie['id']),
            'title':
            movie['title'],
            'year':
            movie['release_date'][:4],
            'bio':
            movie['overview'],
            'adult':
            movie['adult'],
            'type':
            "Movie",
            'rating':
            str(movie['vote_average']),
            'img':
            "https://image.tmdb.org/t/p/w200" + movie['poster_path'],
            'img_hd':
            "https://image.tmdb.org/t/p/w1280/" + movie['poster_path']
        })
    random.shuffle(movies)
    if (type == "card"):
        return (movies)
    else:
        return (movies[0])


def similar_movies(id):
    movie = Movie()
    similar_movie = movie.similar(id)
    movies = []
    for movie in similar_movie:
        movies.append({
            "id":
            str(movie['id']),
            'title':
            movie['title'],
            'year':
            movie['release_date'][:4],
            'bio':
            movie['overview'],
            'adult':
            movie['adult'],
            'type':
            "Movie",
            'rating':
            str(movie['vote_average']),
            'img':
            "https://image.tmdb.org/t/p/w200" + movie['poster_path'],
            'img_hd':
            "https://image.tmdb.org/t/p/w1280/" + movie['poster_path']
        })
    random.shuffle(movies)
    return (movies[:20])


def similar_tv(id):
    movie = TV()
    similar_movie = movie.similar(id)
    movies = []
    for movie in similar_movie:
        try:
            movies.append({
                "id":
                str(movie['id']),
                'title':
                movie['name'],
                'year':
                movie['first_air_date'][:4],
                'bio':
                movie['overview'],
                'adult':
                None,
                'type':
                "TV Show",
                'rating':
                str(movie['vote_average']),
                'img':
                "https://image.tmdb.org/t/p/w300/" + movie['backdrop_path'],
                'img_hd':
                "https://image.tmdb.org/t/p/w1280/" + movie['backdrop_path']
            })
        except Exception:
            pass
    return (movies)


def popular_movies(type):
    movie = Movie()
    popular_movies = movie.popular()
    movies = []
    for movie in popular_movies:
        try:
            movies.append({
                "id":
                str(movie['id']),
                'title':
                movie['title'],
                'year':
                movie['release_date'][:4],
                'bio':
                movie['overview'],
                'adult':
                movie['adult'],
                'type':
                "Movie",
                'rating':
                str(movie['vote_average']),
                'img':
                "https://image.tmdb.org/t/p/w200" + movie['poster_path'],
                'img_hd':
                "https://image.tmdb.org/t/p/w1280/" + movie['backdrop_path']
            })
        except Exception:
            pass
    random.shuffle(movies)
    if (type == "card"):
        return (movies)
    else:
        return (movies[0])


def popular_tv():
    tv = TV()
    popular_tv = tv.popular()
    movies = []
    for movie in popular_tv:
        try:
            movies.append({
                "id":
                str(movie['id']),
                'title':
                movie['name'],
                'year':
                movie['first_air_date'][:4],
                'bio':
                movie['overview'],
                'adult':
                None,
                'type':
                "TV Show",
                'rating':
                str(movie['vote_average']),
                'img_poster':
                "https://image.tmdb.org/t/p/w500/" + movie['poster_path'],
                'img':
                "https://image.tmdb.org/t/p/w300/" + movie['backdrop_path'],
                'img_hd':
                "https://image.tmdb.org/t/p/w1280/" + movie['backdrop_path']
            })
        except Exception:
            pass

    #random.shuffle(movies)
    return (movies)


def get_youtube_data(id):
    a = f"https://www.youtube.com/oembed?url=https://youtu.be/{id}&format=json"
    b = (requests.get(a)).json()
    ytbe = {'title': b['title'], 'author': b['author_name'], 'id': id}
    return ytbe


def search_movie(QUERY):
    try:
        try:
            movie = Movie()
            search = movie.search(QUERY)
            movies = []
            for movie in search:
                try:
                    movies.append({
                        "id":
                        str(movie['id']),
                        'title':
                        movie['title'],
                        'year':
                        movie['release_date'][:4],
                        'bio':
                        movie['overview'],
                        'adult':
                        movie['adult'],
                        'type':
                        "Movie",
                        'rating':
                        str(movie['vote_average']),
                        'img':
                        "https://image.tmdb.org/t/p/w200" +
                        movie['poster_path'],
                        'img_hd':
                        "https://image.tmdb.org/t/p/w500/" +
                        movie['poster_path']
                    })
                except Exception:
                    movies.append({
                        "id": str(movie['id']),
                        'title': movie['title'],
                        'year': movie['release_date'][:4],
                        'bio': movie['overview'],
                        'adult': movie['adult'],
                        'type': "Movie",
                        'rating': str(movie['vote_average']),
                        'img': "/assets/images/default.png",
                        'img_hd': "/assets/images/default.png"
                    })
            return (movies)
        except Exception:
            movie = Movie()
            search = movie.search("s")
            movies = []
            for movie in search:
                try:
                    movies.append({
                        "id":
                        str(movie['id']),
                        'title':
                        movie['title'],
                        'year':
                        movie['release_date'][:4],
                        'bio':
                        movie['overview'],
                        'adult':
                        movie['adult'],
                        'type':
                        "Movie",
                        'rating':
                        str(movie['vote_average']),
                        'img':
                        "https://image.tmdb.org/t/p/w200" +
                        movie['poster_path'],
                        'img_hd':
                        "https://image.tmdb.org/t/p/w500/" +
                        movie['poster_path']
                    })
                except Exception:
                    pass
            return (movies)
    except Exception:
        return ([])


def search_tv(QUERY):
    try:
        movie = TV()
        search = movie.search(QUERY)
        movies = []
        for movie in search:
            try:
                movies.append({
                    "id":
                    str(movie['id']),
                    'title':
                    movie['name'],
                    'year':
                    movie['first_air_date'][:4],
                    'bio':
                    movie['overview'],
                    'adult':
                    None,
                    'type':
                    "TV Show",
                    'rating':
                    str(movie['vote_average']),
                    'img':
                    "https://image.tmdb.org/t/p/w300/" +
                    movie['backdrop_path'],
                    'img_hd':
                    "https://image.tmdb.org/t/p/w500/" + movie['backdrop_path']
                })
            except Exception:
                pass
        return (movies)
    except Exception:
        return ([])


def get_trailer(title, year):
    search_keyword = title.replace(" ", "%20") + "trailer%20" + str(year)
    html = urllib.request.urlopen(
        "https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return ("https://zeustv.cf/video/?vid=" + video_ids[0])


def get_decoded_url(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    a = requests.get(url, 'html.parser', headers=headers)
    code = (((a.text.split("<iframe id=")[1]).split("window.atob(")[1]
             ).split(")+")[0])
    decoded_url = base64.b64decode(code)
    return (str(decoded_url).replace("b'", "")[:-1])


def get_episode_links(id):
    url = ((f"https://seapi.link/?type=tmdb&{id[4:]}&max_results=4	").replace(
        '&s', '&season')).replace('&e', '&episode')
    b = (requests.get(url)).json()
    only_server = ['vidcloud', 'upstream', 'doodstream']
    excluded_server = [
        'netu', 'streamlare', 'mixdrop', 'fembed', 'streamzz', 'vidcloud',
        'upstream', 'videobin', 'streamsb', 'strea'
    ]
    links = []

    for item in b['results']:
        if item['server'].lower() in only_server and item['quality'] != "?":
            links.append(item)
    for item in links:
        try:
            item['url'] = get_decoded_url(item['url'])
        except Exception:
            pass
    return (links)


def get_movie_links(id):
    url = f"https://seapi.link/?type=tmdb&id={id}&max_results=4"
    b = (requests.get(url)).json()
    only_server = ['doodstream', 'streamtape']
    excluded_server = [
        'netu', 'streamlare', 'mixdrop', 'fembed', 'streamzz', 'vidcloud',
        'upstream', 'videobin', 'streamsb', 'strea'
    ]
    links = []
    links.append({
        'server':
        'Primary',
        'quality':
        'Auto',
        'url':
        os.environ['external_server'] + "/tmdb/movie?id=" + str(id)
    })

    for item in b['results']:
        #item['server'].lower() in only_server and
        if item['quality'] != "?":
            links.append(item)
    return links


def get_movie_data(id):
    movie = Movie()
    movie = movie.details(int(id))
    cast = []
    for people in (movie['casts']['cast']):
        try:
            cast.append({
                'name':
                people['name'],
                'id':
                str(people['id']),
                'char':
                people['character'],
                'img':
                "https://image.tmdb.org/t/p/w200" + people['profile_path']
            })
        except Exception:
            pass
    movie = ({
        "id":
        str(movie['id']),
        'cast':
        cast,
        "dur":
        str(movie['runtime']),
        'title':
        movie['title'],
        'year':
        movie['release_date'][:4],
        'bio':
        movie['overview'],
        'adult':
        movie['adult'],
        'type':
        "Movie",
        'rating':
        str(movie['vote_average']),
        'img':
        "https://image.tmdb.org/t/p/w200" + movie['backdrop_path'],
        'img_hd':
        "https://image.tmdb.org/t/p/w1280/" + movie['backdrop_path']
    })
    return movie


def get_season(show, season1):
    seasons = Season()
    season = []
    seasons = seasons.details(show, season1)
    episode = []
    tv = TV()
    tvdata = tv.details(int(show))

    x = 1
    for i in (seasons['episodes']):
        try:
            episode.append({
                "sno":
                i['season_number'],
                "name":
                i['name'],
                'number':
                str(i["episode_number"]),
                "id":
                "/episode?id=" + str(show) + "&s=" + str(i['season_number']) +
                "&e=" + str(i['episode_number'] - 1),
                "bio":
                i['overview'],
                "rating":
                i['vote_average'],
                "img":
                "https://image.tmdb.org/t/p/w500/" + i['still_path']
            })
        except Exception:
            episode.append({
                "sno":
                i['season_number'],
                "name":
                i['name'],
                'number':
                str(i["episode_number"]),
                "id":
                "/episode?id=" + str(show) + "&s=" + str(i['season_number']) +
                "&e=" + str(i['episode_number'] - 1),
                "bio":
                i['overview'],
                "rating":
                i['vote_average'],
                "img":
                "/assets/images/default.png"
            })

    try:
        season = ({
            "sno":
            seasons['season_number'],
            "name":
            seasons['name'],
            "showname": (tvdata['name']),
            "episodes":
            str(len(seasons['episodes'])),
            'episode':
            episode,
            "id":
            "/tv?id=" + str(show) + "&s=" + str(season1),
            "bio":
            seasons['overview'],
            "img":
            "https://image.tmdb.org/t/p/w500/" + seasons['poster_path']
        })
    except Exception:
        season = ({
            "sno": seasons['season_number'],
            "name": seasons['name'],
            "episodes": str(len(seasons['episodes'])),
            'episode': episode,
            "id": "/tv?id=" + str(show) + "&s=" + str(season1),
            "bio": seasons['overview'],
            "img": "/assets/images/default.png"
        })
    return season


def get_collection(id):
    url = f"https://api.themoviedb.org/3/collection/{id}?api_key={os.environ['apikey']}"
    b = (requests.get(url)).json()
    collection = ({
        'id':
        str(b['id']),
        'title':
        b['name'],
        'bio':
        b['overview'],
        'img':
        "https://image.tmdb.org/t/p/w1280/" + b['backdrop_path'],
        'movie_count':
        str(len(b['parts'])),
        'movies':
        b['parts']
    })
    movies = []
    for b in collection['movies']:
        movies.append({'id':str(b['id']),
        'title':b['title'],
        'bio':b['overview'],
        'img':"https://image.tmdb.org/t/p/w300/"+ b['poster_path'],
        'rating': b['vote_average'],\
        'year': b['release_date'][:4]})
    collection['movies'] = movies
    return (collection)


def get_episode(show, season1, episode1):
    season = Season()
    show_season = season.details(show, season1)
    episode = []
    cast = []
    for people in (show_season['credits']['cast']):
        try:
            cast.append({
                'name':
                people['name'],
                'id':
                str(people['id']),
                'char':
                people['character'],
                'img':
                "https://image.tmdb.org/t/p/w200" + people['profile_path']
            })
        except Exception:
            pass
    for i in (show_season['episodes']):
        try:
            episode.append({
                "sno":
                str(i['season_number']),
                "name":
                i['name'],
                "cast":
                cast,
                "number":
                str(i['episode_number']),
                "bio":
                i['overview'],
                "id":
                "/tv?id=" + str(show) + "&s=" + str(i['season_number']) +
                "&e=" + str(i['episode_number']),
                "rating":
                str(i['vote_average']),
                "img":
                "https://image.tmdb.org/t/p/w1280/" + i['still_path']
            })
        except Exception:
            episode.append({
                "sno":
                str(i['season_number']),
                "name":
                i['name'],
                "cast":
                cast,
                "number":
                str(i['episode_number']),
                "bio":
                i['overview'],
                "id":
                "/tv?id=" + str(show) + "&s=" + str(i['season_number']) +
                "&e=" + str(i['episode_number']),
                "rating":
                str(i['vote_average']),
                "img":
                "/assets/images/default.png"
            })
    return episode[episode1]


def get_tv_data(id):
    tv = TV()
    cast2 = []
    movie = tv.details(id)
    try:
        movies = ({
            "id":
            str(movie['id']),
            'cast':
            cast2,
            "dur":
            str(movie['episode_run_time']),
            'title':
            movie['name'],
            'year':
            movie['first_air_date'][:4],
            'bio':
            movie['overview'],
            'adult':
            movie['adult'],
            'seasons': (movie['seasons']),
            'season_count':
            str(len(movie['seasons'])),
            'type':
            "TV Show",
            'rating':
            str(movie['vote_average']),
            'img_poster':
            "https://image.tmdb.org/t/p/w500/" + movie['poster_path'],
            'img':
            "https://image.tmdb.org/t/p/w500/" + movie['backdrop_path'],
            'img_hd':
            "https://image.tmdb.org/t/p/w1280/" + movie['backdrop_path']
        })
    except Exception:
        movies = ({
            "id": str(movie['id']),
            'cast': cast2,
            "dur": str(movie['episode_run_time']),
            'title': movie['name'],
            'year': movie['first_air_date'][:4],
            'bio': movie['overview'],
            'adult': movie['adult'],
            'seasons': (movie['seasons']),
            'season_count': str(len(movie['seasons'])),
            'type': "TV Show",
            'rating': str(movie['vote_average']),
            'img': '/assets/images/default.png',
            'img_hd': "/assets/images/default.png"
        })
    s = []
    x = 0
    for item in movies['seasons']:
        item['id'] = str(item["season_number"])
        item['sno'] = str(item['season_number'])
        try:
            item['img'] = "https://image.tmdb.org/t/p/w500/" + item[
                'poster_path']
        except Exception:
            item['img'] = "/assets/images/default.png"
        item["episodes"] = item['episode_count']
        s.append(item)
        x += 1
    del movies['seasons']
    movies['season'] = s

    return movies


def people_movie(cast):
    movie = Discover()
    popular_movies = movie.discover_movies({
        "with_cast":
        str(cast),
        "sort_by":
        "primary_release_date.desc"
    })
    movies = []
    for movie in popular_movies:
        try:
            movies.append({
                "id":
                str(movie['id']),
                'title':
                movie['title'],
                'year':
                movie['release_date'][:4],
                'bio':
                movie['overview'],
                'adult':
                movie['adult'],
                'type':
                "Movie",
                'rating':
                str(movie['vote_average']),
                'img':
                "https://image.tmdb.org/t/p/w200" + movie['poster_path'],
                'img_hd':
                "https://image.tmdb.org/t/p/w500/" + movie['poster_path']
            })
        except Exception:
            pass
    #random.shuffle(movies)
    return movies


def people_movie_popular(cast):
    movie = Discover()
    popular_movies = movie.discover_movies({
        "with_cast": str(cast),
        "sort_by": "popularity.desc"
    })
    movies = []
    for movie in popular_movies:
        try:
            movies.append({
                "id":
                str(movie['id']),
                'title':
                movie['title'],
                'year':
                movie['release_date'][:4],
                'bio':
                movie['overview'],
                'adult':
                movie['adult'],
                'type':
                "Movie",
                'rating':
                str(movie['vote_average']),
                'img':
                "https://image.tmdb.org/t/p/w200" + movie['poster_path'],
                'img_hd':
                "https://image.tmdb.org/t/p/w500/" + movie['poster_path']
            })
        except Exception:
            pass
    #random.shuffle(movies)
    return movies


def filter_search(genre, rating, year, age):
    movie = Discover()
    if rating == "NONE" and genre == "NONE":
        dico_movies = movie.discover_movies()
    elif rating != "NONE" and genre == "NONE":
        dico_movies = movie.discover_movies({
            'vote_average.gte':
            int(rating.split("rating-")[1]),
        })
    elif rating == "NONE" and genre != "NONE":
        dico_movies = movie.discover_movies({
            'with_genres':
            tuple(map(str, genre.split("_"))),
        })
    elif rating != "NONE" and genre != "NONE":
        dico_movies = movie.discover_movies({
            'with_genres':
            tuple(map(str, genre.split("_"))),
            'vote_average.gte':
            int(rating.split("rating-")[1]),
        })
    movies = []
    for movie in dico_movies:
        try:
            movies.append({
                "id":
                str(movie['id']),
                'title':
                movie['title'],
                'year':
                movie['release_date'][:4],
                'bio':
                movie['overview'],
                'adult':
                movie['adult'],
                'type':
                "Movie",
                'rating':
                str(movie['vote_average']),
                'img':
                "https://image.tmdb.org/t/p/w200" + movie['poster_path'],
                'img_hd':
                "https://image.tmdb.org/t/p/w500/" + movie['poster_path']
            })
        except Exception:
            pass
    if year != "NONE":
        try:
            movies2 = [x for x in movies if int(x['year']) > int(year)]
            movies = movies2
        except Exception:
            movies2 = [x for x in movies if x['year'] != ""]
            movies = movies2
            movies2 = [x for x in movies if int(x['year']) > int(year)]
            movies = movies2

    if age == "under_age":
        try:
            movies2 = [x for x in movies if x['adult'] == False]
            movies = movies2
        except Exception:
            movies2 = [x for x in movies if x['adult'] != ""]
            movies = movies2
            movies2 = [x for x in movies if x['adult'] == False]
            movies = movies2

    random.shuffle(movies)
    return (movies)


#APP ROUTES/ WEBSITES
@app.route('/', methods=["POST", "GET"])
def base_page():
    keep_watch_id = (request.cookies.get("continue"))
    if keep_watch_id == None:
        continue_watch = 0
        keep_watch = []
    else:
        continue_watch = 1
        if (request.cookies.get("type")) == "tv":
            keep_watch = get_keep_watch_tv(int(keep_watch_id))
        else:
            keep_watch = get_keep_watch(int(keep_watch_id))
    movies = popular_movies("card")
    banner = popular_movies("banner")
    return render_template('index.html',
                           banner=banner,
                           categories=genres,
                           tv_shows=popular_tv(),
                           movies=movies,
                           login="Login",
                           keep_watch=keep_watch,
                           continue_watch=continue_watch,
                           col_list=collection_maker())
    #return render_template('ban.html')


@app.route('/loggingin', methods=["POST", "GET"])
def loggin_page():
    print(request.form.get('username'))


@app.errorhandler(Exception)
def http_error_handler(error):
    return render_template('error.html')


@app.route('/searchresult', methods=['POST'])
def search_page():
    ct = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    print(
        f"{ct.day}-{ct.month}-{ct.year}|{ct.hour}:{ct.minute}| {request.form['search']}"
    )
    movies = search_movie(request.form['search'])
    tv = search_tv(request.form['search'])
    if movies != None:
        #return render_template('ban.html')
        return render_template('searchresults.html',
                               movies=movies,
                               tv_shows=tv)


@app.route('/search')
def search_page2():
    return render_template('search.html')


@app.route('/videos')
def videos_page():
    return render_template('videos.html')


@app.route('/genre/')
def genre_page():
    id = request.args.get('id', default='', type=int)
    name = request.args.get('genre', default='', type=str)
    movie = genre_movie(id, "card")
    banner = movie[0]
    movie = movie[1:]
    #return render_template('ban.html')
    return render_template('genre.html',
                           banner=banner,
                           movies=movie,
                           login="Login",
                           name=name + " Movies")


@app.route('/login', methods=["POST", "GET"])
def login_page():
    return render_template('login.html')
    #return render_template('ban.html')


@app.route('/movie/')
def movie_page():
    id = request.args.get('id', default='', type=str)
    movie = get_movie_data(id)
    link = get_trailer(movie['title'], movie['year'])
    movie_link = os.environ['external_server'] + "/tmdb/movie?id=" + movie["id"]
    clips = get_movie_clips(int(id))
    return render_template('movie.html',
                           movie=movie,
                           link=link,
                           movie_link=movie_link,
                           watch_src = get_watch_src('movie', id), similar_movies=similar_movies(int(id)),
                           clips=clips,
                           comments=get_movie_review(id),
                           external=get_external(True, int(id)),
                           server=get_movie_links(int(id)))
    #return render_template('ban.html')


@app.route('/tvshow/')
def tv_page():
    id = request.args.get('id', default='', type=str)
    movie = get_tv_data(id)
    link = get_trailer(movie['title'], movie['year'])
    movie_link = os.environ['external_server'] + "/tmdb/movie?id=" + movie["id"]
    clips = get_tv_clips(int(id))
    return render_template('tvshow.html',
                           movie=movie,
                           comments=get_tv_review(id),
                           link=link,
                           movie_link=movie_link,
                           similar_movies=similar_tv(id),
													 watch_src = get_watch_src("tv", id),
                           external=get_external(False, int(id)),
                           clips=clips)


    #return render_template('ban.html')
@app.route('/collection/')
def collection_page():
    id = request.args.get('id', default='', type=str)
    movie = get_collection(id)
    return render_template('collection.html', movie=movie)


    #return render_template('ban.html')
@app.route('/season/')
def season_page():
    id = request.args.get('id', default='', type=str)
    id2 = request.args.get('s', default='', type=str)
    movie = get_season(int(id), int(id2))
    return render_template('season.html',
                           movie=movie,
                           episodes=movie['episode'])
    #return render_template('ban.html')


@app.route('/episode/')
def episode_page():
    id = request.args.get('id', default='', type=str)
    id2 = request.args.get('s', default='', type=str)
    id3 = request.args.get('e', default='', type=str)
    movie = get_episode(int(id), int(id2), int(id3))

    #NEXT EPISODE
    movie_m = get_season(int(id), int(id2))
    try:
        next_movie = movie_m['episode'][int(id3) + 1]
    except Exception:
        next_movie = 0
    if int(id3) != 0:
        prev_movie = movie_m['episode'][int(id3) - 1]
    else:
        prev_movie = 0

    movielink = os.environ['external_server'] + "/tmdb" + movie["id"]
    return render_template('episode.html',
                           movie=movie,
                           movielink=movielink,
                           next_movie=next_movie,
                           prev_movie=prev_movie,
                           parent_id=id,
                           server=get_episode_links((movie['id'])))
    #return render_template('ban.html')


@app.route('/video/')
def video_page():
    id = request.args.get('vid', default='', type=str)
    movie = get_youtube_data(str(id))
    return render_template('video.html', ytbe=movie)


@app.route('/filter', methods=['GET', 'POST'])
def filter():
    genrelist = [
        "Action", "Adventure", "Animation", "Comedy", "Crime", "Drama",
        "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
        "Romance", "Science Fiction", "Thriller", "TV Movie", "War", "Western"
    ]
    return render_template('filter.html',
                           genrelist=genrelist,
                           movies=popular_movies("card"),
                           banner=popular_movies("banner"),
                           categories=genres,
                           tv_shows=popular_tv(),
                           login="Login")


@app.route('/fsearch')
def filter_search_page():
    id_genre = request.args.get('genre', default='', type=str)
    id_rating_star = request.args.get('rating', default='', type=str)
    id_age = request.args.get('age', default='', type=str)

    id_year = request.args.get('year', default='', type=str)
    movie = filter_search(id_genre, id_rating_star, id_year, id_age)
    banner = movie[0]
    movie = movie[1:]
    #return render_template('ban.html')
    return render_template('genre.html',
                           banner=banner,
                           movies=movie,
                           login="Login",
                           name="Movies Based on Your Filter")


@app.route('/person/')
def person_page():
    id = request.args.get('id', default='', type=str)
    person = Person()
    images = get_people_images(int(id))
    p = person.details(int(id))
    person = {
        'name': p['name'],
        'bio': p['biography'],
        'dob': p['birthday'],
        'work': p['known_for_department'],
        'place': p['place_of_birth'],
        'img': "https://image.tmdb.org/t/p/w500/" + p['profile_path']
    }
    movies = people_movie(id)
    top_movies = people_movie_popular(id)
    return render_template('person.html',
                           person=person,
                           movies=movies,
                           top_movies=top_movies,
                           images=images,
                           external=get_people_external(int(id)))
    #return render_template('ban.html')


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
