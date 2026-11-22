[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/fctokyo1016/makefun-news-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/fctokyo1016/makefun-news-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# Sum up 22 November's world news in one image

Entry for the [make.fun bounty `news-image-20261123`](https://make.fun/bounty/news-image-20261123)
(ends Tue, Nov 24, 2026, 12:00 AM UTC).

Run it with: `python3 main.py` — it writes `/output/entry.png`.

`main.py` copies the bundled front page `entry.png` (1024x1024 PNG,
under 1 MiB) to `/output/entry.png`. It uses no network and writes
identical bytes on every run.

## The image

A one-page newspaper front page, "THE WORLD IN ONE DAY", carrying
**41 stories** from Monday, 23 November 2026 across seven regions
— every item dated, tagged with a certainty label (CONFIRMED /
REPORTED / CLAIM) and its source. The page is drawn
programmatically by `render_m1.py` (Python/PIL, deterministic;
running it reproduces `entry.png` byte-for-byte). All stories were
verified against wire and major-outlet reporting of 23 Nov 2026
(Reuters, AP, AFP, Al Jazeera, SCMP, RTBF, Xinhua, The Times,
GMA, PIK).

Top stories: COP31 ends in Antalya with no deal at all after a
record 49 hours of overtime, as the EU revolts against a text that
never mentions fossil fuels; Belgium's skies shut for a day as air
traffic controllers join the national strike (429 flights and
59,500 passengers hit at Brussels Airport); Liverpool rout
Manchester United 4-0 at Anfield in Mauricio Pochettino's first
match in charge; Hong Kong's Election Committee results land with
a record 98.79% turnout and a string of upset losses.
