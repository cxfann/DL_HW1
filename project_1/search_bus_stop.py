from text_to_unicode import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4

def search_bus_stop(bus_stop):
    """
    Retrieves information about a bus stop based on the given stop name.

    Args:
        bus_stop (str): The name of the bus stop as a string.

    Returns:
        list or None: A list of dictionaries, each containing information about a different bus route
                      passing through the specified bus stop. If the stop is found, the list will contain
                      dictionaries with the following keys:
                        - 'name': The name of the bus stop.
                        - 'route': A list of bus route names passing through the stop.
                      If the stop is not found, it returns None.

    Note:
        This function scrapes data from 'https://www.hfbus.cn' using a headless Chrome WebDriver.
        It then parses the HTML content to extract information about the specified bus stop.

    Example:
        >>> search_bus_stop('双岗南')
        [{'name': '双岗南(阜阳路-东)', 'route': ['5路', '4路', 'B9路', '46路', '10路', 'e54路', '155路', '117路', '114路', '109路', 'T797路']},
         {'name': '双岗南(阜阳路-西)', 'route': ['5路', '4路', 'T2路', 'B9路', '46路', '14路', '10路', 'e54路', '155路', '137路', '117路', '114路', '109路']}]
    """


    bus_stop_unicode = txt_to_unicode(bus_stop)
    url = "https://www.hfbus.cn/map/MapIndex.html?type=station&stationname=" + bus_stop_unicode

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    wait = WebDriverWait(driver, 0.3)
    iframe_element = wait.until(EC.presence_of_element_located((By.ID, 'iframeMap')))


    driver.switch_to.frame(iframe_element)

    iframe_page_source = driver.page_source

    driver.switch_to.default_content()

    driver.quit()

    bs = bs4.BeautifulSoup(iframe_page_source, 'html.parser')

    content = bs.find('div', id = 'r-result')
    content = content.find(class_ = 'stationList')

    if content == None:
        return None
    else:
        imformations = []
        stations = content.find(class_ = 'box').find('ul').find_all('li', recursive=False)
        for station in stations:
            imformation = {}
            name_text = station.find('tbody').find('tr').find_all('td')[1].text
            imformation['name'] = "".join(name_text.split())
            
            routes = station.find(class_='linestr').find_all('a')
            routes_name = []
            for route in routes:
                route_text = route.text
                routes_name.append("".join(route_text.split()))
                
            imformation['route'] = routes_name
            
            imformations.append(imformation)
        return imformations


print(search_bus_stop('稻香村'))