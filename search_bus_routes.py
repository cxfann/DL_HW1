from text_to_unicode import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import bs4
import time

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
                        - 'stops': A dictionary indicating whether there are buses (1) or not (0) at each bus stop interval.
                          Format: {'Bus Stop Name': 1 or 0}
                      If the route is not found, it returns None.

    Note:
        This function scrapes data from 'https://www.hfbus.cn' using a headless Chrome WebDriver.
        It then parses the HTML content to extract information about the specified bus route.

    Example:
        >>> search_bus_route('78')
        [{'dir': '78路(曙光影院-市府广场枢纽站)', 'time': '营运时间：05:30-22:00', 'length': '线路长度：5.8km', 'stops_num': '站点总数：7',
          'company': '所属单位：第六巴士公司',
          'stops': {'曙光影院(和平路北)': 0, '安纺总厂(和平路北)': 1, '市二院(和平路北)': 1, '和平广场南(和平路北)': 1, '东方商城(长江中路中)': 0,
                    '小东门(长江中路中)': 1, '市府广场枢纽站(徽州大道东': 1}},
         {'dir': '78路(市府广场枢纽站-曙光影院)', 'time': '营运时间：06:00-22:30', 'length': '线路长度：5.8km', 'stops_num': '站点总数：9',
          'company': '所属单位：第六巴士公司',
          'stops': {'市府广场枢纽站(徽州大道东': 0, '四牌楼(长江中路中)': 1, '小东门(长江中路中)': 0, '东方商城(长江中路中)': 1,
                    '和平广场南(和平路南)': 0, '公交集团(和平路南)': 0, '南平路口(和平路南)': 0, '安纺总厂(和平路南)': 0, '曙光影院(和平路南)': 1}}]
    """

    bus_route_unicode = txt_to_unicode(bus_route)
    url = 'https://www.hfbus.cn/map/MapIndex.html?type=line&linename=' + bus_route_unicode

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    wait = WebDriverWait(driver, 1)
    iframe_element = wait.until(EC.presence_of_element_located((By.ID, 'iframeMap')))
    driver.switch_to.frame(iframe_element)

    try:
        elements_with_common_onclick = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//b[contains(@onclick, "ShowHideLine(")]')))
    except TimeoutException:
        elements_with_common_onclick = []


    for element in elements_with_common_onclick:
        element.click()
        time.sleep(2)

    iframe_page_source = driver.page_source

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

            stops_dic = {}
            stops_details = dir.find_all('div', recursive=False)[1].find('div').find_all('div', recursive=False)[1].find('div').find('ul').find_all('li')

            for stop in stops_details:
                stop_e = stop.find('div', class_ = 'l-right').get('style', '')
                if 'display:none;' in stop_e:
                    stops_dic[stop.find('div', class_ = 'l-center').text] = 0
                else:
                    stops_dic[stop.find('div', class_ = 'l-center').text] = 1


            imformation['stops'] = stops_dic

            imformations.append(imformation)

        return imformations

# print(search_bus_route('3'))
    


