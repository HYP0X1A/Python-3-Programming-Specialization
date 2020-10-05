import json
import requests_with_caching

def get_sorted_recommendations(x):
    recs = get_related_titles(x)
    best = sorted(recs,key = lambda x: (get_movie_rating(get_movie_data(x)), x), reverse = True)
    return(best)

def get_movies_from_tastedive(search):
    url = "https://tastedive.com/api/similar"
    d = {}
    d['q'] = search
    d['limit'] = '5'
    d['type'] = 'movies'
    resp = requests_with_caching.get(url, params = d)
    return(resp.json())

def extract_movie_titles(movies):
    lst = []
    for x in movies['Similar']['Results']:
        lst.append(x['Name'])
        print(x)
    return(lst)

def get_related_titles(movie_lst):
    related = []
    for movie in movie_lst:
        res = extract_movie_titles(get_movies_from_tastedive(movie))
        for y in res:
            if y not in related:
                related.append(y)
    return(related)

def get_movie_data(movie):
    url = "http://www.omdbapi.com/"
    d = {}
    d['t'] = movie
    d['r'] = 'json'
    resp = requests_with_caching.get(url, params = d)
    return(resp.json())

def get_movie_rating(movies):
    print(movies['Ratings'])
    val = 0
    for x in range(len(movies['Ratings'])):
        if movies['Ratings'][x]['Source'] == 'Rotten Tomatoes':
            tmp = movies['Ratings'][x]['Value']
            val = int(tmp.replace('%',''))
    return(val)

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
