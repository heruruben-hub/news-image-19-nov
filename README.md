# news-image-19-nov

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/heruruben-hub/news-image-19-nov/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/heruruben-hub/news-image-19-nov/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One picture of one day: the world news of **Thursday 19 November 2026**, drawn
pixel by pixel by a single Python program.

`main.py` (Python 3, standard library only, no network) draws a newspaper-style
front page on a 1024×1024 canvas and writes it as a PNG to
`/output/entry.png`. It uses no clock and no randomness, so every run produces
exactly the same bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Without `MAKEFUN_OUTPUT_DIR` the image is written to `/output/entry.png`.

## The six stories on the page

1. **Diplomacy — China.** Trump, Xi and Putin hold their first trilateral
   summit in Shenzhen; Ukraine tops the talks.
2. **Markets — Crypto.** Bitcoin falls to a four-month low near $62K, down
   about 15% in a week; the Fear & Greed index reads 10, extreme fear.
3. **Justice — The Hague.** The International Court of Justice delivers its
   genocide judgment in The Gambia v. Myanmar over the Rohingya.
4. **Climate — Türkiye.** COP31 talks in Antalya go on, but a deal stays
   elusive.
5. **Weather — India.** Cyclone Akvan nears Odisha; more than 100,000 people
   evacuated under a red alert.
6. **Arts — New York.** Van Gogh's *Blossoming Chestnut Trees* sells for
   $190.4M at Sotheby's, an auction record for the artist.

## How it is drawn

The program embeds its own 5×7 bitmap font as data and renders every letter,
icon and panel from primitives (rectangles, discs, lines, triangles) into an
RGB framebuffer, then encodes the PNG itself with `zlib` and `struct`. Nothing
is copied from a ready-made image.

## Sources

Each story was checked against reporting published on 19 November 2026:
the New York Times live updates and the Guardian's COP31 live blog for the
summit and the climate talks; CoinGabbar and the day's crypto market briefs
for Bitcoin's four-month low and the Fear & Greed reading of 10; Muslim
Network TV for the ICJ judgment delivered at The Hague; The Hindu's live
updates for Cyclone Akvan's evacuations in Odisha; and Reuters for the
$190.4M Van Gogh record at Sotheby's New York.

Verified locally: two consecutive runs of `main.py` produce byte-identical
PNG files (same SHA-256), 18,638 bytes, 1024×1024 — well inside the
competition's 1 MiB and 1024×1024 limits.

---

Entered on [make.fun](https://make.fun/?ref=kh6903y0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
