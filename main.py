import requests, re
import pandas as pd
from bs4 import BeautifulSoup

job_listings = []

def format_input(job_title, location):
    job_title = re.sub(r"\s+", '+', job_title)
    location = re.sub(r"\s+", '%2C+', location)
    formated_input = {'job title':job_title, 'location':location}
    return(formated_input)

def job_search():
    job_title = str(input('Enter Job Title: '))  
    location = str(input('Enter location ie(Bronx ny): '))
    input_dict = format_input(job_title, location)
    return input_dict

def construct_url(dict,page):
    url = 'https://www.indeed.com/jobs?q={}&l={},&start={}'.format(dict['job title'],dict['location'],page)
    return url

def get_html(dict,pages):
    for page in range(0,pages,10):
        print('Getting Page', page)
        url = construct_url(dict,page)
        headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        r = requests.get(url,headers=headers)
        if r.status_code != 200:
            print(r.status_code)
        else:
            soup = BeautifulSoup(r.content, 'html.parser')  
            parse_data(soup)

def parse_data(soup):
    divs = soup.find_all('div', class_ = 'jobsearch-SerpJobCard')
    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span', class_ = 'company').text.strip()
        if item.find('span', class_ ='salaryText'):
            salary = item.find('span', class_ ='salaryText').text.strip()
        else:
            salary = 'No Salary Data'
        summary = item.find('div', {'class' : 'summary'}).text.strip()
        link = item.find('a', href=True)['href']
        listing = {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary,
            'link':link
        }
        job_listings.append(listing)

def csv_create(jobs):
    df =pd.DataFrame(jobs)
    print(df.head())
    df.to_csv('jobs.csv')

def main():
    search_data = job_search() # returns dict
    pages = 40
    soup = get_html(search_data, pages)
    csv_create(job_listings)

if __name__ == '__main__':
    main()