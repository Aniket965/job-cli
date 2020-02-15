
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


from bs4 import BeautifulSoup

class GlassdoorSalaryFinder:
    def __init__(self,salary_page_url):
        self.salary_page_url = salary_page_url
    def findSalaries(self):
        browser.get(self.salary_page_url)
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
        