import requests
import info
from bs4 import BeautifulSoup

URL = "https://computer.cnu.ac.kr/computer/notice/job.do"
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
    j_channel = message.channel
    information = recent_info()
    if len(information) == 0:
        await j_channel.send(f'▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒[취업정보]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n{line}')
        await j_channel.send(f"새로 올라온 공지가 없습니다.\n{line}")
    else:
        await j_channel.send('#####[취업정보]#####')
        for j_info in information:
            await j_channel.send(
                f"{line}\n[제목] : {j_info['title']}\n[날짜] : {j_info['date']}\n[링크] : {j_info['link']}\n")
        await j_channel.send(line)
