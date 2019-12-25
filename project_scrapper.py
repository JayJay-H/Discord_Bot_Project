import requests
from bs4 import BeautifulSoup

URL = "https://computer.cnu.ac.kr/computer/notice/project.do"


def recent_info():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    table = soup.find("table", {"class": "board-table"})

    data = []

    nums = table.find_all("td", {"class": "b-num-box"})
    latest_num = nums[0].get_text(strip=True)

    titles = table.find_all("div", {"class": "b-title-box"})
    latest_title = titles[0].find("a").get_text(strip=True)

    dates = table.find_all("div", {"class": "b-m-con"})
    latest_date = dates[0].find("span", {"class": "b-date"}).get_text(strip=True)

    link = titles[0].find('a')["href"]
    latest_link = f"{URL}{link}"

    result = requests.get(latest_link)
    soup = BeautifulSoup(result.text, "html.parser")
    content = soup.find("pre", {"class": "pre"}).get_text(strip=True)
    return {"index": latest_num, "date": latest_date, "title": latest_date, "content": content}
