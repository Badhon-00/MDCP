# design-tokens.md

Define once, use everywhere. Replace the values with the project's own.

```css
:root {
  --bg: #0b0d12;
  --surface: #12151c;
  --text: #e8eaf0;
  --muted: #9aa3b2;
  --accent: #4da3ff;
  --border: #232836;
  --radius: 10px;
  --space-1: 4px; --space-2: 8px; --space-3: 16px; --space-4: 24px; --space-5: 40px;
  --font-display: "Your Display Face", system-ui, sans-serif;
  --font-body: "Your Body Face", system-ui, sans-serif;
}
@media (prefers-color-scheme: light) {
  :root { --bg: #f6f7fa; --surface: #fff; --text: #14161c; --muted: #5b6372; --border: #dfe3ec; }
}
```

Check text contrast of every token pair in both themes.
