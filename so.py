import requests
from bs4 import BeautifulSoup
import csv



def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    pages = soup.find("div",{"class": "s-pagination"}).find_all("a")    
    last_pages = pages[-2].get_text(strip=True)
    return int(last_pages)



def extract_job(html):
    title = html.find("h2").find("a")["title"]    
    company_row = html.find("h3").find_all("span",recirsove=False)        
    company = company_row[0].get_text(strip=True)
    location = company_row[1].get_text(strip=True).strip("-").strip(" \r").strip("\n").strip("")
    job_id = html["data-jobid"]
    link = f"https://stackoverflow.com/jobs/{job_id}"    
    return {"title":title , "company":company,"location":location , "link":link}    
    

    
    
def extract_jobs(last_page,url):
    jobs=[]
    for page in range(last_page):
        print(f"scrapping SO: Page: {page+1}")        
        result = requests.get(f"{url}&pg={page+1}")
        #         print(result.status_code)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div",{"class":"-job"})        
        for result in results:
            job = extract_job(result)            
            jobs.append(job)
    return jobs
    
    
    
def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(url)
#     너무 많이 뽑혀서 2번만 반복하게 만듭(2개의 페이지에서만 정보를 뽑아옴)
#     jobs = extract_jobs(last_page)
    jobs = extract_jobs(2,url)
    return jobs





