---
title: How to build a completely native static site generator
date: 2026-06-16
---

## Brutalist Web Development

Today I built my own static site generator in ~100 lines of Python.

Instead of relying on Jekyll, Next.js, or Hugo, I realized that I just need a script that reads Markdown, injects it into an HTML template, and manages the file hierarchy for me.

### Why?
Because human endeavor should be limitless, and relying on black-box frameworks hides the fundamental mechanics of the web.

**Benefits:**
- Zero dependencies
- Fast
- Perfect Markdown integration
