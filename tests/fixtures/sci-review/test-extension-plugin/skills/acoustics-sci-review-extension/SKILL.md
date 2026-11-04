---
name: acoustics-sci-review-extension
description: "sci-review extension: acoustics. Adds an acoustician perspective and an acoustics reference document to a sci-review panel. Consumed by sci-review only; not for direct use."
---

# Acoustics extension for sci-review

This skill is consumed by `sci-review`. It declares, in `extension.json`, an acoustician perspective (`perspective.md`) and one reference document (`reference/acoustics.md`), together with the files and imports to which they apply.

A model that loads this skill directly must not perform a review from it. Run the `sci-review` skill instead; `sci-review` discovers this extension, decides whether it applies to the code under review, and adds the acoustician to the panel when it does.
