import requests
import info
from bs4 import BeautifulSoup

URL = "https://computer.cnu.ac.kr/computer/notice/cse.do"
line = "---------------------------------------------------------------------------------------------------"
end_line = "--------------------------------------------done!-------------------------------------------------"


def recent_info():
    last_update = info.get_last_update()

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
    c_channel = message.channel
    information = recent_info()
    if len(information) == 0:
        await c_channel.send(f':thumbsup:\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒[우리학부 News]▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n{line}')
        await c_channel.send(f"새로 올라온 공지가 없습니다.\n{end_line}")
    else:
        await c_channel.send(':pinching_hand: :eyes: :ok_hand: \n▒▒▒▒▒▒▒▒▒▒▒▒▒▒[우리학부 News]▒▒▒▒▒▒▒▒▒▒▒▒▒▒')
        for c_info in information:
            await c_channel.send(
                f"{line}\n[제목] : {c_info['title']}\n[날짜] : {c_info['date']}\n[링크] : {c_info['link']}\n")
        await c_channel.send(end_line)
