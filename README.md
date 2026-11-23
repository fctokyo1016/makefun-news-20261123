[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/fctokyo1016/makefun-news-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/fctokyo1016/makefun-news-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# Sum up 23 November's world news in one image

Entry for the [make.fun bounty `news-image-20261123`](https://make.fun/bounty/news-image-20261123)
(ends Tue, Nov 25, 2026, 09:00 JST).

Run it with: `python3 main.py` — it writes `/output/entry.png`.

`main.py` copies the bundled front page `entry.png` (1024x1024 PNG,
under 1 MiB) to `/output/entry.png`. It uses no network and writes
identical bytes on every run.

## The image

A one-page newspaper front page, "THE WORLD IN ONE DAY", carrying
**41 stories** from Monday, 23 November 2026 across seven regions
plus sport, markets and science — every item dated and tagged with
its source and a certainty level (CONFIRMED / REPORTED / CLAIM).
The page is drawn programmatically by `render.py`
(Python/PIL, deterministic; running it reproduces `entry.png`
byte-for-byte). All stories were verified against wire and
major-outlet reporting of 23 Nov 2026 (Reuters, AP, AFP,
Al Jazeera, RTBF, Xinhua, SCMP, The Times, El País, GMA,
Haaretz, KCNA, ATP).

Top stories: the COP31 climate summit's collapse in Antalya with
no cover decision adopted after a record 49 hours of overtime;
Belgium's nationwide strike shutting air traffic control for
14 hours, with 429 flights and ~59,500 passengers due at
Brussels Airport; Liverpool's 4-0 rout of Manchester United
at Anfield in Mauricio Pochettino's first match in charge;
Hong Kong's record-turnout Election Committee poll (98.79%);
and the Russian cargo ship Sparta II still burning off Finland.
