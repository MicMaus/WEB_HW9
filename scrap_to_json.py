import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://quotes.toscrape.com/"

# define file paths
quotes_file = r"./json_files/qoutes.json"
authors_file = r"./json_files/authors.json"


def quotes_to_json():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    quotes_list = []
    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    tags = soup.find_all("div", class_="tags")

    for i in range(0, len(quotes)):
        quote_tags = []
        q = quotes[i].text
        a = authors[i].text
        tagsforquote = tags[i].find_all("a", class_="tag")
        for el in tagsforquote:
            quote_tags.append(el.text)
        quotes_list.append({"tags": quote_tags, "author": a, "quote": q})

    json_res = json.dumps(obj=quotes_list, ensure_ascii=False, indent=1)
    with open(quotes_file, "w") as fh:
        fh.write(json_res)
    print("quotes successfully recorded to json file")


def authors_links():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    full_links = []

    # find all elements where href starts with /author/:
    relative_links = soup.find_all("a", href=lambda x: x and x.startswith("/author/"))
    for el in relative_links:
        matches = re.findall(r'"(.*?)"', str(el))
        for match in matches:
            full_links.append(url + match.lstrip("/"))

    return full_links


def authors_to_json(full_links):
    fullnames = []
    born_dates = []
    born_locations = []
    descriptions = []

    for author_url in full_links:
        response = requests.get(author_url)
        soup = BeautifulSoup(response.text, "lxml")

        fullnames.append(soup.find("h3", class_="author-title"))
        born_dates.append(soup.find("span", class_="author-born-date"))
        born_locations.append(soup.find("span", class_="author-born-location"))
        descriptions.append(soup.find("div", class_="author-description"))

    authors_list = []
    for i in range(0, len(fullnames)):
        name = fullnames[i].text
        birthdate = born_dates[i].text
        birthplace = born_locations[i].text
        descrip = descriptions[i].text.strip("\n").strip()

        authors_list.append(
            {
                "fullname": name,
                "born_date": birthdate,
                "born_location": birthplace,
                "description": descrip,
            }
        )

    json_res = json.dumps(obj=authors_list, ensure_ascii=False, indent=1)
    with open(authors_file, "w") as fh:
        fh.write(json_res)
    print("authors successfully recorded to json file")


if __name__ == "__main__":
    quotes_to_json()
    authors_to_json(authors_links())
