import json
import logging
import os
import time
from datetime import datetime
import requests
from indeed import IndeedClient

from scraper.api import DataAPI
from scraper.pia_proxy import Proxy
from scraper.utils import find_categories, find_tags, is_valid_title, get_soup, is_excluded_organization
from config import api_url, search_terms, search_countries, log_file


logging.basicConfig(level=logging.DEBUG,
                    filename=log_file, filemode='w',
                    format='%(name)s %(levelname)s %(message)s')

client = IndeedClient(publisher=os.environ.get('INDEED_KEY'))

prxy = Proxy()

params = {
    'q': None,
    'start': 0,
    'limit': 25,
    'format': 'json',
    'userip': '1.2.3.4',
    'highlight': 0,
    'filter': 1,
    'latlong': 1,
    'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
    'co': None,
    'l': ''  # location, try 'remote'
}


def run():
    print('executing scraper...')
    api = DataAPI()
    status = {
        'time_start': datetime.utcnow(),
        'time_end': None,
        'errors': 0,
        'is_success': True,
        'messages': '',
        'new': 0,
        'expired': 0,
        'total_valid': 0,
        'processed': 0
    }

    try:
        prxy.retrieve_proxy(api_url)
        for country_code in search_countries:
            params['co'] = country_code
            api.get_invalid_jobkeys()
            api.get_valid_jobkeys(country_code)
            for search_term in search_terms:
                params['start'] = 0
                params['limit'] = 25
                params['q'] = search_term
                total_results = 25
                result_number = 0
                while result_number <= int(total_results):
                    search_response = client.search(**params, proxies=prxy.proxy)
                    total_results = search_response['totalResults']
                    results = search_response.get('results')
                    print(f"{country_code.upper()} ({search_term}) ---> result {result_number}/{total_results}")
                    if not results:
                        break
                    for r in results:
                        try:
                            jobkey = r['jobkey']
                            jobtitle = r['jobtitle']
                            company = r['company']
                            city = r['city']
                            state = r['state']
                            formatted_location = r['formattedLocation']
                            date = r['date']
                            date4db = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
                            url = r['url']
                            if jobkey in api.invalid:
                                result_number += 1
                                continue
                            if jobkey in api.new_invalid:
                                result_number += 1
                                continue
                            if jobkey in api.current_active:
                                result_number += 1
                                continue
                            if jobkey in api.valid_active:
                                api.current_active.append(jobkey)
                                result_number += 1
                                continue
                            if jobkey in api.valid_inactive:
                                api.set_active_inactive(keys=[jobkey], task='active')
                                api.current_active.append(jobkey)
                                status['new'] += 1
                                result_number += 1
                                continue
                            soup = get_soup(url=url, proxy_instance=prxy)
                            is_jobtitle_valid = is_valid_title(jobtitle)
                            tags = find_tags(soup, api.tags)
                            try:
                                if (tags['gis_specific'] or is_jobtitle_valid) and not is_excluded_organization(
                                        company):
                                    job_categories = find_categories(jobtitle, api.categories)
                                    payload = {
                                        'indeedKey': jobkey,
                                        'title': jobtitle,
                                        'company': company,
                                        'url': url,
                                        'city': city,
                                        'state': state,
                                        'countryCode': r.get('country', country_code),
                                        'lat': r.get('latitude', 0),
                                        'lon': r.get('longitude', 0),
                                        'formattedLocation': formatted_location,
                                        'isRemote': True if formatted_location.lower().strip() in ['remote',
                                                                                                   'telework',
                                                                                                   'telecommute'] else False,
                                        'searchTerm': search_term,
                                        'description': soup,
                                        'publishDate': date4db,
                                        'tags': tags['tags'],
                                        'categories': job_categories,
                                        'dataSource': 'indeed'
                                    }
                                    api.add_valid_job(payload)
                                    api.current_active.append(jobkey)
                                    status['new'] += 1
                                    print(f"New Job: {company} - {jobtitle}\n\n")
                                else:
                                    api.new_invalid.append(jobkey)
                            except Exception as e:
                                print('General Exception: {}. '.format(str(e)))
                                status['messages'] += ' | {}'.format(str(e))
                                status['errors'] += 1
                                logging.error(str(e))
                                continue
                            result_number += 1
                        except (TimeoutError, ConnectionResetError, requests.ConnectionError, requests.RequestException,
                                requests.Timeout) as se:
                            prxy.retrieve_proxy(api_url)
                            continue
                    params['start'] += 25
                    params['limit'] += 25
                status['processed'] += params['start']
            # end country iteration
            expired = [item for item in api.valid_active if
                       item not in api.current_active]
            if len(expired):
                api.set_active_inactive(keys=expired, task='inactive')
                status['expired'] += len(list(set(expired)))
            if len(api.new_invalid):
                api.add_invalid_jobkeys(api.new_invalid)
                api.new_invalid = []
            status['total_valid'] += len(list(set(api.valid_active)))
    except Exception as e:
        status['is_success'] = False
        status['messages'] += 'General Exception: {}. | '.format(str(e))
        logging.error('General Exception: {}. '.format(str(e)))
    finally:
        status['time_end'] = datetime.utcnow()
        api.set_status(status)
        api.logout()
        print("\n\n**Scrape Complete**")
        print("*" * 30)
        print(json.dumps(status, indent=4, sort_keys=True, default=str))
        print("*" * 30)
        time.sleep(30 * 60)  # sleep for 30 minutes between runs


if __name__ == "__main__":
    run()
