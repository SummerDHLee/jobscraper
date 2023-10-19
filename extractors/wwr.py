from bs4 import BeautifulSoup
import requests


def extract_wwr_jobs(keyword):
    pages, results = get_pages(keyword)

    for page in pages:
        # print(page,"\n")
        request = requests.get(page)
        if request.status_code != 200:
            print("Can't request website: ", request.url)
        else:
            soup = BeautifulSoup(request.text, "html.parser")
            jobs = soup.select(
                "section.jobs > article > ul > li:not(:first-of-type):not(:last-of-type)"
            )
            for job in jobs:
                info = job.find("a", recursive=False)
                link = f"https://weworkremotely.com{info["href"]}"
                company = info.find("span", class_="company").string.replace(",", "/")
                position = info.find("span", class_="title").string.replace(",", "/")
                location = info.find("span", class_="region").string
                if location is not None:
                    location.replace(",", "/")
                else: 
                    location= "-"

                job_data = {
                    "company": company,
                    "position": position,
                    "location": location,
                    "link": link,
                }
                results.append(job_data)
    return results


def get_pages(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    request = requests.get(f"{base_url}{keyword}")

    pages = []
    results = []

    if request.status_code != 200:
        print("Can't request website: ", request.url)
    else:
        soup = BeautifulSoup(request.text, "html.parser")
        sections = soup.find_all("section", class_="jobs")
        # for section in sections:
        #     print(section)
        lists = soup.find_all("li", class_="view-all")
        for list in lists:
            pages.append(f"https://weworkremotely.com{list.find('a')['href']}")

    return pages, results
