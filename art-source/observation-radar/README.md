# Observation Radar Art Source

`obs-radar-script.py` is the Blender 4.3.2 script that generates the
observation radar's icon and placed-entity rotation animation
(`src/graphics/entity/observation-radar/`). It builds the model
procedurally and renders it with two fixed orthographic cameras, so the
placed-entity frames share an identical base position and size across all
16 rotation angles.

Run headless:

```sh
blender --background --python obs-radar-script.py
```

Output lands in `~/factorio_radar_output/` (`inventory.png`,
`placed_frames/radar_00.png`..`radar_15.png`, `placed_4x4_atlas.png`);
copy the icon and atlas into `src/graphics/entity/observation-radar/`
manually and update the `scale`/`shift` values in
`src/prototypes/radar/helpers.lua` if the render geometry changes.
