# Advanced Radar Network

Advanced Radar Network is a Factorio 2.1 + Space Age mod that splits vanilla radar's two jobs, local visibility and long-range scanning, into two separate progressions instead of one entity that does both adequately.

Vanilla radar bundles always-on local visibility with periodic long-range sector scanning. This mod adds an observation branch that trades away scanning for strong local visibility, and a reconnaissance branch that trades away local visibility for fast, far-reaching scanning, so covering a base and finding distant resources become deliberate, separately-upgradable investments.

## Requirements

- Factorio 2.1.
- Space Age.

## Features

- Three-tier observation radar progression for compact, always-on local visibility with no long-range scanning; Observation Radar I replaces the vanilla radar entity and technology in place, so new and existing games transition straight from vanilla radar into it.
- Three-tier reconnaissance radar progression for long-distance sector scanning with a minimal local visibility floor, fully independent of the vanilla radar tech position.
- Independent `fast_replaceable_group` and `next_upgrade` chains per branch, so within-branch upgrades are a drag-and-replace.
- Observation radars use a 2x2 footprint (reconnaissance radars keep vanilla radar's 3x3 footprint). All six radar tiers use temporary placeholder art; observation radars use a separate icon and world sprite, matching vanilla radar's own convention: a shallow 3/4-angle icon for inventory/tech tree slots, and a steep near-overhead camera angle with a grounded contact shadow for the placed entity. The placed entity is currently a static single frame (unlike vanilla radar's rotating dish); see docs/radar-network-benchmark.md for why a rotation animation hasn't landed yet. No third-party asset mod dependency.

## Progression Shape

Current tier behavior is documented in [docs/radar-network-benchmark.md](docs/radar-network-benchmark.md).

## Installation

Install the released mod through the Factorio mod portal when available. Release packages are also attached to repository releases as `{mod-name}_{version}.zip`.

For local development, keep the repository layout intact and run validation from the repository root:

```sh
./scripts/validate.sh
```

### External-mod validation

CI reads `src/info.json`, downloads every declared Mod Portal dependency (required, recommended, optional, and hidden optional), and then headlessly validates the local source against that complete mod list. Configure the repository Actions secrets `FACTORIO_MOD_PORTAL_USERNAME` and `FACTORIO_MOD_PORTAL_TOKEN` with a Factorio account username and service token; neither value is logged or stored in the repository.

The same download can be run locally:

```sh
export FACTORIO_MOD_PORTAL_USERNAME='your-factorio-username'
export FACTORIO_MOD_PORTAL_TOKEN='your-factorio-service-token'
./scripts/download-factorio-mods.py --mods-dir /tmp/factorio-mods --from-info src/info.json
```

`--from-info` automatically follows the full dependency closure, including optional and recommended dependencies, and uses the local mod's declared Factorio version. This makes the workflow portable to another repository without hard-coded mod names. For a direct Mod Portal download, `--with-dependencies` follows required and recommended (`+`) dependencies; add `--include-optional-dependencies` for its full optional closure.

Semantic versioning policy is documented in [docs/semantic-versioning.md](docs/semantic-versioning.md).

Release packaging and automated deployment are documented in [docs/release-process.md](docs/release-process.md).

Contribution guidelines are documented in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Advanced Radar Network is released under the [MIT License](LICENSE).

## AI Disclosure

This mod is developed with substantial AI assistance. AI tools have contributed to code implementation, documentation, validation workflow setup, release automation, and temporary placeholder artwork (the observation radar entity graphic, pending real art).

AI-assisted work in this repository is governed through the policy files under `.governance/`. Those policies are intended to keep AI contributions reviewable, scoped to the task at hand, and aligned with the repository's validation and release process.
