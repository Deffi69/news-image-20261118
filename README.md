# The World on One Page — Wednesday 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Deffi69/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Deffi69/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)


A make.fun `news-image-20261118` entry: a program that draws one image
summing up the world news of Wednesday 18 November 2026.

## The image

A cream newspaper front page, 1024×1024 PNG:

- **Masthead** — "THE WORLD ON ONE PAGE", with the date line
  *Wednesday 18 November 2026*
- **The Day in Numbers** — $83 (Anthropic IPO price), 5,412 (US measles
  cases in 2026), 3.6% (UK inflation, a one-year high)
- **3 hero stories** — Trump, Xi and Putin meet in China for a historic
  summit; Anthropic prices its record IPO at $83 a share; Iran fires on
  Kuwait and Bahrain after a US strike
- **16 numbered story cards** with simplified flag badges — Nvidia beats
  forecasts; GTA 6 unlocks first in New Zealand; Waymo pulls driverless
  cars off all US freeways; US loses measles-free status; Bangladesh sends
  in troops over Hasina unrest; UN court set for historic genocide verdict
  on Myanmar; Peltola wins Alaska; Israel's rare ground raid in Gaza; Fed
  minutes point to faster hikes; UK inflation 3.6%; Prince Harry warns of
  Russia; William and Kate meet Modi; TfL breach exposes 265,000
  customers; Philippines seeks charges in the Thomas Markle case; Costa
  Rica journalist shot dead; Pope bids farewell to Peru
- **The Day Around the World** — a dark world map band with numbered red
  dots marking where each story happened
- **In Brief** — Java security flaw; Crimea Bridge blast video; Ukraine's
  pipeline war; South Korea's exam crackdown; UK energy bills up £443;
  Hakeem Jeffries nominated as next US House Speaker

Every headline and figure was checked against wire and major sources
(Reuters, AP, BBC, AFP, PAHO, CDC) for 18 November 2026. No headline or
number was invented.

## Run it

```sh
python3 main.py          # writes /output/entry.png
```

Requirements: Python 3.13, Pillow. No network access. Fully deterministic:
running it twice produces byte-identical output.

## License

MIT — see `LICENSE`.
