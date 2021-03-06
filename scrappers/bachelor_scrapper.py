import requests
import info
from bs4 import BeautifulSoup

URL = "https://computer.cnu.ac.kr/computer/notice/bachelor.do"
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
    b_channel = message.channel
    information = recent_info()
    if len(information) == 0:
        await b_channel.send(f':thumbsup:\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒[학사공지]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n{line}')
        await b_channel.send(f"새로 올라온 공지가 없습니다.\n{end_line}")
    else:
        await b_channel.send(':pinching_hand: :eyes: :ok_hand: \n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒[학사공지]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒')
        for b_info in information:
            await b_channel.send(
                f"{line}\n[제목] : {b_info['title']}\n[날짜] : {b_info['date']}\n[링크] : {b_info['link']}\n")
        await b_channel.send(end_line)

