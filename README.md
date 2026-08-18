# Count Blackjack

A mobile-first HTML blackjack game that teaches the **Hi-Lo card counting** system. Open `index.html` in Safari on your iPhone — no build step required.

## Features

- Full blackjack: Hit, Stand, Double, Surrender
- 6-deck shoe with automatic shuffle at ~75% penetration
- **Learn mode** — see +1 / 0 / −1 badges on every card
- **Practice mode** — hide counts and quiz yourself after each hand
- Live running count, true count, and decks-remaining display
- Built-in tutorial explaining Hi-Lo and basic strategy

## Play on iPhone

1. Open `index.html` in **Safari**
2. Tap **Share → Add to Home Screen** for an app-like experience

Or serve locally and visit from your phone on the same Wi‑Fi:

```bash
python3 -m http.server 8080
# then open http://<your-ip>:8080 on your iPhone
```

## Hi-Lo Quick Reference

| Cards   | Count |
|---------|-------|
| 2–6     | +1    |
| 7–9     | 0     |
| 10, J, Q, K, A | −1 |

**True count** = running count ÷ decks remaining

## License

MIT — use freely for learning and personal projects.
