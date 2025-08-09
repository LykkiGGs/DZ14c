from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/get-sum")
def get_sum():
    url = "https://www.leagueofgraphs.com/summoner/eune/Vertigo-3110#championsData-all"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to retrieve page, status code: {response.status_code}"}

    soup = BeautifulSoup(response.text, "html.parser")

    players = {
        "villain+arc-777": None,
        "hot+korean+ad-001": None  # example second player, change as needed
    }

    td_tags = soup.find_all("td", attrs={"data-sort-value": True})

    for td in td_tags:
        a_tag = td.find("a", href=True)
        if a_tag:
            href = a_tag['href'].lower()
            for player in players.keys():
                if player in href and players[player] is None:
                    try:
                        val = float(td["data-sort-value"])
                        if val >= 1 and val.is_integer():
                            players[player] = val
                    except ValueError:
                        pass

    if None in players.values():
        missing = [k for k, v in players.items() if v is None]
        return {"error": f"Could not find data for: {', '.join(missing)}"}

    total = sum(players.values())

    return {
        "villain_arc_777": int(players["villain+arc-777"]),
        "hot_korean_ad_001": int(players["hot_korean_ad_001"]),
        "sum": int(total)
    }
