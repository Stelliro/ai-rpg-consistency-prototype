# Mørkyn

<p align="center">
  <img src="Media/morkyn-logo.png" alt="Mørkyn logo" width="68%" />
</p>

**Version `0.7.0`**

**Mørkyn** is a local-first browser RPG. A local LLM narrates turns and proposes structured world changes, while SQLite remains the source of truth for the player, inventory, NPCs, events, summaries, and long-running continuity.

It is still pre-1.0 software, but it has enough systems to be a playable prototype and a solid base for long playthroughs.

<p align="center">
  <img src="Media/morkyn-key-art.png" alt="Mørkyn key art" width="86%" />
</p>

## Interface

| Setup | Play | Model / context health |
| --- | --- | --- |
| <img src="Media/screen-setup.png" alt="Mørkyn setup" width="100%"> | <img src="Media/screen-play.png" alt="Mørkyn play" width="100%"> | <img src="Media/screen-play-model.png" alt="Mørkyn model tab" width="100%"> |

| World setup | LLM settings | Compact mode |
| --- | --- | --- |
| <img src="Media/screen-setup-world.png" alt="Mørkyn world setup" width="100%"> | <img src="Media/screen-model-settings.png" alt="Mørkyn LLM settings" width="100%"> | <img src="Media/screen-play-compact.png" alt="Mørkyn compact mode" width="100%"> |

Assets: [`Media/`](Media/).

## Highlights

- FastAPI backend with a plain browser UI (no frontend build step).
- SQLite world state stored locally under `data/`.
- Local LLM support through llama.cpp-compatible and Ollama-compatible APIs.
- Character and world setup for identity, previous-life details, rules, abilities, economy, magic, tech, skills, progression, and narration style.
- Action-focused turn context for movement, combat, abilities, conversation, trade, inventory, training, rest, and investigation.
- Deterministic NPC combat profiles (health, attack range, defense, dodge) with LLM prose layered on top.
- Certainty-based selective verification and durable verification memory.
- **Hierarchical memory consolidation** - older turn summaries roll into durable source-index facts.
- **Token budget guard** - pre-call estimation and pruning so prompts stay under safe limits.
- **Campaign save slots** - named slots from the play top bar, plus full world export/import.
- **Context health** panel, **compact mode**, and consolidate-memory control.
- Equipment effects that fold equipped item modifiers into effective stats/abilities only while equipped.
- Stable entity codes with clickable references in narration.
- Visual history, source-index search, World Bible, rewind, regenerate.
- Hidden backend-only GM events for off-screen pressure.
- Local-only, LAN/phone, and trusted VPN launch modes.

## Requirements

- Windows is the primary supported launch target.
- Python 3.11+ recommended.
- A local model server or GGUF model for AI generation.

```powershell
python -m pip install -r requirements.txt
```

## Quick Start

Double-click:

```text
start_ai_rpg.bat
```

Launch modes:

- `1` - This machine only (`http://127.0.0.1:8000`)
- `2` - Local network / phone on the same LAN
- `3` - VPN / private overlay (Tailscale, WireGuard, ZeroTier, OpenVPN)

Non-interactive:

```text
start_ai_rpg.bat local
start_ai_rpg.bat lan
start_ai_rpg.bat vpn 8088
```

## Model Setup

```powershell
$env:AI_RPG_GGUF_MODEL="D:\path\to\model.gguf"
```

You can also choose a GGUF path in **LLM Settings**. Soft Token Target and Hard Token Cap control response generation.

Useful overrides:

```powershell
$env:AI_RPG_LLAMA_CPP_CONTEXT="8192"
$env:AI_RPG_LLAMA_CPP_GPU_LAYERS="-1"
$env:AI_RPG_MAX_RESPONSE_TOKENS="1500"
$env:AI_RPG_RESPONSE_HARD_CAP_TOKENS="2000"
$env:AI_RPG_FAST_VERIFICATION="1"
$env:AI_RPG_MEMORY_KEEP_SUMMARIES="12"
$env:AI_RPG_MEMORY_MAX_FACTS="200"
$env:AI_RPG_GM_OFFSCREEN_INTERVAL="8"
```

## Local 8B turn times

Measured on **Ollama `qwen3:8b`** (Q4_K_M, 32k context, thinking off). Times are wall-clock for a full turn pipeline (draft + repairs + verify on the machine under test), not pure token decode.

| Step | Time |
| --- | ---: |
| Opening scene | ~**1.5–3.1 min** (98–186 s) |
| Typical player turn | ~**1.5–3.5 min** (114–194 s) |
| Mean step (opening + 3 turns) | ~**2.8 min** (~169 s) |
| Full playtest total (4 steps) | ~**11.2 min** (674 s) |

On local 8B, expect multi-minute turns when draft and verify both run. Faster machines, smaller context, `AI_RPG_FAST_VERIFICATION`, or NAR+OPS draft mode (`AI_RPG_DRAFT_MODE=dsl`) can improve this; re-measure after changes.

Full tables and JSON: [`docs/turn-metrics/`](docs/turn-metrics/). Re-run:

```powershell
python tools/playtest_timed_turns.py
```

## Play UI notes

- **Save Slot / Load Slot** - named campaigns under `data/campaign_slots/`.
- **Compact** - denser UI spacing (preference stored in the browser).
- **Context Health** (Model tab) - token budget + summary/fact counts; **Consolidate Memory** forces hierarchical rollup.
- Settings forms keep per-field / group **Randomize** controls for setup fields.

## Development checks

```powershell
python behavior_test.py
```

Covers memory consolidation, token budget pruning, source scoring, campaign slots, and context-health shape.

## Design notes

- New playthroughs start with no default player skills.
- Equipment-granted abilities appear only while the source item is equipped.
- Source-index retrieval ranks hits with keyword overlap plus recency and importance.
- Campaign slots are separate from one-off JSON exports.
- Combat has a deterministic layer for core health/weapon math before narration.

Architecture: [CODEBASE_INDEX.md](CODEBASE_INDEX.md)  
History: [CHANGELOG.md](CHANGELOG.md)  
License: [LICENSE.md](LICENSE.md) (PolyForm Noncommercial)

## Repository

| Field | Value |
| --- | --- |
| Product | **Mørkyn** |
| Version | **0.7.0** |
| GitHub | https://github.com/Stelliro/Morkyn |

Formerly published as AI RPG Consistency Prototype (`ai-rpg-consistency-prototype`).
