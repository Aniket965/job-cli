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
        