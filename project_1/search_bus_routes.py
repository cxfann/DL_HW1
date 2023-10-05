from text_to_unicode import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4

def search_bus_route(bus_route):
    """
    Retrieves information about a bus route based on the given route number.

    Args:
        bus_route (str): The route number as a string.

    Returns:
        list or None: A list of dictionaries, each containing information about a different direction of the bus route.
                      If the route is found, the list will contain dictionaries with the following keys:
                        - 'dir': The direction of the bus route.
                        - 'time': The estimated time for the entire route.
                        - 'length': The length of the route.
                        - 'stops_num': The number of stops on the route.
                        - 'company': The bus company operating the route.
                        - 'stops': A list of bus stops along the route.
                      If the route is not found, it returns None.

    Note:
        This function scrapes data from 'https://www.hfbus.cn' using a headless Chrome WebDriver.
        It then parses the HTML content to extract information about the specified bus route.

    Example:
        >>> search_bus_route('78')
        [{'dir': '78路(曙光影院-市府广场枢纽站)', 'time': '营运时间：05:30-22:00', 'length': '线路长度：5.8km', 'stops_num': '站点总数：7', 'company': '所属单位：第六巴士公司',
        'stops': ['曙光影院(和平路北)', '安纺总厂(和平路北)', '市二院(和平路北)', '和平广场南(和平路北)', '东方商城(长江中路中)', '小东门(长江中路中)', '市 府广场枢纽站(徽州大道东']}, 
        {'dir': '78路(市府广场枢纽站-曙光影院)', 'time': '营运时间：06:00-22:30', 'length': '线路长度：5.8km', 'stops_num': '站点总数：9', 'company': '所属单位：第六巴士公司', 
        'stops': ['市府广场枢纽站(徽州大道东', '四牌楼(长江中路中)', '小东门(长江中路中)', '东方商城(长江中路中)', '和平广场南(和 平路南)', '公交集团(和平路南)', '南平路口(和平路南)', '安纺总厂(和平路南)', '曙光影院(和平路南)']}]
    """

    bus_route_unicode = txt_to_unicode(bus_route)
    url = 'https://www.hfbus.cn/map/MapIndex.html?type=line&linename=' + bus_route_unicode
    
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
    
    content = content.find(class_ = 'liner')

    if content == None:

        return None
    
    else:

        two_dir = content.find_all(class_ = 'lineContent')
        imformations = []
        for dir in two_dir:
            imformation = {}
            dir_text = dir.find_all('div', recursive=False)[0].find('b').text
            imformation['dir'] = "".join(dir_text.split())

            details = dir.find_all('div', recursive=False)[1].find('table').find('tbody').find_all('tr')
            
            imformation['time'] = "".join(details[0].text.split())
            imformation['length'] = "".join(details[1].text.split())
            imformation['stops_num'] = "".join(details[2].text.split())
            imformation['company'] = "".join(details[3].text.split())

            stops_list = []
            stops_details = dir.find_all('div', recursive=False)[1].find('div').find_all('div', recursive=False)[1].find('div').find('ul').find_all('li')

            for stop in stops_details:
                stops_list.append(stop.find('div', class_ = 'l-center').text)
            imformation['stops'] = stops_list

            imformations.append(imformation)

        return imformations

print(search_bus_route('78'))
    


