#!/usr/bin/env python3

# MIT License

# Copyright (c) 2020 aniket sharma (@aniket965)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
from tqdm import tqdm
from browser import Browser

def get_soup(uri):
    req = requests.get(uri)
    return BeautifulSoup(req.content, 'html5lib')

browser = Browser.get(driver_path='/Users/aniketsharma/chromedriver').chrome

def getDetails(uri):
    try:
        html = get_soup(uri)
        table = html.find('table')
        rows = table.findAll('tr')
        company_name = rows[0].findAll('td')[1].text
        company_website = rows[1].findAll('td')[1].text
        job_role = rows[2].findAll('td')[1].text
        id = rows[3].findAll('td')[1].text 
        salary = None
        for i in range(4,8):
            r = rows[i].findAll('td')
            if 'salary' in r[0].text.lower():
                salary = r[1].text
                break
        
        spans = html.find('div', attrs={'class':'td-post-content tagdiv-type'}).findAll('span')
        link = None
        for span in spans:
            if span.find('a'):
                link = span.find('a')['href']
    except:
        return None,None,None,None,None,None
    return id,company_name,company_website,job_role,link,salary

def create_glass_door_url(company_name):
    # FIXME: if there is only one listing in salaries the main page is returend
    # handle that
    name = company_name.replace(' ', '-')
    base_url = "https://www.glassdoor.co.in" 
    search_url = "https://www.glassdoor.co.in/Salaries/{}-salary-SRCH_KE0,{}.htm".format(name,len(name))
    browser.get(search_url)
    try:
       html = BeautifulSoup(browser.page_source, 'html5lib')
       links = html.find('div',attrs={'class','salaryEmployerList'}).findAll('a')
       links = [x['href'] for x in links]
       # TODO: choose from different links
       return base_url + links[0]
    except:
        return ''
  
def getGlassDoorSalary(company_name):
    table_data = [
        ['Job Title','Salary']
    ]
    try:
        url = create_glass_door_url(company_name)
        if url == '':
            return None
        browser.get(url)
        html = BeautifulSoup(browser.page_source, 'html5lib')
        salary_rows_divs = html.findAll('div',attrs={'class':'salaryRow__SalaryRowStyle__row'})
        for row in salary_rows_divs:
            job_title = row.find('div',attrs={'class','salaryRow__JobInfoStyle__jobTitle'}).find('a').text
            salary_rows = row.find('div', attrs={'class','salaryRow__SalaryRowStyle__amt'}).findAll('div')
            if len(salary_rows) == 0:
                salary_row= row.find('div', attrs={'class','salaryRow__SalaryRowStyle__amt'})
                salary = salary_row.text
            else:                
                salary = None
                for r in salary_rows:
                    if '₹' in r.text:
                        salary = r.text
                        break
            table_data.append([job_title, salary])
        print(AsciiTable(table_data).table)
    finally:
        pass
        # browser.close()
    
def find_jobs(page=2):
    URL = "https://www.freshercooker.in/category/courses/btech-be/btech-be-cse-it/page/{}".format(page)
    req = requests.get(URL)
    soup = BeautifulSoup(req.content, 'html5lib')
    table_data = [
        ['Company','Role','Company Website','Salary']
    ]
    jobs_div = soup.findAll('div', attrs={'class':'td_module_16 td_module_wrap td-animation-stack'})
        
    for job_div in tqdm(jobs_div):
        job_detail_div = job_div.find('div', attrs={'class':'item-details'})
        job_page_anchor = job_detail_div.find('a', attrs={'rel':'bookmark'})  
        link_job_page = job_page_anchor['href']
        job_title = job_page_anchor['title']
        description = job_detail_div.find('div',attrs={'class':'td-excerpt'}).text
        id,company_name,company_website,job_role,link,salary= getDetails(link_job_page)
        # print(id,company_name,company_website,job_role,link)
        # getGlassDoorSalary(company_name)
        table_data.append([company_name,job_role,company_website,salary])
        # break
        # print(job_title)
        # print(link_job_page)
        # print(description)
        # print(link)
    print(AsciiTable(table_data).table)




if __name__ == '__main__':
    # TODO: selectable jobs,keep track in json
    # TODO: open links directly by selecting company
    # TODO: add filters
    # TODO: make code modular to add more website
    # TODO: make applied jobs record
    
    find_jobs(page=3)
    browser.close()
    # print(create_glass_door_url('snap on inc'))