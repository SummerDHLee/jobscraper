from bs4 import BeautifulSoup
import requests


def extract_wwr_jobs(keyword):
    pages = get_pages(keyword)
    results = []

    for page in pages:
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
                company = info.find("span", class_="company").string
                position = info.find("span", class_="title").string
                location = info.find("span", class_="region").string

                job_data = {
                    "company": company.string.replace(",", "/"),
                    "position": position.string.replace(",", "/"),
                    "location": location.string.replace(",", "/"),
                    "link": link,
                }
                results.append(job_data)
    return results


def get_pages(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    request = requests.get(f"{base_url}{keyword}")

    pages = []

    if request.status_code != 200:
        print("Can't request website: ", request.url)
    else:
        soup = BeautifulSoup(request.text, "html.parser")
        lists = soup.find_all("li", class_="view-all")
        for list in lists:
            pages.append(f"https://weworkremotely.com{list.find('a')['href']}")

    return pages
