import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

def fetch_job_info(position, location, geo_id):
    """Fetch job details from LinkedIn."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    job_list = []
    target_url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={position}&location={location}&geoId={geo_id}&start={{}}'
    
    for i in range(0, 1):
        res = requests.get(target_url.format(i), headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        all_jobs = soup.find_all("li")
        
        for job in all_jobs:
            try:
                job_id = job.find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
                detailed_url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}'
                detailed_res = requests.get(detailed_url, headers=headers)
                detailed_soup = BeautifulSoup(detailed_res.text, 'html.parser')
                
                company = detailed_soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt') if detailed_soup.find("div", {"class": "top-card-layout__card"}) else "Unknown"
                title = detailed_soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip() if detailed_soup.find("div", {"class": "top-card-layout__entity-info"}) else "Unknown"
                level = detailed_soup.find("ul", {"class": "description__job-criteria-list"}).find("li").text.replace("Seniority level", "").strip() if detailed_soup.find("ul", {"class": "description__job-criteria-list"}) else "Unknown"
                
                # Extract number of applicants
                num_applicants = detailed_soup.find("figcaption", {"class": "num-applicants__caption"})
                num_applicants = num_applicants.text.strip() if num_applicants else "Unknown"
                
                # Extract job posted date
                posted_date = detailed_soup.find("span", {"class": "posted-time-ago__text"})
                posted_date = posted_date.text.strip() if posted_date else "Unknown"
                
                # Extract job description
                job_desc = detailed_soup.find("div", {"class": "show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden"})
                job_desc = job_desc.text.strip() if job_desc else "Unknown"
                
                job_list.append({
                    "job_id": job_id, 
                    "company": company, 
                    "job_title": title, 
                    "level": level, 
                    "num_applicants": num_applicants, 
                    "posted_date": posted_date, 
                    "job_description": job_desc, 
                    "application_link": get_application_link(job_id)  # Fetch application link
                })
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
    
    return job_list

def get_application_link(job_id):
    """Fetch job application link using requests and BeautifulSoup."""
    search_url = f"https://www.linkedin.com/jobs/view/{job_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return f"Failed to fetch page, status code: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")

    # Find application link
    link_element = soup.find("a", class_="sign-up-modal__company_webiste")  # Update class if needed
    return link_element["href"] if link_element else "Application link not found"

def main():
    position = "Data Scientist"
    location = "Las Vegas, Nevada, United States"
    geo_id = "100293800"
    
    job_list = fetch_job_info(position, location, geo_id)
    
    df = pd.DataFrame(job_list)
    df.to_csv("jobs_with_application_links.csv", index=False)
    print("Job information with application links saved to jobs_with_application_links.csv")

if __name__ == "__main__":
    main()
