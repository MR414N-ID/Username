#!/usr/bin/env python3
"""Username Finder - cari username di 500 situs, dari nama, atau massal (file txt / manual).
Pakai : python username.py                (menu interaktif)
        python username.py <username>     (langsung cek)
Termux: pkg install python && pip install requests
BY. MR414N-ID
"""
import sys
import os
import time
import random
import string
import shutil
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
fosstodon https://fosstodon.org/@{u}
mstdn https://mstdn.social/@{u}
mastodononline https://mastodon.online/@{u}
infosecexchange https://infosec.exchange/@{u}
hachyderm https://hachyderm.io/@{u}
techhub https://techhub.social/@{u}
mastoto https://mas.to/@{u}
mastodonworld https://mastodon.world/@{u}
universeodon https://universeodon.com/@{u}
sigmoid https://sigmoid.social/@{u}
pawoo https://pawoo.net/@{u}
misskeyio https://misskey.io/@{u}
chaossocial https://chaos.social/@{u}
tchncs https://social.tchncs.de/@{u}
floss https://floss.social/@{u}
techlgbt https://tech.lgbt/@{u}
vivaldisocial https://social.vivaldi.net/@{u}
octodon https://octodon.social/@{u}
mastodonart https://mastodon.art/@{u}
gamedevplace https://mastodon.gamedev.place/@{u}
rubysocial https://ruby.social/@{u}
phpcsocial https://phpc.social/@{u}
indieweb https://indieweb.social/@{u}
mathstodon https://mathstodon.xyz/@{u}
scholarsocial https://scholar.social/@{u}
journahost https://journa.host/@{u}
cim https://c.im/@{u}
tootcommunity https://toot.community/@{u}
nocsocial https://noc.social/@{u}
mastodoncloud https://mastodon.cloud/@{u}
socialcoop https://social.coop/@{u}
kolektiva https://kolektiva.social/@{u}
pixelfed https://pixelfed.social/{u}
lemmyworld https://lemmy.world/u/{u}
lemmyml https://lemmy.ml/u/{u}
beehaw https://beehaw.org/u/{u}
itjustworks https://sh.itjust.works/u/{u}
lemmee https://lemm.ee/u/{u}
programmingdev https://programming.dev/u/{u}
feddit https://feddit.de/u/{u}
lemmyca https://lemmy.ca/u/{u}
slrpnk https://slrpnk.net/u/{u}
tildes https://tildes.net/user/{u}
codeberg https://codeberg.org/{u}
gitea https://gitea.com/{u}
sourcehut https://sr.ht/~{u}/
cratesio https://crates.io/users/{u}
rubygems https://rubygems.org/profiles/{u}
packagist https://packagist.org/users/{u}/
nuget https://www.nuget.org/profiles/{u}
metacpan https://metacpan.org/author/{u}
jsfiddle https://jsfiddle.net/user/{u}/
stackblitz https://stackblitz.com/@{u}
codesandbox https://codesandbox.io/u/{u}
githubgist https://gist.github.com/{u}
anaconda https://anaconda.org/{u}
githubio https://{u}.github.io
gitlabio https://{u}.gitlab.io
netlify https://{u}.netlify.app
vercel https://{u}.vercel.app
cloudflarepages https://{u}.pages.dev
herokuapp https://{u}.herokuapp.com
surge https://{u}.surge.sh
webflow https://{u}.webflow.io
hackmd https://hackmd.io/@{u}
codeproject https://www.codeproject.com/Members/{u}
leanpub https://leanpub.com/u/{u}
hackster https://www.hackster.io/{u}
tinkercad https://www.tinkercad.com/users/{u}
gamedevnet https://www.gamedev.net/{u}/
hackernoon https://hackernoon.com/u/{u}
dicoding https://www.dicoding.com/users/{u}
datacamp https://www.datacamp.com/portfolio/{u}
geeksforgeeks https://auth.geeksforgeeks.org/user/{u}
leetcodecn https://leetcode.cn/u/{u}/
kattis https://open.kattis.com/users/{u}
dmoj https://dmoj.ca/user/{u}
toph https://toph.co/p/{u}
vjudge https://vjudge.net/user/{u}
bugcrowd https://bugcrowd.com/{u}
intigriti https://app.intigriti.com/profile/{u}
yeswehack https://yeswehack.com/hunters/{u}
v2ex https://www.v2ex.com/member/{u}
discoursemeta https://meta.discourse.org/u/{u}
discusspython https://discuss.python.org/u/{u}
cloudflarecommunity https://community.cloudflare.com/u/{u}
freecodecampforum https://forum.freecodecamp.org/u/{u}
mozillaforum https://discourse.mozilla.org/u/{u}
rustusers https://users.rust-lang.org/u/{u}
pytorchforum https://discuss.pytorch.org/u/{u}
openaicommunity https://community.openai.com/u/{u}
obsidianforum https://forum.obsidian.md/u/{u}
homeassistant https://community.home-assistant.io/u/{u}
kotlinforum https://discuss.kotlinlang.org/u/{u}
hashicorpforum https://discuss.hashicorp.com/u/{u}
gitlabforum https://forum.gitlab.com/u/{u}
letsencrypt https://community.letsencrypt.org/u/{u}
elasticforum https://discuss.elastic.co/u/{u}
manjaroforum https://forum.manjaro.org/u/{u}
nixosdiscourse https://discourse.nixos.org/u/{u}
snapcraftforum https://forum.snapcraft.io/u/{u}
flyiocommunity https://community.fly.io/u/{u}
ansibleforum https://forum.ansible.com/u/{u}
julialang https://discourse.julialang.org/u/{u}
godotforum https://forum.godotengine.org/u/{u}
ionicforum https://forum.ionicframework.com/u/{u}
bubbleforum https://forum.bubble.io/u/{u}
n8ncommunity https://community.n8n.io/u/{u}
huggingfaceforum https://discuss.huggingface.co/u/{u}
streamlitforum https://discuss.streamlit.io/u/{u}
rcloneforum https://forum.rclone.org/u/{u}
openwrtforum https://forum.openwrt.org/u/{u}
weheartit https://weheartit.com/{u}
ello https://ello.co/{u}
writeas https://write.as/{u}/
microblog https://micro.blog/{u}
beehiiv https://{u}.beehiiv.com
buttondown https://buttondown.email/{u}
tinyletter https://tinyletter.com/{u}
bearblog https://{u}.bearblog.dev
weebly https://{u}.weebly.com
jimdo https://{u}.jimdofree.com
neocities https://{u}.neocities.org
nekoweb https://{u}.nekoweb.org
tildeclub https://tilde.club/~{u}/
dreamwidth https://{u}.dreamwidth.org
insanejournal https://{u}.insanejournal.com
typepad https://{u}.typepad.com
overblog https://{u}.over-blog.com
skyrock https://{u}.skyrock.com
bloggse https://{u}.blogg.se
wikidot https://{u}.wikidot.com
livedoor https://blog.livedoor.jp/{u}/
hatena https://profile.hatena.ne.jp/{u}/
hatenablog https://{u}.hatenablog.com
fc2blog https://{u}.blog.fc2.com
lofter https://{u}.lofter.com
cnblogs https://www.cnblogs.com/{u}/
douban https://www.douban.com/people/{u}/
zhihu https://www.zhihu.com/people/{u}
naverblog https://blog.naver.com/{u}
booth https://{u}.booth.pm
fanbox https://{u}.fanbox.cc
skeb https://skeb.jp/@{u}
dzen https://dzen.ru/{u}
mailru https://my.mail.ru/mail/{u}/
drive2 https://www.drive2.ru/users/{u}/
flru https://www.fl.ru/users/{u}/
kwork https://kwork.ru/user/{u}
authortoday https://author.today/u/{u}
proza https://proza.ru/avtor/{u}
stihi https://stihi.ru/avtor/{u}
livelib https://www.livelib.ru/reader/{u}
bitchute https://www.bitchute.com/channel/{u}/
brighteon https://www.brighteon.com/channels/{u}
locals https://{u}.locals.com
kumparan https://kumparan.com/{u}
karyakarsa https://karyakarsa.com/{u}
bagibagi https://bagibagi.co/{u}
tako https://tako.id/{u}
goodreads https://www.goodreads.com/{u}
librarything https://www.librarything.com/profile/{u}
storygraph https://app.thestorygraph.com/profile/{u}
inkitt https://www.inkitt.com/{u}
tapas https://tapas.io/{u}
comicvine https://comicvine.gamespot.com/profile/{u}/
tmdb https://www.themoviedb.org/u/{u}
mydramalist https://mydramalist.com/profile/{u}
animeplanet https://www.anime-planet.com/users/{u}
shikimori https://shikimori.one/{u}
metacritic https://www.metacritic.com/user/{u}/
giantbomb https://www.giantbomb.com/profile/{u}/
gamefaqs https://gamefaqs.gamespot.com/community/{u}
backloggd https://www.backloggd.com/u/{u}/
exophase https://www.exophase.com/user/{u}/
psnprofiles https://psnprofiles.com/{u}
faceit https://www.faceit.com/en/players/{u}
rateyourmusic https://rateyourmusic.com/~{u}
modrinth https://modrinth.com/user/{u}
curseforge https://www.curseforge.com/members/{u}/projects
moddb https://www.moddb.com/members/{u}
indiedb https://www.indiedb.com/members/{u}
minecraftforum https://www.minecraftforum.net/members/{u}
moxfield https://www.moxfield.com/users/{u}
archidekt https://archidekt.com/u/{u}
deckbox https://deckbox.org/users/{u}
pokemonshowdown https://pokemonshowdown.com/users/{u}
humblebundle https://www.humblebundle.com/user/{u}
trovo https://trovo.live/s/{u}
dlive https://dlive.tv/{u}
bigo https://www.bigo.tv/user/{u}
picarto https://picarto.tv/{u}
mobcrush https://www.mobcrush.com/{u}
glimesh https://glimesh.tv/{u}
vkplay https://live.vkplay.ru/{u}
afreecatv https://bj.afreecatv.com/{u}
audius https://audius.co/{u}
hearthis https://hearthis.at/{u}/
musicbrainz https://musicbrainz.org/user/{u}
setlistfm https://www.setlist.fm/user/{u}
listenbrainz https://listenbrainz.org/user/{u}/
ultimateguitar https://www.ultimate-guitar.com/u/{u}
8tracks https://8tracks.com/{u}
audiotool https://www.audiotool.com/user/{u}/
flatio https://flat.io/{u}
imgbb https://{u}.imgbb.com
tenor https://tenor.com/users/{u}
zenfolio https://{u}.zenfolio.com
viewbug https://www.viewbug.com/member/{u}
pixieset https://{u}.pixieset.com
exposure https://{u}.exposure.co
awwwards https://www.awwwards.com/{u}/
carbonmade https://{u}.carbonmade.com
cargo https://{u}.cargo.site
adobeportfolio https://{u}.myportfolio.com
tilda https://{u}.tilda.ws
strikingly https://{u}.mystrikingly.com
polycount https://polycount.com/profile/{u}
grabcad https://grabcad.com/{u}
cgtrader https://www.cgtrader.com/{u}
freepik https://www.freepik.com/author/{u}
flaticon https://www.flaticon.com/authors/{u}
iconfinder https://www.iconfinder.com/{u}
nounproject https://thenounproject.com/{u}/
canva https://www.canva.com/{u}
speakerdeck https://speakerdeck.com/{u}
yumpu https://www.yumpu.com/user/{u}
houzz https://www.houzz.com/user/{u}
envato https://themeforest.net/user/{u}
codecanyon https://codecanyon.net/user/{u}
audiojungle https://audiojungle.net/user/{u}
videohive https://videohive.net/user/{u}
graphicriver https://graphicriver.net/user/{u}
creativemarket https://creativemarket.com/{u}
redbubble https://www.redbubble.com/people/{u}
society6 https://society6.com/{u}
zazzle https://www.zazzle.com/mbr/{u}
teepublic https://www.teepublic.com/user/{u}
threadless https://{u}.threadless.com
dreamstime https://www.dreamstime.com/{u}_info
cameo https://www.cameo.com/{u}
throne https://throne.com/{u}
subscribestar https://www.subscribestar.com/{u}
liberapay https://liberapay.com/{u}
opencollective https://opencollective.com/{u}
githubsponsors https://github.com/sponsors/{u}
paypalme https://www.paypal.me/{u}
cashapp https://cash.app/${u}
venmo https://venmo.com/{u}
payhip https://payhip.com/{u}
sellfy https://sellfy.com/{u}
storenvy https://{u}.storenvy.com
bigcartel https://{u}.bigcartel.com
bonanza https://www.bonanza.com/booths/{u}
reverb https://reverb.com/shop/{u}
carousell https://id.carousell.com/u/{u}/
skillshare https://www.skillshare.com/en/profile/{u}
kickstarter https://www.kickstarter.com/profile/{u}
kiva https://www.kiva.org/lender/{u}
flavorsme https://flavors.me/{u}
lnkbio https://lnk.bio/{u}
campsitebio https://campsite.bio/{u}
soloto https://solo.to/{u}
allmylinks https://allmylinks.com/{u}
taplink https://taplink.cc/{u}
hoobe https://hoo.be/{u}
withkoji https://withkoji.com/@{u}
directme https://direct.me/{u}
tapbio https://tap.bio/@{u}
stanstore https://stan.store/{u}
linkpop https://linkpop.com/{u}
litlink https://lit.link/{u}
potofu https://potofu.me/{u}
crunchbase https://www.crunchbase.com/person/{u}
f6s https://www.f6s.com/{u}
steemit https://steemit.com/@{u}
peakd https://peakd.com/@{u}
warpcast https://warpcast.com/{u}
rarible https://rarible.com/{u}
foundation https://foundation.app/@{u}
superrare https://superrare.com/{u}
coinmarketcap https://coinmarketcap.com/community/profile/{u}/
etoro https://www.etoro.com/people/{u}
couchsurfing https://www.couchsurfing.com/people/{u}
memrise https://community.memrise.com/user/{u}/
quizlet https://quizlet.com/{u}
brilliant https://brilliant.org/profile/{u}/
tripadvisor https://www.tripadvisor.com/Profile/{u}
untappd https://untappd.com/user/{u}
beeradvocate https://www.beeradvocate.com/community/members/{u}
wikimediacommons https://commons.wikimedia.org/wiki/User:{u}
wikidata https://www.wikidata.org/wiki/User:{u}
archiveorg https://archive.org/details/@{u}
openstreetmap https://www.openstreetmap.org/user/{u}
mapillary https://www.mapillary.com/app/user/{u}
wikiloc https://www.wikiloc.com/wikiloc/user.do?name={u}
wikibooks https://en.wikibooks.org/wiki/User:{u}
wikiquote https://en.wikiquote.org/wiki/User:{u}
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

# ===== FITUR BARU: pencarian dari nama + filter daerah =====
PRIORITY_SITES = [
    "instagram", "facebook", "tiktok", "x", "threads",
    "telegram", "github", "linkedin",
]

INDONESIAN_SITES = [
    "tokopedia", "shopee", "bukalapak", "kaskus", "kompasiana",
    "trakteer", "saweria", "sociabuzz",
]

REGION_ALIASES = {
    "bandung":    ["bandung", "bdg", "jabar"],
    "jakarta":    ["jakarta", "jkt", "dki"],
    "surabaya":   ["surabaya", "sby", "jatim"],
    "yogyakarta": ["yogyakarta", "jogja", "yogya", "jgj"],
    "semarang":   ["semarang", "smg"],
    "medan":      ["medan", "mdn"],
    "makassar":   ["makassar", "mks", "ujungpandang"],
    "palembang":  ["palembang", "plg"],
    "denpasar":   ["denpasar", "bali", "dps"],
    "malang":     ["malang", "mlg"],
    "solo":       ["solo", "surakarta", "skt"],
    "bogor":      ["bogor", "bgr"],
    "depok":      ["depok", "dpk"],
    "tangerang":  ["tangerang", "tgr"],
    "bekasi":     ["bekasi", "bks"],
}


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
    print(C["d"] + f"Username Finder  •  {len(parse_sites())} situs".center(cols) + C["x"])
    print(C["d"] + ("─" * min(cols, 44)).center(cols) + C["x"])
    print()


SHOW_GAGAL = False   # True = tampilkan juga baris [gagal] satu per satu


def cari(username, simpan=True, koleksi=None):
    """Mode lama: cari username di 500 situs. Return jumlah situs sukses.
    simpan=False -> tidak menulis file (dipakai mode massal, simpan ditanya di akhir).
    koleksi (dict) -> kalau diisi, hasil [(situs, link), ...] dicatat di koleksi[username].
    """
    sites = parse_sites()
    total = len(sites)
    sukses = []
    selesai = 0
    cols = shutil.get_terminal_size((50, 20)).columns
    print(C["y"] + f"[*] Mencari '{username}' di {total} situs...\n" + C["x"])

    def progres():
        print(f"\r{C['d']}[{selesai}/{total}] sedang dicek...{C['x']}", end="", flush=True)

    with ThreadPoolExecutor(max_workers=40) as ex:
        futures = {ex.submit(cek_situs, n, p, username): n for n, p in sites.items()}
        try:
            for f in as_completed(futures):
                selesai += 1
                try:
                    nama, link, ada = f.result()
                except Exception:
                    nama, link, ada = futures[f], "", False
                if ada:
                    print(f"\r\033[K{C['g']}[sukses]{C['x']} {nama}: {link}", flush=True)
                    sukses.append((nama, link))
                elif SHOW_GAGAL:
                    print(f"\r\033[K{C['r']}[gagal]{C['x']} {nama}", flush=True)
                progres()
        except KeyboardInterrupt:
            for fu in futures:
                fu.cancel()
            raise

    sukses.sort(key=lambda x: x[0])
    garis = "=" * min(cols, 44)
    print("\r\033[K", end="")
    print(f"\n{C['c']}{garis}{C['x']}")
    print(f"{C['g']}{C['B']}Searching selesai sukses [ {len(sukses)} situs ]{C['x']}")
    print(f"{C['d']}(dari {total} situs yang dicek){C['x']}")
    print(f"{C['c']}{garis}{C['x']}")
    if sukses:
        for nama, link in sukses:
            print(f"{C['y']}{nama}{C['x']} : {link}")
        print(f"{C['c']}{garis}{C['x']}")
        if simpan:
            with open(f"hasil_{username}.txt", "w", encoding="utf-8") as fh:
                fh.write(f"Searching selesai sukses [ {len(sukses)} situs ]\n")
                fh.write("\n".join(f"{n} : {l}" for n, l in sukses) + "\n")
            print(f"{C['g']}Tersimpan di hasil_{username}.txt{C['x']}")
    else:
        print(f"{C['r']}Tidak ada akun ditemukan.{C['x']}")
    if koleksi is not None:
        koleksi[username] = list(sukses)
    return len(sukses)


# ===== FUNGSI BARU =====

def normalize_name(nama):
    """Bersihkan nama untuk generation kandidat."""
    nama = nama.lower().strip()
    for ch in [",", ".", "-", "_"]:
        nama = nama.replace(ch, " ")
    return [p for p in nama.split() if p and len(p) > 1]


def generate_candidates(nama, max_candidates=40):
    """Generate kandidat username dari nama."""
    parts = normalize_name(nama)
    if not parts:
        return []
    candidates = set()
    if len(parts) == 1:
        base = parts[0]
        candidates.update([
            base, f"{base}1", f"{base}01", f"{base}88", f"{base}99",
            f"{base}.id", f"{base}_id", f"_{base}", f"{base}_",
            f"the{base}", f"real{base}",
        ])
    else:
        first, last = parts[0], parts[-1]
        joined = "".join(parts)
        candidates.add(joined)
        candidates.add(f"{first}{last}")
        candidates.add(f"{last}{first}")
        candidates.add(f"{first}.{last}")
        candidates.add(f"{first}_{last}")
        candidates.add(f"{first}-{last}")
        candidates.add(f"{first[:3]}{last}")
        candidates.add(f"{first}{last[:3]}")
        candidates.add(f"{first[0]}{last}")
        if len(parts) > 2:
            mid = "".join(parts[1:-1])
            candidates.add(f"{first}{mid}{last}")
        for n in ["01", "88", "99", "123", "1"]:
            candidates.add(f"{joined}{n}")
            candidates.add(f"{first}{last}{n}")
        for p in ["the", "real", "mr"]:
            candidates.add(f"{p}{joined}")
        candidates.add(f"{joined}.id")
        candidates.add(f"{joined}_id")
        candidates.add(f"{joined}official")
    return list(candidates)[:max_candidates]


def region_in_username(username, region):
    if not region:
        return False
    region_lower = region.lower().strip()
    aliases = REGION_ALIASES.get(region_lower, [region_lower])
    ul = username.lower()
    return any(a in ul for a in aliases)


def check_candidate_on_sites(candidate, sites_subset, max_workers=15):
    """Cek 1 kandidat ke subset situs. Return [(site_name, link), ...]."""
    found = []

    def _check(item):
        name, pattern = item
        ada, link = ada_akun(name, pattern, candidate)
        return name, link, ada

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_check, item): item for item in sites_subset.items()}
        for f in as_completed(futures):
            try:
                name, link, ada = f.result()
                if ada:
                    found.append((name, link))
            except Exception:
                pass
    return found


def cari_dari_nama(nama, region):
    """Mode 2: cari username dari nama + filter daerah, lalu pilih manual."""
    sites = parse_sites()
    candidates = generate_candidates(nama)
    if not candidates:
        print(f"{C['r']}Nama tidak valid.{C['x']}")
        return

    print(f"\n{C['y']}[*] Nama       : {nama}{C['x']}")
    print(f"{C['y']}[*] Daerah     : {region or '(tidak difilter)'}{C['x']}")
    print(f"{C['y']}[*] Kandidat   : {len(candidates)} variasi username{C['x']}")
    situs_info = f"{len(PRIORITY_SITES)} prioritas"
    if region:
        situs_info += f" + {len(INDONESIAN_SITES)} lokal"
    print(f"{C['y']}[*] Situs cek  : {situs_info}\n")

    priority_patterns = {n: sites[n] for n in PRIORITY_SITES if n in sites}
    indo_patterns = {n: sites[n] for n in INDONESIAN_SITES if n in sites} if region else {}

    found = {}

    for i, cand in enumerate(candidates, 1):
        print(f"\r{C['d']}[{i}/{len(candidates)}] cek: {cand}...{C['x']}   ", end="", flush=True)
        social = check_candidate_on_sites(cand, priority_patterns)
        if social:
            found[cand] = {
                "sites": social,
                "region_match": region_in_username(cand, region),
                "indonesian": False,
            }
            print(f"\r\033[K{C['g']}[+] {cand} → {', '.join(s[0] for s in social)}{C['x']}")

    print("\r\033[K", end="")

    if not found:
        print(f"{C['r']}Tidak ada kandidat ditemukan di situs prioritas.{C['x']}")
        return

    if region and indo_patterns:
        print(f"\n{C['y']}[*] Cek sinyal daerah di {len(indo_patterns)} situs lokal Indonesia...{C['x']}")
        for cand in list(found.keys()):
            indo = check_candidate_on_sites(cand, indo_patterns, max_workers=8)
            if indo:
                found[cand]["sites"].extend(indo)
                found[cand]["indonesian"] = True

    def skor(item):
        _, info = item
        s = len(info["sites"])
        if info["region_match"]:
            s += 10
        if info["indonesian"]:
            s += 5
        return -s

    sorted_found = sorted(found.items(), key=skor)

    cols = shutil.get_terminal_size((50, 20)).columns
    garis = "=" * min(cols, 44)
    print(f"\n{C['c']}{garis}{C['x']}")
    print(f"{C['g']}{C['B']}KANDIDAT DITEMUKAN [ {len(sorted_found)} username ]{C['x']}")
    if region:
        print(f"{C['d']}Filter daerah: {region}{C['x']}")
    print(f"{C['c']}{garis}{C['x']}")

    for i, (cand, info) in enumerate(sorted_found, 1):
        tags = []
        if info["region_match"]:
            tags.append(f"{C['g']}[daerah✓]{C['x']}")
        if info["indonesian"]:
            tags.append(f"{C['c']}[indo✓]{C['x']}")
        sites_str = ", ".join(s[0] for s in info["sites"][:4])
        print(f"{C['y']}{i:2}.{C['x']} {C['w']}{cand:<22}{C['x']} {C['d']}({sites_str}){C['x']} {' '.join(tags)}")

    print(f"{C['c']}{garis}{C['x']}")

    try:
        choice = input(f"\n{C['y']}Pilih nomor untuk cek 500 situs (contoh: 1,2,3 / all / skip) >> {C['x']}").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return

    if not choice or choice == "skip":
        return

    if choice == "all":
        selected = [c for c, _ in sorted_found]
    else:
        indices = []
        for part in choice.replace(",", " ").split():
            try:
                idx = int(part) - 1
                if 0 <= idx < len(sorted_found):
                    indices.append(idx)
            except ValueError:
                pass
        selected = [sorted_found[i][0] for i in indices]

    if not selected:
        print(f"{C['r']}Tidak ada yang dipilih.{C['x']}")
        return

    for cand in selected:
        print()
        cari(cand)

    if len(selected) > 1:
        fname = f"hasil_nama_{nama.replace(' ', '_').lower()}.txt"
        with open(fname, "w", encoding="utf-8") as fh:
            fh.write(f"Pencarian nama: {nama}\n")
            if region:
                fh.write(f"Daerah: {region}\n")
            fh.write(f"\nKandidat terpilih: {', '.join(selected)}\n")
            fh.write("\nDetail per username ada di hasil_<username>.txt\n")
        print(f"\n{C['g']}Ringkasan disimpan di {fname}{C['x']}")


def cari_gabungan(nama, region):
    """Mode 3: nama -> kandidat -> auto cek 500 situs tiap kandidat."""
    sites = parse_sites()
    candidates = generate_candidates(nama)
    if not candidates:
        print(f"{C['r']}Nama tidak valid.{C['x']}")
        return

    print(f"\n{C['y']}[*] Nama       : {nama}{C['x']}")
    print(f"{C['y']}[*] Daerah     : {region or '(tidak difilter)'}{C['x']}")
    print(f"{C['y']}[*] Kandidat   : {len(candidates)} variasi username{C['x']}\n")

    priority_patterns = {n: sites[n] for n in PRIORITY_SITES if n in sites}

    # FASE 1: filter kandidat via situs prioritas
    found = []
    for i, cand in enumerate(candidates, 1):
        print(f"\r{C['d']}[{i}/{len(candidates)}] filter: {cand}...{C['x']}   ", end="", flush=True)
        social = check_candidate_on_sites(cand, priority_patterns)
        if social:
            found.append((cand, social))
            print(f"\r\033[K{C['g']}[+] {cand} → {', '.join(s[0] for s in social)}{C['x']}")
    print("\r\033[K", end="")

    if not found:
        print(f"{C['r']}Tidak ada kandidat ditemukan di situs prioritas.{C['x']}")
        return

    # FILTER DAERAH (kalau diisi)
    if region:
        filtered = [(c, s) for c, s in found if region_in_username(c, region)]
        if filtered:
            print(f"{C['y']}[*] Difilter ke {len(filtered)} kandidat dengan sinyal daerah '{region}'.{C['x']}")
            found = filtered
        else:
            print(f"{C['y']}[*] Tidak ada kandidat dengan sinyal '{region}', lanjut semua kandidat.{C['x']}")

    # FASE 2: cek 500 situs per username
    print(f"\n{C['c']}{'=' * 44}{C['x']}")
    print(f"{C['g']}{C['B']}CEK 500 SITUS UNTUK {len(found)} USERNAME{C['x']}")
    print(f"{C['c']}{'=' * 44}{C['x']}")

    hasil_akhir = []
    for idx, (cand, _) in enumerate(found, 1):
        # separator kuning
        print(f"\n{C['y']}{C['B']}{'=' * 44}{C['x']}")
        print(f"{C['y']}{C['B']}[{idx}/{len(found)}] USERNAME: {cand}{C['x']}")
        print(f"{C['y']}{C['B']}{'=' * 44}{C['x']}")
        count = cari(cand)
        hasil_akhir.append((cand, count))
        print(f"{C['y']}{C['B']}>>> {cand} = {count} situs ditemukan{C['x']}")

    # RINGKASAN AKHIR
    print(f"\n{C['c']}{'=' * 44}{C['x']}")
    print(f"{C['g']}{C['B']}RINGKASAN AKHIR — {nama}{C['x']}")
    if region:
        print(f"{C['d']}Daerah: {region}{C['x']}")
    print(f"{C['c']}{'=' * 44}{C['x']}")

    for cand, count in sorted(hasil_akhir, key=lambda x: -x[1]):
        warn = C['g'] if count > 0 else C['r']
        print(f"{C['y']}{cand:<22}{C['x']} : {warn}{C['B']}{count} situs{C['x']}")

    total_semua = sum(c for _, c in hasil_akhir)
    print(f"{C['c']}{'=' * 44}{C['x']}")
    print(f"{C['d']}Total: {len(hasil_akhir)} username, {total_semua} jejak akun{C['x']}")

    fname = f"hasil_gabungan_{nama.replace(' ', '_').lower()}.txt"
    with open(fname, "w", encoding="utf-8") as fh:
        fh.write(f"Pencarian gabungan: {nama}\n")
        if region:
            fh.write(f"Daerah: {region}\n")
        fh.write("\n" + "=" * 44 + "\n")
        fh.write("RINGKASAN PER USERNAME\n")
        fh.write("=" * 44 + "\n")
        for cand, count in sorted(hasil_akhir, key=lambda x: -x[1]):
            fh.write(f"{cand} : {count} situs\n")
        fh.write(f"\nTotal: {len(hasil_akhir)} username, {total_semua} jejak akun\n")
        fh.write("\nDetail lengkap per username ada di hasil_<username>.txt\n")
    print(f"\n{C['g']}Ringkasan disimpan di {fname}{C['x']}")


# ===== FITUR 4: pencarian username massal =====

def tanya_yn(pesan):
    """Tanya y/n sampai jawabannya valid. Return True kalau y."""
    while True:
        j = input(f"{C['y']}{pesan} (y/n) {C['w']}>> {C['x']}").strip().lower()
        if j in ("y", "ya"):
            return True
        if j in ("n", "t", "tidak"):
            return False
        print(f"{C['r']}Ketik y atau n.{C['x']}")


def baca_file_username(path):
    """Baca daftar username dari file txt (satu per baris).
    Return (daftar, dilewati), atau None kalau file tidak ditemukan."""
    path = os.path.expanduser(path.strip().strip("\"'"))
    if not os.path.isfile(path) and os.path.isfile(path + ".txt"):
        path += ".txt"
    if not os.path.isfile(path):
        return None
    daftar, dilewati, lihat = [], 0, set()
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for baris in fh:
            u = baris.strip().lstrip("@")
            if not u:
                continue
            if " " in u or "\t" in u or u.lower() in lihat:
                dilewati += 1
                continue
            lihat.add(u.lower())
            daftar.append(u)
    return daftar, dilewati


def input_manual():
    """Input username satu per satu. 1 = tambah lagi, 2 = selesai & cari."""
    daftar = []
    while True:
        u = input(f"\n{C['g']}[?] Masukkan username >> {C['x']}").strip().lstrip("@")
        if not u or " " in u:
            print(f"{C['r']}Username tidak valid, coba lagi.{C['x']}")
        elif u.lower() in [x.lower() for x in daftar]:
            print(f"{C['y']}'{u}' sudah ada di daftar.{C['x']}")
        else:
            daftar.append(u)
            print(f"{C['g']}[+] Ditambahkan: {u}  (total {len(daftar)}){C['x']}")
        while True:
            lanjut = input(
                f"{C['y']}[1]{C['x']} Tambah username lagi  "
                f"{C['y']}[2]{C['x']} Selesai & lanjut cari {C['w']}>> {C['x']}"
            ).strip()
            if lanjut in ("1", "2"):
                break
            print(f"{C['r']}Ketik 1 atau 2.{C['x']}")
        if lanjut == "2":
            return daftar


def cari_massal():
    """Mode 4: cari banyak username sekaligus (dari file txt atau input manual)."""
    print(f"\n{C['c']}{C['B']}CARI USERNAME MASSAL{C['x']}")
    print(f"{C['y']}[1]{C['x']} Dari file txt {C['d']}(satu username per baris){C['x']}")
    print(f"{C['y']}[2]{C['x']} Input manual")
    print(f"{C['y']}[b]{C['x']} Kembali")

    try:
        pilih = input(f"\n{C['g']}[?] Pilih >> {C['x']}").strip().lower()
        if pilih == "1":
            fn = input(f"{C['g']}[?] Nama file txt (contoh: list.txt) >> {C['x']}").strip()
            if not fn:
                return
            data = baca_file_username(fn)
            if data is None:
                print(f"{C['r']}File '{fn}' tidak ditemukan. Cek nama/lokasi file.{C['x']}")
                return
            daftar, dilewati = data
            print(f"{C['g']}[+] {len(daftar)} username terbaca dari {fn}{C['x']}")
            if dilewati:
                print(f"{C['d']}    ({dilewati} baris dilewati: kembar / mengandung spasi){C['x']}")
        elif pilih == "2":
            daftar = input_manual()
        else:
            return

        if not daftar:
            print(f"{C['r']}Tidak ada username untuk dicari.{C['x']}")
            return

        total_situs = len(parse_sites())
        print(f"\n{C['c']}Daftar username ({len(daftar)}):{C['x']}")
        for u in daftar[:8]:
            print(f"  {C['w']}{u}{C['x']}")
        if len(daftar) > 8:
            print(f"  {C['d']}... dan {len(daftar) - 8} lainnya{C['x']}")
        print(f"{C['d']}Total {len(daftar)} username x {total_situs} situs = "
              f"{len(daftar) * total_situs} pengecekan (bisa lama){C['x']}\n")

        if not tanya_yn("Mulai pencarian?"):
            print(f"{C['y']}Dibatalkan.{C['x']}")
            return
    except (EOFError, KeyboardInterrupt):
        print()
        return

    hasil = {}
    garis = "=" * 44
    try:
        for i, u in enumerate(daftar, 1):
            print(f"\n{C['y']}{C['B']}{garis}{C['x']}")
            print(f"{C['y']}{C['B']}[{i}/{len(daftar)}] USERNAME: {u}{C['x']}")
            print(f"{C['y']}{C['B']}{garis}{C['x']}")
            cari(u, simpan=False, koleksi=hasil)
            print(f"{C['y']}{C['B']}>>> {u} = {len(hasil[u])} situs ditemukan{C['x']}")
    except (KeyboardInterrupt, EOFError):
        print(f"\n{C['r']}[!] Dibatalkan. Menampilkan hasil yang sudah selesai.{C['x']}")

    if not hasil:
        print(f"{C['r']}Belum ada hasil.{C['x']}")
        return

    # Ringkasan akhir
    print(f"\n{C['c']}{garis}{C['x']}")
    print(f"{C['g']}{C['B']}RINGKASAN PENCARIAN MASSAL{C['x']}")
    print(f"{C['c']}{garis}{C['x']}")
    urut = sorted(hasil.items(), key=lambda kv: -len(kv[1]))
    total_jejak = sum(len(v) for v in hasil.values())
    for u, v in urut:
        warna = C["g"] if v else C["r"]
        print(f"{C['y']}{u:<22}{C['x']} : {warna}{C['B']}{len(v)} situs{C['x']}")
    print(f"{C['c']}{garis}{C['x']}")
    print(f"{C['d']}Total: {len(hasil)} username, {total_jejak} jejak akun{C['x']}\n")

    # Simpan hanya kalau disetujui
    try:
        if tanya_yn("Simpan hasil ke hasil_massal.txt?"):
            with open("hasil_massal.txt", "w", encoding="utf-8") as fh:
                fh.write("Pencarian massal - BY. MR414N-ID\n")
                fh.write(f"Total: {len(hasil)} username, {total_jejak} jejak akun\n")
                for u, v in urut:
                    fh.write(f"\n=== {u} ({len(v)} situs) ===\n")
                    for nama_situs, link in sorted(v):
                        fh.write(f"{nama_situs} : {link}\n")
            print(f"{C['g']}Tersimpan di hasil_massal.txt{C['x']}")
        else:
            print(f"{C['y']}Hasil tidak disimpan.{C['x']}")
    except (EOFError, KeyboardInterrupt):
        print(f"\n{C['y']}Hasil tidak disimpan.{C['x']}")


def tampilkan_menu():
    print(f"{C['y']}[1]{C['x']} Cari username langsung {C['d']}(500 situs — cara lama){C['x']}")
    print(f"{C['y']}[2]{C['x']} Cari username dari nama {C['d']}(+ filter daerah, pilih manual){C['x']}")
    print(f"{C['y']}[3]{C['x']} Gabungan: nama → kandidat → cek 500 situs tiap kandidat {C['d']}(full auto){C['x']}")
    print(f"{C['y']}[4]{C['x']} Cari username massal {C['d']}(dari file txt / input manual){C['x']}")
    print(f"{C['y']}[q]{C['x']} Keluar")


def main():
    banner()

    # Mode lama tetap jalan: python username.py <username>
    if len(sys.argv) > 1:
        username = sys.argv[1].strip().lstrip("@")
        if username:
            cari(username)
            print(C["c"] + "\nTerima kasih!  —  BY. MR414N-ID" + C["x"])
        return

    # Mode menu
    while True:
        print(f"\n{C['c']}{C['B']}MENU UTAMA{C['x']}")
        tampilkan_menu()
        try:
            pilih = input(f"\n{C['g']}[?] Pilih >> {C['x']}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if pilih in ("q", "quit", "exit"):
            break
        elif pilih == "1":
            try:
                username = input(f"\n{C['g']}[?] Masukkan username >> {C['x']}").strip().lstrip("@")
            except (EOFError, KeyboardInterrupt):
                break
            if username:
                cari(username)
        elif pilih == "2":
            try:
                nama = input(f"\n{C['g']}[?] Masukkan nama lengkap >> {C['x']}").strip()
                if not nama:
                    continue
                region = input(f"{C['g']}[?] Daerah (contoh: Bandung, kosongkan jika tidak perlu) >> {C['x']}").strip()
            except (EOFError, KeyboardInterrupt):
                break
            cari_dari_nama(nama, region)
        elif pilih == "3":
            try:
                nama = input(f"\n{C['g']}[?] Masukkan nama lengkap >> {C['x']}").strip()
                if not nama:
                    continue
                region = input(f"{C['g']}[?] Daerah (contoh: Bandung, kosongkan jika tidak perlu) >> {C['x']}").strip()
            except (EOFError, KeyboardInterrupt):
                break
            cari_gabungan(nama, region)
        elif pilih == "4":
            cari_massal()
        else:
            print(f"{C['r']}Pilihan tidak valid.{C['x']}")

    print(C["c"] + "\nTerima kasih!  —  BY. MR414N-ID" + C["x"])


if __name__ == "__main__":
    main()
