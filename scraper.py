from numpy import nan  # Missing dataset values
import pandas as pd  # Data processing, CSV file I/O (e.g. pd.read_csv)
import requests  # HTML request
from bs4 import BeautifulSoup as bs  # HTML parsing
import re  # Regex
import time  # Time sleep for failed HTML requests
import logging  # Logs management

pd.set_option('display.max_columns', 50)

''' Decorators for error handling when using bs - START '''


def log_err_set(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return set()

    return wrapper


def log_err_str(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return ""

    return wrapper


def log_err_num(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return nan  # Not a number

    return wrapper


def log_err_dict(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return {}

    return wrapper


def log_err_ps(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return 'None', set()

    return wrapper


''' Decorators for error handling when using bs - END '''


''' Functions for scraping data in HTML using bs - START '''


# Scrape player positions
@log_err_set
def scrape_positions(sp: bs):
    positions_class = sp.find_all('span', class_='Table_tag__3Mxk9 generated_utility3sm__0pg6W '
                                                 'generated_utility1lg__ECKe_')

    # Extract the text content of each position
    return {position.text for position in positions_class}


# Scrape overall
@log_err_num
def scrape_ovr(sp: bs):
    return sp.find(class_='Table_statCellValue____Twu').text


# Scrape name
@log_err_str
def scrape_name(sp: bs):
    return sp.find(class_='Table_profileCellAnchor__VU0JH').text


# Scrape stats
@log_err_dict
def scrape_stats(sp: bs):
    temp_dict = {}
    for stats in sp.findAll('div', class_='Stat_stat__lh90p generated_utility2__1zAUs'):
        stat_name = re.search('[A-Za-z]+', stats.text)[0]
        stat_name_formatted = f"_{stat_name[0:3].lower()}"  # formatted for class "player" needs
        temp_dict[stat_name_formatted] = int(re.search('[0-9]+', stats.text)[0])
    return temp_dict


# Scrape workrates
@log_err_str
def scrape_att_wr(sp: bs):
    return sp.find(string='ATT WORK RATE').parent.text[13:]


@log_err_str
def scrape_def_wr(sp: bs):
    return sp.find(string='DEF WORK RATE').parent.text[13:]


# Scrape weak foot
@log_err_num
def scrape_wf(sp: bs):
    return sp.find(string='WEAK FOOT').parent.span['aria-label'][0]


# Scrape skill moves
@log_err_num
def scrape_skills(sp: bs):
    return sp.find(string='SKILL MOVES').parent.span['aria-label'][0]


# Scrape PlayStyles
@log_err_ps
def scrape_playstyles(sp: bs):
    # Tags path for PlayStyles and PlayStyle Plus
    playstyle_tags = sp.find_all('div',
                                 class_='DetailedView_detailsItem__ZwdcY')

    if len(playstyle_tags) == 2:  # Player has a PlayStyle Plus
        temp_playstyle_plus = playstyle_tags[0].find('div',
                                                     class_='IconAttribute_attribute__KTIK0 generated_utility2__1zAUs').text
        playstyles_class = playstyle_tags[1].find_all('div',
                                                      class_='IconAttribute_attribute__KTIK0 generated_utility2__1zAUs')

    elif len(playstyle_tags) == 1:  # No PlayStyle Plus but found PlayStyles
        temp_playstyle_plus = 'None'
        playstyles_class = playstyle_tags[0].find_all('div',
                                                      class_='IconAttribute_attribute__KTIK0 generated_utility2__1zAUs')

    else:
        temp_playstyle_plus = 'None'
        playstyles_class = set()

    # Extract the text content of each playstyle and arrange in a set
    temp_playstyles = {playstyle.text for playstyle in playstyles_class}

    return temp_playstyles, temp_playstyle_plus


''' Functions for scraping data in HTML using bs - END '''


for page in range(1, 175):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/91.0.4472.124 Safari/537.36'}
    absolute = "https://www.ea.com"
    url = f"https://www.ea.com/games/ea-sports-fc/ratings?page={page}"

    # Html request handling
    html_try = 0
    html_success = False

    while not html_success and html_try < 4:
        try:
            html_try += 1
            html = requests.get(url, headers=headers)
            if html.status_code == 200:  # No exception
                html_success = True
        except requests.exceptions.RequestException:
            logging.error(f"Failed attempt no. {html_try} for http request in page {page}")
            time.sleep(2 ** html_try)  # Exponential backoff

    if not html_success:
        logging.error(f"Http request in page {page} failed. Skipping to the next page.")
        continue

    soup = bs(html.text, features="lxml")

    table = soup.find('tbody', class_='Table_tbody__gYqSw')
    for link in table.findAll('a', class_='Table_profileCellAnchor__VU0JH'):
        player_link = absolute + link['href']
        player_dict = {}
        player_html = requests.get(player_link)
        player_soup = bs(player_html.text, features="lxml")

        # Get Positions
        positions = scrape_positions(player_soup)

        # Not interested in Goalkeepers
        if 'GK' in positions:
            continue

        # Get overall
        overall = scrape_ovr(player_soup)

        # Get name of player
        name = scrape_name(player_soup)

        # Get player general stats
        stat_dict = scrape_stats(player_soup)

        # Get attacking workrate
        att_work_rate = scrape_att_wr(player_soup)

        # Get defensive workrate
        def_work_rate = scrape_def_wr(player_soup)

        # Get weak foot
        weak_foot = scrape_wf(player_soup)

        # Get skill moves
        skill_moves = scrape_skills(player_soup)

        # Get PlayStyles
        playstyles, playstyle_plus = scrape_playstyles(player_soup)

        # Update dictionary
        player_dict.update({'name': name})

        player_dict.update(stat_dict)

        player_dict.update({
            '_ovr': overall,
            'skills': skill_moves,
            'wf': weak_foot,
            'positions': positions,
            'playstyle_plus': playstyle_plus,
            'playstyles': playstyles,
            'att_wr': att_work_rate,
            'def_wr': def_work_rate
        })

        # Append to a CSV the new player data as a row
        pd.DataFrame([player_dict]).to_csv('eafc_players_new.csv', mode='a', header=False, index=False)
        print(f"Succeeded to scrape: {player_dict['name']}")
