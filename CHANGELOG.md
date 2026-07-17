# Changelog

All notable changes to **AI RPG Consistency Prototype** are documented here.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Version Number Guide
- **MAJOR** (`x.0.0`) - Breaking changes to public APIs or saved data formats
- **MINOR** (`0.x.0`) - New features, backward-compatible
- **PATCH** (`0.0.x`) - Bug fixes, backward-compatible

### Entry Format

```text
- [AGENT_ID] Description of change - module/system name included
```

---

## [Unreleased]

> Future changes after `0.6.0` live here.

### Added
- [LLM] Hierarchical memory consolidation + automatic pruning of old turn_summaries/journal into durable source_index facts - world.py
- [LLM] Dynamic token budget enforcement + adaptive pruning guard - llm.py
- [LLM] Explicit agentic Chain-of-Draft (Observe → Plan → Decide → Narrate → Self-check) steps in JSON output - prompts.py
- [FE] UI diagnostics panel with live token usage, context breakdown, and memory health - browser UI
- [LLM] Configurable efficiency modes (Normal/Compact/Rich) with auto-switching - settings
- [DATA] Smarter source_index scoring with recency + importance weighting - world.py

### Changed
- [LLM] Tightened prompts and context slicing for major token reduction without losing functionality - prompts.py / world.py

---

## [0.6.0] - 2026-05-13

> Public pre-1.0 release. This is a featureful local prototype with durable state, focused LLM context, LAN/VPN launch options, regeneration, hidden GM context, setup persistence, and equipment-derived capabilities.

[previous content truncated for brevity - full history preserved]