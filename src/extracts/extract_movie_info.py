def extract_movie_info(**kwargs):
    # main_detail
    soup = kwargs['soup']
    movie_info_div = soup.find('div', class_='main_detail')
    movie_infos = movie_info_div.find('dl', class_='list_movie').find_all('dd')
    movie = {
        'title': extract_title(div_=movie_info_div),
        'title_en': extract_title_en(div_=movie_info_div),
        'rating': extract_rating(div_=movie_info_div),
        'description': extract_description(div_=movie_info_div),
        'genre': extract_genres(dd_=movie_infos[0]),
        'country': extract_country(dd_=movie_infos[1])
    }

    if len(movie_infos) == 5:
        # 개봉 안한 영화
        movie['date'] = '0000.00.00'
        movie['time'] = extract_time(dd_=movie_infos[2])
        movie['grade'] = extract_grade(dd_=movie_infos[2])
        movie['director'] = extract_director(dd_=movie_infos[3])
        movie['actors'] = extract_actors(dd_=movie_infos[4])
    elif len(movie_infos) == 7:
        # 재개봉 한 영화
        movie['date'] = extract_date(dd_=movie_infos[2])
        movie['time'] = extract_time(dd_=movie_infos[4])
        movie['grade'] = extract_grade(dd_=movie_infos[4])
        movie['director'] = extract_director(dd_=movie_infos[5])
        movie['actors'] = extract_actors(dd_=movie_infos[6])
    else:
        # 일반 개봉영화 length -> 6
        movie['date'] = extract_date(dd_=movie_infos[2])
        movie['time'] = extract_time(dd_=movie_infos[3])
        movie['grade'] = extract_grade(dd_=movie_infos[3])
        movie['director'] = extract_director(dd_=movie_infos[4])
        movie['actors'] = extract_actors(dd_=movie_infos[5])

    return movie


def extract_title(**kwargs):
    try:
        div_ = kwargs['div_']
        title = div_.find('strong', class_='tit_movie')
        title = title.text.strip()
        result = title[:title.rfind('(')]
    except AttributeError:
        result = 'None'
    return result


def extract_title_en(**kwargs):
    try:
        div_ = kwargs['div_']
        title = div_.find('span', class_='txt_movie')
        result = title.text.strip()
    except AttributeError:
        result = 'None'
    return result


def extract_rating(**kwargs):
    try:
        div_ = kwargs['div_']
        rating = div_.find('em', class_='emph_grade')
        result = rating.text.strip()
    except AttributeError:
        result = '0.0'
    return result


def extract_genres(**kwargs):
    try:
        dd_ = kwargs['dd_']
        result = dd_.text.strip().split('/')
    except AttributeError:
        result = []
    return result


def extract_country(**kwargs):
    try:
        dd_ = kwargs['dd_']
        result = dd_.text.replace('\t', '').strip().split(',')
    except AttributeError:
        result = []
    return result


def extract_date(**kwargs):
    try:
        dd_ = kwargs['dd_']
        result = dd_.text.replace('개봉', '').strip()
    except AttributeError:
        result = '0000.00.00'
    return result


def extract_time(**kwargs):
    try:
        dd_ = kwargs['dd_']
        result = dd_.text.split(',')[0].replace('분', '').strip()
    except [AttributeError, IndexError]:
        result = '0'
    return result


def extract_grade(**kwargs):
    try:
        dd_ = kwargs['dd_']
        result = dd_.text.split(',')[1].strip()
    except [AttributeError, IndexError]:
        result = 'None'
    return result


def extract_director(**kwargs):
    try:
        dd_ = kwargs['dd_']
        result = dd_.find('a').text.strip()
    except AttributeError:
        result = 'None'
    return result


def extract_actors(**kwargs):
    try:
        dd_ = kwargs['dd_']
        if len(dd_.find_all('a')) != 0:
            result = [actor.text.strip() for actor in dd_.find_all('a')]
        else:
            result = []
    except Exception:
        result = []
    return result


def extract_description(**kwargs):
    try:
        div_ = kwargs['div_']
        result = div_.find('div', class_='desc_movie').text.replace('\n', '').replace('\t', '').replace('\r', '').strip()
        # if len(result) >= 255:
        #     result = result[:255]
    except Exception:
        result = 'None'
    return result
