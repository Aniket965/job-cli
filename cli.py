
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


import math
from Scrapers import Scrapers
from xlwt import Workbook,easyxf
import xlwt
from os import path
from tqdm import tqdm
class Jobcli:
    
    def __init__(self,n,default_scraper='fresher_cooker'):
        self.no_of_jobs = n
        self.jobs = []
        self.scraper = Scrapers.get(default_scraper)
        
    def run(self):
        print(self.scraper)
        job_listing_links = []
        r = math.ceil(self.no_of_jobs / self.scraper.jobs_per_page)
        for i in range(r):
            links = self.scraper.scrapeJobListingPage( self.scraper.generateNextPageLink(i+1))
            job_listing_links.extend(links)
        for job_url in tqdm(job_listing_links[0:self.no_of_jobs]):
            self.jobs.append(self.scraper.scrapeJobPage(job_url))
            
    def generate_excel(self,outdir):
        print('[*] Generating Excel Sheet')
        wb = Workbook()
        sheet = wb.add_sheet('Jobs')
        style = easyxf('font: bold 1')
        sheet.write(0,0,'Status',style)
        sheet.write(0,1,'Company Name',style)
        sheet.write(0,2,'Job Role', style)
        sheet.write(0,3,'Company Website', style)
        sheet.write(0,4,'Job Link', style)
        sheet.write(0,5,'Salary', style)
        for i,job in enumerate(self.jobs):
            sheet.write(i+1,1,job.company_name)
            sheet.write(i+1,2,job.job_role)
            sheet.write(i+1,3,xlwt.Formula('HYPERLINK("%s";"Website")' % job.company_website))
            sheet.write(i+1,4,xlwt.Formula('HYPERLINK("%s";"Apply")' % job.job_link))
            sheet.write(i+1,5,job.salary)
        wb.save(path.join(outdir,'jobs.xls'))
        print('[*] Generated Excel Sheet named as jobs.xls')