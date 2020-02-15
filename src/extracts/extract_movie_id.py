def extract_movie_ids(**kwargs):
    soup = kwargs['soup']
    results = []

    movie_divs = soup.find_all('div', class_='desc_boxthumb')
    for div in movie_divs:
        results.append(div.find('a')['href'].split('=')[1])

    return results
