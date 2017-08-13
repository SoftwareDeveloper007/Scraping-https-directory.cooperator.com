from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

import csv
import time
import threading

def open_url(url, num_retries=5):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
    except:
        if num_retries > 0:
            driver.quit()
            open_url(url, num_retries-1)
    driver.maximize_window()
    return driver

class scraper_directory_cooperator():
    def __init__(self, company_manufacturer):
        self.url = 'https://directory.cooperator.com/'
        self.company_manufacturer = company_manufacturer
        self.total_data = []
        self.page_number = 0
        self.start_url = ''
        self.next_url = []

    def start_scraping(self):
        self.driver = open_url(self.url)

        input = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#keyword")))

        search_btn = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.standardButton")))
        search_btn = search_btn.find_elements_by_tag_name('li')[0].find_element_by_tag_name('input')

        input.send_keys(self.company_manufacturer)
        search_btn.click()
        time.sleep(3)

        self.firstpage_scraping()
        #self.total_threading()
        #self.save_csv()

    def firstpage_scraping(self):
        # trs = self.driver.find_elements_by_css_selector('div.single_result_wrapper')
        tbs = WebDriverWait(self.driver, 50).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "table.listingSummary")))

        view_contacts = self.driver.find_elements_by_link_text('view contact')
        for view_contact in view_contacts:
            view_contact.click()

        view_phones = self.driver.find_elements_by_link_text('view phone')
        for view_phone in view_phones:
            view_phone.click()

        view_faxes = self.driver.find_elements_by_link_text('view fax')
        for view_fax in view_faxes:
            view_fax.click()

        for tb in tbs:
            text = tb.text
            text = text.split('\n')
            if 'add to quick list' in text:
                text.remove('add to quick list')
            if 'Add to Quick List' in text:
                text.remove('Add to Quick List')
            if 'email to friend' in text:
                text.remove('email to friend')
            if 'Email to Friend' in text:
                text.remove('Email to Friend')
            if '' in text:
                text.remove('')

            company_name = text[0]
            address = ''
            phone_number = ''
            fax = ''
            website = ''
            email = ''

            for i in range(1, len(text)):
                if 't: ' in text[i]:
                    phone_number = text[i].replace('t: ', '')
                elif 'f: ' in text[i]:
                    fax = text[i].replace('f: ', '')
                elif 'w: ' in text[i]:
                    website = text[i].replace('w: ', '')
                elif 'e: ' in text[i]:
                    email = text[i].replace('e: ', '')
                else:
                    address = address + text[i] + ', '
                address = address[0:len(address)-1]

            self.total_data.append({
                'company name': company_name,
                'address': address,
                'phone number': phone_number,
                'fax': fax,
                'website': website,
                'email': email
            })

        self.driver.quit()


    def save_csv(self):

        filename = self.company_manufacturer + '.csv'
        self.output_file = open(filename, 'w', encoding='utf-8', newline='')
        self.writer = csv.writer(self.output_file)
        headers = ['Company Name', 'Address', 'Phone Number', 'Fax', 'Website', 'Email']
        self.writer.writerow(headers)

        for i, elm in enumerate(self.total_data):
            row = [
                elm['company name'],
                elm['address'],
                elm['phone number'],
                elm['fax'],
                elm['website'],
                elm['email']
            ]
            self.writer.writerow(row)

        self.output_file.close()


if __name__ == '__main__':
    app = scraper_directory_cooperator('Electrical')
    app.start_scraping()
    app.save_csv()




