# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/choirunconslet-boop/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/choirunconslet-boop/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026,
built for the make.fun bounty `news-image-20261119`.

## The image

A newspaper front page, "THE WORLD", with six stories:

1. **Lead — The Hague:** the International Court of Justice rules on
   whether Myanmar committed genocide against the Rohingya.
2. **Geopolitics:** Xi, Putin and Trump meet in their first trilateral,
   in Shenzhen on the APEC sidelines.
3. **Culture:** Grand Theft Auto VI rolls out worldwide; Vice City opens.
4. **Space:** NASA confirms Voyager 1 is one light-day from Earth.
5. **Diplomacy:** Australia sanctions Israeli settlers over West Bank
   expansion.
6. **Weather:** Cyclone Akvan bears down on India's east coast.

An "Also on 19 Nov" box carries four more items. Every story was
verified against live reporting dated 19 November 2026 — see
SOURCES.md.

## Files

- `entry.png` — the finished front page (1024x1024, PNG).
- `main.py` — the entry program: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). Standard library
  only, no network, deterministic.
- `render_frontpage.py` — the script that drew the front page with PIL
  (flat illustrations, headlines, decks). Re-run it to rebuild
  `entry.png`: `python3 render_frontpage.py entry.png`.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=j32a98da&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>

License: MIT.
