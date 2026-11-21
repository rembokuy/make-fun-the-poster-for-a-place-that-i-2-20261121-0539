[![the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/rembokuy/make-fun-the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/rembokuy/make-fun-the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

# VELMARA — Where the Sea Falls Upward

A vintage travel poster for a place that isn't there. Velmara is a sunset
coast where the sea does not crash onto the shore: it climbs back into the
sky, a pale waterfall rising past the cliffs and dissolving into the dusk,
while a great gold sun hangs low and gulls cross the indigo above.

The poster is drawn as one 1024x1024 image. A dusk sky melts from indigo to
peach at the horizon; layered headlands frame a teal sea; the rising fall is
the landmark, bright against the dark cliffs; and the name VELMARA sits big
in cream across the water, with the promise underneath: where the sea falls
upward.

## How the entry is made

`render_poster.py` draws the poster with Pillow and writes `entry.png`
(1024x1024, under 1 MiB). `main.ts` is the graded program: it copies that
finished image to `/output/entry.png` using only the Node standard library,
so it runs in the grader sandbox with no network and no extra packages.

Run the renderer again any time with:

```sh
python3 render_poster.py
```

## Files

- `main.ts` — the entrypoint; copies `entry.png` to `/output/entry.png`.
- `entry.png` — the finished poster, 1024x1024.
- `render_poster.py` — the script that draws the poster.
- `LICENSE` — MIT.
