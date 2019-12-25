import requests
import info
from bs4 import BeautifulSoup

URL = "https://computer.cnu.ac.kr/computer/notice/notice.do"
line = "------------------------------------------------------------------------------------------------"
last_update = info.get_last_update()


def recent_info():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    table = soup.find("table", {"class": "board-table"})

    data = []

    nums = table.find_all("td", {"class": "b-num-box"})
    titles = table.find_all("div", {"class": "b-title-box"})
    dates = table.find_all("div", {"class": "b-m-con"})

    for n, t, d in zip(nums, titles, dates):
        date = d.find('span', {'class': 'b-date'}).get_text(strip=True)
        check = info.check(last_update, date)
        if check:
            num = n.get_text(strip=True)
            title = t.find("a").get_text(strip=True)
            link = URL + t.find('a')['href']

            data.append({'index': num, 'title': title, 'date': date, 'link': link})

    return data


async def send(message):
    n_channel = message.channel
    information = recent_info()
    if len(information) == 0:
        await n_channel.send(f'▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒[일반소식]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n{line}')
        await n_channel.send(f"새로 올라온 공지가 없습니다.\n{line}")
    else:
        await n_channel.send('#####[일반소식]#####')
        for n_info in information:
            await n_channel.send(
                f"{line}\n[제목] : {n_info['title']}\n[날짜] : {n_info['date']}\n[링크] : {n_info['link']}\n")

        await n_channel.send(line)
