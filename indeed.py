import requests
from bs4 import BeautifulSoup


# indeed의 url을 분석하여 limit와 url을 잘 조합한다.
LIMIT = 50 


# 마지막 페이지를 알아낸다
def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div",{"class": "pagination"})
    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.find("span").string))    
    max_page = pages[-1]    
    return max_page


# extract_jobs에서 쓰이는 용도
# 하나의 페이지에서 반복되는 job의 정보를 추출
def extract_job(html):
    title = html.find("h2",{"class":"title"}).find("a")["title"]        
    company = html.find("span",{"class":"company"})
    if company:
        company_anchor = company.find("a")
        if company.find("a") is not None:
            company = (str(company_anchor.string))
        else:
            company = (str(company.string))        
        company = company.strip()    
    else:
        company: None
    location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]    
    return {"title": title, "company": company, "location":location ,"link":f"https://kr.indeed.com/viewjob?jk={job_id}"}
    

# 마지막페이지까지 반복하며 페이지마다 job의 정보를 모두 추출
def extract_jobs(last_page, url):    
    jobs=[]
    for page in range(last_page):
        print(f"scrapping indeed: page: {page+1}")
        result = requests.get(f"{url}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
        for result in results:        
            job = extract_job(result)        
            jobs.append(job)
    return jobs

        
def get_jobs(word):    
    url = f"https://kr.indeed.com/jobs?q={word}&limit={LIMIT}"
    last_page = get_last_page(url)
#     너무 많이 뽑혀서 2번만 반복하게 만듭(2개의 페이지에서만 정보를 뽑아옴)
#     jobs = extract_jobs(last_page)    
    jobs = extract_jobs(2,url)    
    return  jobs



