import requests
import info
from bs4 import BeautifulSoup

URL = "https://computer.cnu.ac.kr/computer/notice/project.do"
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
            link = URL+t.find('a')['href']

            data.append({'index': num, 'title': title, 'date': date, 'link': link})

    return data


async def send(message):
    p_channel = message.channel
    information = recent_info()
    if len(information) == 0:
        await p_channel.send(f'▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒[사업단소식]▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n{line}')
        await p_channel.send(f"새로 올라온 공지가 없습니다.\n{line}")
    else:
        await p_channel.send('#####[사업단소식]#####')
        for p_info in information:
            await p_channel.send(
                f"{line}\n[제목] : {p_info['title']}\n[날짜] : {p_info['date']}\n[링크] : {p_info['link']}\n")
        await p_channel.send(line)
