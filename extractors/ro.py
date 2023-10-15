from bs4 import BeautifulSoup
import requests


def extract_ro_jobs(keyword):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    results = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all("tr", class_="job")
        for job in jobs:
            company = job.find("h3", itemprop="name")
            position = job.find("h2", itemprop="title")
            locations = [
                x.text.split(" ", 1)[-1] for x in job.find_all("div", class_="location")
            ]
            if company:
                company = company.string.strip()
            if position:
                position = position.string.strip()
            if locations:
                locations.pop(-1)
                location = "/".join(locations)
            if job.find("span", class_="closed") is None:
                link = (
                    "https://remoteok.com"
                    + job.find("td", class_="source").find("a")["href"]
                )
                job = {
                    "company": company,
                    "position": position,
                    "location": location,
                    "link": link,
                }
                results.append(job)
    else:
        print("Can't request website:", request.url)
    return results
