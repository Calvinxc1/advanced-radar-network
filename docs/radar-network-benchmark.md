# Radar Network Benchmark

This benchmark summarizes the two radar branches that split vanilla radar's local-visibility and long-range-scanning roles apart.

The design goal is to make "can I see it live" and "can I find it far away" separate investments instead of one entity doing both adequately. Observation radars trade away scanning entirely for strong, always-on local visibility. Reconnaissance radars trade away local visibility for long-distance sector scanning throughput.

Assumptions:

- Local visibility range is prototype `max_distance_of_nearby_sector_revealed`, in chunks.
- Scan range is prototype `max_distance_of_sector_revealed`, in chunks. `0` means the entity never performs a long-range sector scan.
- Energy usage is prototype `energy_usage`, the base electricity draw.
- Observation radars use `1YJ` (effectively infinite) energy per sector scan so they never actually complete one, keeping them local-visibility-only regardless of scan range being `0`.

| Radar | Tier | Local Visibility Range | Scan Range | Energy Usage | Primary Role |
|---|---:|---:|---:|---:|---|
| Observation I (base radar) | 1 | `4` | `0` | `75kW` | default local visibility, replaces vanilla radar entirely |
| Observation II | 2 | `6` | `0` | `300kW` | wider local visibility for a growing base |
| Observation III | 3 | `10` | `0` | `1MW` | wide local visibility for mature factory infrastructure |
| Reconnaissance I | 1 | `2` | `12` | `700kW` | first scanning tier, unlocked as an alternative to Observation II |
| Reconnaissance II | 2 | `3` | `24` | `2MW` | faster, farther scanning for expansion planning |
| Reconnaissance III | 3 | `5` | `40` | `6MW` | deep late-game scanning for large-scale expansion |

## Branch Reading

- Observation radars never gain scan range; each tier only grows local visibility and durability.
- Reconnaissance radars keep a small local visibility floor (so the tile under the radar itself is never a blind spot) but scale scan range aggressively.
- Observation I replaces the vanilla `radar` prototype directly (entity, item, recipe, and technology), so new and existing saves transition straight from vanilla radar into it. The vanilla technology's prerequisites and cost are left completely unchanged; only the localised text and the entity's stats/graphics change.
- Reconnaissance is fully independent of the vanilla radar prototype. Reconnaissance I is a new prototype, unlocked as a parallel choice to Observation II at the same tech tier (both require `radar` + `chemical-science-pack`), not a prerequisite of it.
- Observation and reconnaissance radars each have their own `fast_replaceable_group` and `next_upgrade` chain, so within-branch upgrades are a drag-and-replace, not a rebuild. Factorio requires every step in a `next_upgrade` chain to share the same bounding box, so all three observation tiers share the same 2x2 `collision_box`/`selection_box` (matching vanilla steel-furnace's real 2x2 collision box) rather than Observation I staying vanilla-sized.

## Compatibility Notes

- Space Age is required.
- No third-party asset mod dependency. Observation radars use temporary placeholder art sized for their 2x2 footprint; reconnaissance radars keep vanilla's original layered dish+shadow animation, tinted, at vanilla's original 3x3 footprint.
- Unlike vanilla radar and reconnaissance radars, the observation radar world sprite is currently a static single frame (`direction_count = 1`), not animated. Two 2D approaches were tried and rejected on 2026-08-14: a literal in-plane rotation of the dish+arm+collar layer (an obliquely-viewed disc tumbles into visually wrong orientations when spun in its own plane instead of appearing to turn around its vertical axis), and a horizontal squash-by-`abs(cos(theta))`-with-mirror-flip "spinning coin" trick (looked like the object was just being flattened and flipped rather than rotating, especially the linear off-axis mount arm). Getting a convincing rotation likely needs either a real 3D model to re-render from multiple angles, or hand-authored frame-by-frame art -- see `.governance/local/factorio-workflow.yaml` before attempting a third automated approach.
- The mod keeps radar progression self-contained so other mods can depend on it without owning radar prototypes themselves.
- Toxic Biters is declared as an optional (`?`) dependency so it loads before this mod. Its `tb_infected_radar` prototype reads `data.raw.radar.radar.icon`/`.icon_size` directly when building its own entity from the vanilla radar, so Observation I keeps those singular fields populated (alongside `icons`) rather than nil-ing them out, and the declared load order makes that read happen against a known-good, not-yet-mutated vanilla radar.
- Reconnaissance's entities are built from a pristine deepcopy of vanilla radar captured before Observation I mutates it in place (`prototypes/radar/vanilla_snapshot.lua`), not from the live, already-mutated vanilla radar prototype -- otherwise reconnaissance would inherit Observation I's 2x2 footprint and placeholder art instead of its own vanilla-derived look.
