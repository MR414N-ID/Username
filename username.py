#!/usr/bin/env python3
"""Cari username di ~200 situs.
Pakai : python username.py   (Termux: pkg install python && pip install requests)
Butuh : pip install requests
BY. MR414N-ID
"""
import sys
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Format per baris: nama  pola-url   ({u} = username)
SITES_TEXT = """
tiktok https://www.tiktok.com/@{u}
instagram https://www.instagram.com/{u}/
x https://x.com/{u}
facebook https://www.facebook.com/{u}
threads https://www.threads.net/@{u}
snapchat https://www.snapchat.com/add/{u}
pinterest https://www.pinterest.com/{u}/
reddit https://www.reddit.com/user/{u}
tumblr https://{u}.tumblr.com
linkedin https://www.linkedin.com/in/{u}
vk https://vk.com/{u}
telegram https://t.me/{u}
mastodon https://mastodon.social/@{u}
bluesky https://bsky.app/profile/{u}.bsky.social
quora https://www.quora.com/profile/{u}
flickr https://www.flickr.com/people/{u}
myspace https://myspace.com/{u}
okru https://ok.ru/{u}
livejournal https://{u}.livejournal.com
medium https://medium.com/@{u}
substack https://{u}.substack.com
wordpress https://{u}.wordpress.com
blogspot https://{u}.blogspot.com
aboutme https://about.me/{u}
linktree https://linktr.ee/{u}
carrd https://{u}.carrd.co
biolink https://bio.link/{u}
beacons https://beacons.ai/{u}
kofi https://ko-fi.com/{u}
patreon https://www.patreon.com/{u}
buymeacoffee https://www.buymeacoffee.com/{u}
gumroad https://{u}.gumroad.com
github https://github.com/{u}
gitlab https://gitlab.com/{u}
bitbucket https://bitbucket.org/{u}/
codepen https://codepen.io/{u}
replit https://replit.com/@{u}
hackerone https://hackerone.com/{u}
devto https://dev.to/{u}
hashnode https://hashnode.com/@{u}
npm https://www.npmjs.com/~{u}
pypi https://pypi.org/user/{u}/
dockerhub https://hub.docker.com/u/{u}
kaggle https://www.kaggle.com/{u}
leetcode https://leetcode.com/{u}/
codeforces https://codeforces.com/profile/{u}
hackerrank https://www.hackerrank.com/{u}
codewars https://www.codewars.com/users/{u}
sourceforge https://sourceforge.net/u/{u}/profile
gitee https://gitee.com/{u}
glitch https://glitch.com/@{u}
observable https://observablehq.com/@{u}
huggingface https://huggingface.co/{u}
launchpad https://launchpad.net/~{u}
wikipedia https://en.wikipedia.org/wiki/User:{u}
roblox https://www.roblox.com/user.aspx?username={u}
steam https://steamcommunity.com/id/{u}
twitch https://www.twitch.tv/{u}
chesscom https://www.chess.com/member/{u}
lichess https://lichess.org/@/{u}
namemc https://namemc.com/profile/{u}
itchio https://{u}.itch.io
gamejolt https://gamejolt.com/@{u}
speedrun https://www.speedrun.com/users/{u}
osu https://osu.ppy.sh/users/{u}
newgrounds https://{u}.newgrounds.com
kongregate https://www.kongregate.com/accounts/{u}
trakt https://trakt.tv/users/{u}
myanimelist https://myanimelist.net/profile/{u}
anilist https://anilist.co/user/{u}
kitsu https://kitsu.io/users/{u}
gog https://www.gog.com/u/{u}
planetminecraft https://www.planetminecraft.com/member/{u}/
bandcamp https://{u}.bandcamp.com
soundcloud https://soundcloud.com/{u}
spotify https://open.spotify.com/user/{u}
lastfm https://www.last.fm/user/{u}
mixcloud https://www.mixcloud.com/{u}/
reverbnation https://www.reverbnation.com/{u}
audiomack https://audiomack.com/{u}
genius https://genius.com/{u}
discogs https://www.discogs.com/user/{u}
smule https://www.smule.com/{u}
youtube https://www.youtube.com/@{u}
vimeo https://vimeo.com/{u}
dailymotion https://www.dailymotion.com/{u}
rumble https://rumble.com/user/{u}
odysee https://odysee.com/@{u}
kick https://kick.com/{u}
deviantart https://www.deviantart.com/{u}
behance https://www.behance.net/{u}
dribbble https://dribbble.com/{u}
artstation https://www.artstation.com/{u}
500px https://500px.com/p/{u}
unsplash https://unsplash.com/@{u}
pexels https://www.pexels.com/@{u}
pixabay https://pixabay.com/users/{u}/
imgur https://imgur.com/user/{u}
giphy https://giphy.com/{u}
fiverr https://www.fiverr.com/{u}
freelancer https://www.freelancer.com/u/{u}
99designs https://99designs.com/profiles/{u}
wattpad https://www.wattpad.com/user/{u}
ao3 https://archiveofourown.org/users/{u}
fanfiction https://www.fanfiction.net/~{u}
letterboxd https://letterboxd.com/{u}/
ebay https://www.ebay.com/usr/{u}
etsy https://www.etsy.com/shop/{u}
poshmark https://poshmark.com/closet/{u}
depop https://www.depop.com/{u}/
tokopedia https://www.tokopedia.com/{u}
shopee https://shopee.co.id/{u}
bukalapak https://www.bukalapak.com/u/{u}
kaskus https://www.kaskus.co.id/@{u}
kompasiana https://www.kompasiana.com/{u}
trakteer https://trakteer.id/{u}
saweria https://saweria.co/{u}
sociabuzz https://sociabuzz.com/{u}
likee https://likee.video/@{u}
hackernews https://news.ycombinator.com/user?id={u}
producthunt https://www.producthunt.com/@{u}
disqus https://disqus.com/by/{u}/
gravatar https://gravatar.com/{u}
keybase https://keybase.io/{u}
pastebin https://pastebin.com/u/{u}
slideshare https://www.slideshare.net/{u}
scribd https://www.scribd.com/{u}
issuu https://issuu.com/{u}
instructables https://www.instructables.com/member/{u}/
hackaday https://hackaday.io/{u}
thingiverse https://www.thingiverse.com/{u}
sketchfab https://sketchfab.com/{u}
printables https://www.printables.com/@{u}
grailed https://www.grailed.com/{u}
steamgifts https://www.steamgifts.com/user/{u}
clubhouse https://www.clubhouse.com/@{u}
fandom https://community.fandom.com/wiki/User:{u}
foursquare https://foursquare.com/{u}
duolingo https://www.duolingo.com/profile/{u}
codecademy https://www.codecademy.com/profiles/{u}
freecodecamp https://www.freecodecamp.org/{u}
tryhackme https://tryhackme.com/p/{u}
rootme https://www.root-me.org/{u}
vsco https://vsco.co/{u}
ifunny https://ifunny.co/user/{u}
9gag https://9gag.com/u/{u}
wykop https://www.wykop.pl/ludzie/{u}
pikabu https://pikabu.ru/@{u}
habr https://habr.com/en/users/{u}/
nairaland https://www.nairaland.com/{u}
hubpages https://hubpages.com/@{u}
askfm https://ask.fm/{u}
curiouscat https://curiouscat.live/{u}
tellonym https://tellonym.me/{u}
stocktwits https://stocktwits.com/{u}
tradingview https://www.tradingview.com/u/{u}/
opensea https://opensea.io/{u}
hackerearth https://www.hackerearth.com/@{u}
topcoder https://www.topcoder.com/members/{u}
exercism https://exercism.org/profiles/{u}
codechef https://www.codechef.com/users/{u}
atcoder https://atcoder.jp/users/{u}
spoj https://www.spoj.com/users/{u}/
devpost https://devpost.com/{u}
figma https://www.figma.com/@{u}
indiehackers https://www.indiehackers.com/{u}
wellfound https://wellfound.com/u/{u}
flipboard https://flipboard.com/@{u}
scratch https://scratch.mit.edu/users/{u}/
trello https://trello.com/{u}
myfitnesspal https://www.myfitnesspal.com/profile/{u}
alltrails https://www.alltrails.com/members/{u}
tinder https://tinder.com/@{u}
smugmug https://{u}.smugmug.com
xing https://www.xing.com/profile/{u}
gettr https://gettr.com/user/{u}
truthsocial https://truthsocial.com/@{u}
minds https://www.minds.com/{u}
gab https://gab.com/{u}
mewe https://mewe.com/i/{u}
musescore https://musescore.com/{u}
bandlab https://www.bandlab.com/{u}
younow https://www.younow.com/{u}
ravelry https://www.ravelry.com/people/{u}
cults3d https://cults3d.com/en/users/{u}
myminifactory https://www.myminifactory.com/users/{u}
boardgamegeek https://boardgamegeek.com/user/{u}
geocaching https://www.geocaching.com/p/?u={u}
wordnik https://www.wordnik.com/users/{u}
coroflot https://www.coroflot.com/{u}
contently https://{u}.contently.com
muckrack https://muckrack.com/{u}
qiita https://qiita.com/{u}
zenn https://zenn.dev/{u}
note https://note.com/{u}
ameblo https://ameblo.jp/{u}
velog https://velog.io/@{u}
tistory https://{u}.tistory.com
csdn https://blog.csdn.net/{u}
lobsters https://lobste.rs/u/{u}
slashdot https://slashdot.org/~{u}
arduino https://forum.arduino.cc/u/{u}
"""

# Teks di halaman yang berarti akun TIDAK ada (untuk situs yang selalu balas 200)
NOT_FOUND = {
    "tiktok": ["Couldn't find this account", "couldn\\u2019t find this account"],
    "instagram": ["Page Not Found", "isn't available"],
    "x": ["This account doesn", "doesn\\u2019t exist"],
    "facebook": ["This content isn't available", "Page Not Found"],
    "reddit": ["Sorry, nobody on Reddit goes by that name", "page not found"],
    "twitch": ["Sorry. Unless you've got a time machine"],
    "telegram": ["tgme_page_extra\"></div>"],
    "roblox": ["Page cannot be found", "Page not found"],
    "linktree": ["The page you\u2019re looking for doesn", "doesn't exist"],
}
GENERIC_NOT_FOUND = [
    "page not found", "user not found", "profile not found", "account not found",
    "doesn't exist", "does not exist", "no such user", "couldn't find",
    "halaman tidak ditemukan", "pengguna tidak ditemukan",
]


def parse_sites():
    sites = {}
    for line in SITES_TEXT.strip().splitlines():
        nama, url = line.split(maxsplit=1)
        sites[nama] = url.strip()
    return sites


def build_link(pola, username):
    # Username dengan "_" tidak valid sebagai subdomain
    if pola.startswith("https://{u}."):
        username = username.replace("_", "-")
    return pola.format(u=username)


def ada_akun(nama, pola, username):
    link = build_link(pola, username)
    try:
        r = requests.get(link, headers=HEADERS, timeout=10, allow_redirects=True)
    except requests.RequestException:
        return False, link
    if r.status_code != 200:
        return False, link
    # Redirect ke beranda = akun tidak ada
    if r.url.rstrip("/").count("/") <= 2 and not link.rstrip("/").endswith(r.url.rstrip("/").split("/")[-1]):
        return False, link
    body = r.text[:60000].lower()
    for teks in NOT_FOUND.get(nama, []) + GENERIC_NOT_FOUND:
        if teks.lower() in body:
            return False, link
    return True, link


def cek_situs(nama, pola, username):
    ada, link = ada_akun(nama, pola, username)
    if not ada:
        return nama, link, False
    # Kontrol: username acak. Kalau ini juga "ada", situs tidak bisa dipercaya.
    acak = "zq" + "".join(random.choices(string.ascii_lowercase + string.digits, k=14))
    ada_acak, _ = ada_akun(nama, pola, acak)
    return nama, link, not ada_acak


import os
import time
import shutil

C = {
    "r": "\033[91m", "g": "\033[92m", "y": "\033[93m", "b": "\033[94m",
    "m": "\033[95m", "c": "\033[96m", "w": "\033[97m", "d": "\033[90m",
    "x": "\033[0m", "B": "\033[1m",
}

FONT = {
    "M": ["#   #", "## ##", "# # #", "#   #", "#   #"],
    "R": ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    "4": ["#  # ", "#  # ", "#####", "   # ", "   # "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", " ### "],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    "-": ["     ", "     ", " ### ", "     ", "     "],
    "I": ["###", " # ", " # ", " # ", "###"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#### "],
}

TUX = [
    "      .--.      ",
    "     |o_o |     ",
    "     |:_/ |     ",
    "    //   \\ \\    ",
    "   (|     | )   ",
    "  /'\\_   _/`\\   ",
    "  \\___)=(___/   ",
]


def blok(teks):
    baris = [""] * 5
    for ch in teks:
        for i in range(5):
            baris[i] += FONT[ch][i].replace("#", "█") + " "
    return baris


def banner():
    os.system("clear")
    cols = shutil.get_terminal_size((50, 20)).columns
    print()
    for line in TUX:
        print(C["y"] + C["B"] + line.center(cols) + C["x"])
        time.sleep(0.05)
    print()
    teks = ["MR414N-ID"]
    if sum(len(FONT[c][0]) + 1 for c in teks[0]) > cols:
        teks = ["MR414N", "-ID"]
    warna = ["r", "y", "g", "c", "m"]
    for t in teks:
        for i, row in enumerate(blok(t)):
            print(C[warna[i % len(warna)]] + C["B"] + row.center(cols) + C["x"])
            time.sleep(0.05)
    print()
    print(C["c"] + C["B"] + "BY. MR414N-ID".center(cols) + C["x"])
    print(C["d"] + "Username Finder  •  200+ situs".center(cols) + C["x"])
    print(C["d"] + ("─" * min(cols, 44)).center(cols) + C["x"])
    print()


def cari(username):
    sites = parse_sites()
    sukses = []
    print(C["y"] + f"[*] Mencari '{username}' di {len(sites)} situs...\n" + C["x"])

    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = [ex.submit(cek_situs, n, p, username) for n, p in sites.items()]
        for f in as_completed(futures):
            nama, link, ada = f.result()
            if ada:
                print(f"{C['g']}[sukses]{C['x']} {nama}: {link}", flush=True)
                sukses.append(f"{nama}: {link}")
            else:
                print(f"{C['r']}[gagal]{C['x']} {nama}", flush=True)

    print(f"\n{C['c']}Selesai: {len(sukses)} ditemukan dari {len(sites)} situs.{C['x']}")
    if sukses:
        with open(f"hasil_{username}.txt", "w", encoding="utf-8") as fh:
            fh.write("\n".join(sukses))
        print(f"{C['g']}Link tersimpan di hasil_{username}.txt{C['x']}")


def main():
    banner()
    username = sys.argv[1].strip().lstrip("@") if len(sys.argv) > 1 else None
    while True:
        if username is None:
            try:
                username = input(f"{C['g']}[?] Masukkan username {C['w']}>> {C['x']}").strip().lstrip("@")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not username:
                break
        cari(username)
        username = None
        try:
            lagi = input(f"\n{C['y']}Cari lagi? (y/n) {C['w']}>> {C['x']}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if lagi != "y":
            break
        print()
    print(C["c"] + "\nTerima kasih!  —  BY. MR414N-ID" + C["x"])


if __name__ == "__main__":
    main()
