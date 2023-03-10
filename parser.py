import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    options = Options()
    options.add_argument('--start-maximized')
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


if __name__ == '__main__':

    error_names = pd.read_csv('error_names.csv')
    to_find = error_names[error_names['smiles'].isna()]['Name']

    driver = get_driver()
    found_smiles = {}
    
    for i in to_find.values[930:]:
        driver.get(f'https://pubchem.ncbi.nlm.nih.gov/#query={i}')

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        featured_result = soup.find('div', attrs={'id': 'featured-results'})
        
        smiles = None
        if featured_result is not None:
            label_span = soup.find('span', string=re.compile('Isomeric SMILES'))
            if label_span is not None:
                smiles_span = label_span.find_next_sibling('span')
                smiles = smiles_span.get_text().strip()
                print(smiles_span.get_text().strip())
        
        found_smiles[i] = smiles
    
    pd.DataFrame(found_smiles, index=[0]).to_csv('found_smiles_1000.csv', index=False)
    driver.quit()
