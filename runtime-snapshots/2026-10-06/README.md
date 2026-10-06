# Tested OFM runtime source snapshots

This directory preserves the isolated 2026-10-06 GPU-test runtime: ComfyUI
core and the installed custom-node source directories, including compatibility
changes. Each package contains its upstream notices and license files.

`sources.lock.json` records the upstream revision, modified files, every source
file hash, the complete archive hash and the ordered archive parts. Concatenate
the listed parts in order to recover a `.tar.gz` archive. Parts stay below the
GitHub regular-blob size limit. Model weights, interpreter environments, caches,
credentials and redundant nested distribution ZIPs are excluded.

Restore only from a full Git commit, never a moving branch head. Verify all
parts and archive/file hashes before writing the sources. `verify_sources.py`
performs a read-only verification; its optional Linux-only restore writes a
new, empty ComfyUI directory and does not install Python packages or weights.

This publication adds an independent source snapshot branch. It does not
modify existing mirror paths, a Docker image/tag, any bot, a cloud template,
or a deployment repository. There is no CI workflow in this branch.

The source snapshot is evidence and an input for the next image build. Clean
image dependency resolution and regression checks remain required. MiniMax
uses the separate OFM NVIDIA SDK worker; the unverified DLSS5/FG paths are not
enabled in the accepted short-test graphs.
