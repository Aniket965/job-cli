
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


from utilities import get_soup
from BaseScraper import BaseScraper
from job import Job
class FresherCookerScraper(BaseScraper):
    
    def __str__(self):
        return '[*] Using {} for scraping jobs'.format(self.name)
    
    def generateNextPageLink(self,num):
        url = "https://www.freshercooker.in/category/courses/btech-be/btech-be-cse-it/page/{}".format(num)
        return url
    def scrapeJobPage(self, url) -> Job:
            try:
                html = get_soup(url)
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
                return None
        
            return Job(company_name,company_website,job_role,job_link=link,salary=salary)
    
    def scrapeJobListingPage(self,url):
        soup = get_soup(url)
        job_listing_links = []
        jobs_div = soup.findAll('div', attrs={'class':'td_module_16 td_module_wrap td-animation-stack'})
            
        for job_div in jobs_div:
            job_detail_div = job_div.find('div', attrs={'class':'item-details'})
            job_page_anchor = job_detail_div.find('a', attrs={'rel':'bookmark'})  
            link_job_page = job_page_anchor['href']
            job_listing_links.append(link_job_page)
        return job_listing_links