import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal'

tema = 'seleção brasileira'

# Instanciando o webdriver usando o gerenciado de contexto
options = webdriver.EdgeOptions()
options.add_argument('--start-maximized')
html = None
with webdriver.Edge(options=options) as driver:

    driver.get(url=url)
    search_box = driver.find_element(By.NAME,'search')
    search_box.send_keys(tema)
    search_box.submit()

    desambiguificacao_icon = driver.find_element(by=By.XPATH,value='//*[@id="disambig"]/table/tbody/tr/td[1]/span/a/img')
    xpath_element = driver.find_elements(by=By.XPATH,value='//*[@id="firstHeading"]')
    if desambiguificacao_icon:
        driver.find_element(by=By.XPATH,value='//*[@id="mw-content-text"]/div[1]/ul/li[1]/a').click()
        print("Desambiguificação")
    elif xpath_element:
        if xpath_element[0].text == 'Resultados da pesquisa':
            print("Pesquisa avançada")
            driver.find_element(by=By.XPATH,value='//*[@id="mw-content-text"]/div[3]/div[4]/ul/li[1]/div[2]/div[2]/div[1]/a').click()
        else:
            print('página wiki')
    
    html = driver.page_source

soup = BeautifulSoup(html,'html.parser')

tables = soup.find_all('table')

for table in tables:
    df = pd.read_html(str(table))[0]
    print(df.head())