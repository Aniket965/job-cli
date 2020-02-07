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

def get_soup(uri):
    req = requests.get(uri)
    return BeautifulSoup(req.content, 'html5lib')
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
        table_data.append([company_name,job_role,company_website,salary])
        # break
        # print(job_title)
        # print(link_job_page)
        # print(description)
        # print(link)
    print(AsciiTable(table_data).table)


if __name__ == '__main__':
    # TODO: selectable jobs,keep track in json
    # TODO: find salaries from glass door which are named as best in industry
    # TODO: open links directly by selecting company
    # TODO: add filters
    # TODO: make code modular to add more website
    # TODO: make applied jobs record
    
    find_jobs(page=3)