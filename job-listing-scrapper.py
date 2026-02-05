import csv
import requests
from bs4 import BeautifulSoup

response = requests.get("https://realpython.github.io/fake-jobs/")
soup = BeautifulSoup(response.text, "html.parser")

job_list = soup.find_all("div", class_="card-content")
print(f"List job found : {len(job_list)}")


result = []
for list in job_list:
    title_element = list.find("h2", class_="title")
    job_title = title_element.get_text(strip=True)

    company_element = list.find("h3", class_="company")
    company_name = company_element.get_text(strip=True)

    location_element = list.find("p", class_="location")
    locaton_name = location_element.get_text(strip=True)

    footer = list.find("footer", class_="card-footer")
    apply_link = None

    if footer:
        links = footer.find_all("a", class_="card-footer-item")
        for link in links:
            if "Apply" in link.text:
                apply_link = link.get("href")
                break

    result.append(
        {
            "job": job_title,
            "company": company_name,
            "location": locaton_name,
            "url": apply_link,
        }
    )

# for item in result:
#     print(
#         f"Job : {item['job']} - Company : {item['company']} - Location : {item['location']} - URL : {item['url']}"
#     )

with open("job_listing.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["job", "company", "location", "url"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(result)

print(f"Berhasil menyimpan {len(result)} data ke file job_listing.csv")
