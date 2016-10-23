import httplib2
from BeautifulSoup import BeautifulSoup
import json


class Show(dict):
    def __init__(self):
        super().__init__()
        self.dict_by_date = {}
        self.date = None
        self.show = None

    def add_date(self, date):
        self.date = date
        self.dict_by_date['date'] = self.date

    def add_show(self, show):
        self.show = show
        for k, v in self.show.items():
            self.dict_by_date[k] = v

    def get_dict(self):
        return self.dict_by_date

    def to_json(self):
        data = json.dumps(self.dict_by_date)
        return data


def scrape_ratings(show):
    movie = '+'.join(x for x in show.split())
    show_attrs = dict()
    url = 'http://www.rottentomatoes.com/search/?search='
    show_attrs['show'] = show.strip()
    movie = movie.split()
    movie = '+'.join(x for x in movie)
    final = url + movie
    http = httplib2.Http()
    status, response = http.request(final)
    soup = BeautifulSoup(response)

    # critics average_rating, reviews counted, fresh, rotten
    critic_reviews = soup.find('div', {'id': 'scoreStats'})
    try:
        for x in critic_reviews.findAll('div'):
            key, value = x.text.split(':')
            if key in ['average rating']:
                continue
            if len(key.split()) > 1:
                key = '_'.join(x for x in key.split())
            key = str(key).lower()
            show_attrs[key] = str(value)
    except AttributeError:
        pass

    tomatometer = soup.find('span', {"class": "meter-value superPageFontColor"})
    show_attrs['tomatometer'] = str(tomatometer.text) if tomatometer else None

    audience = soup.find('span', {"class": "superPageFontColor", "style": "vertical-align:top"})
    show_attrs['audience_rating'] = str(audience.text) if audience else None
    more_audience = soup.find('div', {"class": "audience-info hidden-xs superPageFontColor"})
    try:
        # average_rating, user_ratings
        for x in more_audience.findAll('div'):
            key, value = x.text.split(':')
            key = '_'.join(x for x in key.lower().split())
            show_attrs[str(key)] = str(value)
    except AttributeError:
        pass

    critic_consensus = soup.find('p', {"class": "critic_consensus superPageFontColor"})
    show_attrs['critic_consensus'] = str(critic_consensus.text.split(':', 1)[-1]) \
                                         if critic_consensus else 'No critic consensus'

    return show_attrs


def main():
    with open('new_on_netflix.txt') as f:
        for line in f:
            s = Show()
            date, show = line.split(':', 1)
            s.add_date(date)
            s.add_show(scrape_ratings(show))
            print(s.get_dict())


if __name__ == '__main__':
    main()
