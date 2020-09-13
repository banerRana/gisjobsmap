import re
import requests
from bs4 import BeautifulSoup


def get_soup(url=None, file=None, proxy_instance=None):
    soup = None
    while True:
        try:
            if url:
                print(f'Parsing {url}')
                soup = BeautifulSoup(requests.get(url, proxies=proxy_instance.proxy, timeout=2.5).content, "html.parser")
            elif file:  # for tests
                soup = BeautifulSoup(file, "html.parser")
            if soup:
                for script in soup(["script", "style", "noscript", "a", "button"]):
                    script.extract()
                description = soup.find("div", {"class": "jobsearch-JobComponent-description"})
                if description:
                    if description.text:
                        text = description.text.replace("\"", "'")
                        text = re.sub("\s\s+", " ", text)
                        text = text.replace('\n', '\n\n')
                        return text.strip()
                return None
            else:
                return None
        except (TimeoutError, ConnectionResetError, requests.ConnectionError, requests.ConnectionError,
                requests.Timeout) as se:
            proxy_instance.retrieve_proxy(url)
            continue


def is_valid_title(title):
    if title:
        valid_terms = ['geomatics', 'geoscientist', 'remote sensing', 'geographer', 'Geography',
                       'cartographer', 'cartographic', 'cartography', 'geographic information',
                       'GEOINT', 'spatial', 'Maps', 'Mapping', 'Mapper', 'GI&S', ' gis ', 'gis ', ' gis']
        invalid_terms = ['gisborne']  # New Zealand
        for i in invalid_terms:
            if i.lower() in title.lower():
                return False
        for t in valid_terms:
            if t.lower() in title.lower():
                return True
    return False


def find_categories(title, categories):
    result = []  # max 3 results
    if title:
        for c in categories:
            if c['name'] != 'other':
                for searches in c['searches'].split(";"):
                    if searches in title.lower():
                        if c['name'] not in result:
                            result.append(c['name'])
                        if len(result) == 3:
                            break
    if len(result) == 0:
        result.append('other')
    return result


# gets tags and determines if valid
def find_tags(text, tags):
    """
    Find tags in job description
    :param text: url to search in
    :param tags: url to search in
    :return: tags
    """

    found_tags = []
    gis_specific = 0

    try:
        if text:
            for t in tags:
                regex_1 = r"\b(\s|,|>|<|\.\(\)|\·|\*|;|:|-|\(|'|\)|\")*"
                regex_2 = r"(\s|,|>|<|\.\(\)|\·|\*|;|:|-|\(|'|\)|\"|\/)*\b"
                p = re.compile(regex_1 + re.escape(t['name'].replace("-", " ")) + regex_2, re.IGNORECASE)
                result = p.search(text)
                if result:
                    found_tags.append(t['name'])
                    if t['gis']:
                        gis_specific += 1
    except Exception as e:
        print('get_tags error', str(e))
    finally:
        return {'tags': found_tags[:7],  # List with all keywords found - LIMIT of 7
                'gis_specific': gis_specific >= 2}  # a threshold of 2 gis tags == gis specific


def is_excluded_organization(value):
    excluded_orgs = ['army national guard', 'u.s. army']  # remove due to many duplicate postings
    return value.strip().lower() in excluded_orgs
