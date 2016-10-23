import httplib2
from BeautifulSoup import BeautifulSoup


def scrape():
    url = 'http://www.digitaltrends.com/home-theater/whats-new-on-netflix-shows-movies/'
    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response)
    grouped_by_date = soup.find('div', {'class': 'item-grid cols-1'})
    shows = grouped_by_date.findAll('p')
    show_list = []
    for show in shows:
        date = show.findPrevious('h3').text
        for s in show:
            try:  # stripping the tags
                show_list.append([date + ':', s.text.strip()])
            except:  # way to add the season to the show
                show_list[-1].append(s.strip())
    cleaned_of_spaces = (x for x in show_list if x[-2:] != ['', ''])  # somehow: phantom seasons and shows
    cleaned_join_by_season = (' '.join(x) for x in cleaned_of_spaces)  # joining season and show (if season)
    cleaned = (x.replace('&#8217;', "'") for x in cleaned_join_by_season)  # encoding issue
    return cleaned


def write_cleaned(cleaned):
    with open('new_on_netflix.txt', 'w') as f:
        for x in cleaned:
            f.write(x + '\n')

if __name__ == '__main__':
    results = scrape()
    write_cleaned(results)
