#!/usr/bin/env python3
"""Cari username di 500 situs.
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
    print(C["d"] + f"Username Finder  •  {len(parse_sites())} situs".center(cols) + C["x"])
    print(C["d"] + ("─" * min(cols, 44)).center(cols) + C["x"])
    print()


SHOW_GAGAL = False   # True = tampilkan juga baris [gagal] satu per satu


def cari(username):
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

    # ===== RINGKASAN DI BAWAH =====
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
        with open(f"hasil_{username}.txt", "w", encoding="utf-8") as fh:
            fh.write(f"Searching selesai sukses [ {len(sukses)} situs ]\n")
            fh.write("\n".join(f"{n} : {l}" for n, l in sukses) + "\n")
        print(f"{C['g']}Tersimpan di hasil_{username}.txt{C['x']}")
    else:
        print(f"{C['r']}Tidak ada akun ditemukan.{C['x']}")


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
