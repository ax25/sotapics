#!/usr/bin/env bash
# ------------------------------------------------------------
# SOTApics – one‑shot installer & dev‑server launcher
# Usage:  bash scripts/setup_frontend.sh   (from ./frontend)
# ------------------------------------------------------------
set -euo pipefail

# 1. Install React‑18‑compatible lightbox & swiper (legacy deps flag solves peer issues)
printf "\n▶ Installing dependencies…\n\n"
npm install swiper react-image-lightbox --legacy-peer-deps

# 2. Start Vite dev‑server on all interfaces so you can reach it
#    from any device on your LAN (http://<raspberry‑ip>:5173)
printf "\n▶ Starting dev server on 0.0.0.0:5173  (Ctrl‑C to stop)\n\n"
npm run dev -- --host
