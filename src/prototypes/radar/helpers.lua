local observation_tints = {
  nil,
  { r = 0.82, g = 1.0, b = 0.88, a = 1.0 },
  { r = 1.0, g = 0.86, b = 0.56, a = 1.0 },
}

-- Tier 1 needs an actual tint now that Reconnaissance I is a standalone
-- prototype rather than the untinted vanilla radar mutation (that role
-- belongs to Observation I now); leaving it nil here would make the two
-- look visually identical.
local recon_tints = {
  { r = 1.0, g = 0.78, b = 0.5, a = 1.0 },
  { r = 0.78, g = 0.86, b = 1.0, a = 1.0 },
  { r = 0.72, g = 1.0, b = 0.94, a = 1.0 },
}

local function item_icon(tint)
  return {
    {
      icon = "__base__/graphics/icons/radar.png",
      icon_size = 64,
      tint = tint,
    },
  }
end

-- Temporary placeholder art for observation radars' 2x2 footprint. The icon
-- and the placed entity graphic are separate images -- the icon is a clean
-- isolated "product shot" appropriate for inventory/tech tree slots, while
-- the world sprite uses flatter lighting and a grounded contact shadow so
-- it doesn't look like a floating icon sitting in the factory. Swap both
-- for hand-authored art later.
local observation_radar_icon_image = "__advanced-radar-network__/graphics/entity/observation-radar/observation-radar.png"
local observation_radar_icon_image_size = 300
-- Static, non-animated for now. Two rotation approaches were tried and
-- rejected on 2026-08-14: a literal 2D in-plane rotation (an obliquely
-- viewed disc tumbles into wrong-looking orientations), and a horizontal
-- squash-and-mirror-flip "spinning coin" trick (looked like the object was
-- just being flattened and flipped, especially the linear off-axis mount
-- arm, which doesn't transform believably under either technique). See
-- .governance/local/factorio-workflow.yaml before attempting this again.
local observation_radar_world_image = "__advanced-radar-network__/graphics/entity/observation-radar/observation-radar-world.png"
local observation_radar_world_image_width = 335
local observation_radar_world_image_height = 360

local function observation_icon(tier)
  return {
    {
      icon = observation_radar_icon_image,
      icon_size = observation_radar_icon_image_size,
      tint = observation_tints[tier],
    },
  }
end

local function tint_animation(animation, tint)
  if not animation then
    return animation
  end

  local tinted = util.table.deepcopy(animation)

  if tinted.layers then
    for _, layer in pairs(tinted.layers) do
      layer.tint = tint
    end
  else
    tinted.tint = tint
  end

  return tinted
end

-- scale/shift are derived, not eyeballed: object bbox in the 335x360 file
-- is (41,58)-(293,360), object flush with the canvas bottom. scale puts the
-- object's true width at exactly 2 tiles edge-to-edge; shift.y puts the
-- object's bottom on the 2x2 footprint's bottom edge (selection_box bottom
-- at y=+1.0). See .governance/local/factorio-workflow.yaml for the full
-- derivation.
local function observation_pictures(tier)
  return tint_animation({
    filename = observation_radar_world_image,
    width = observation_radar_world_image_width,
    height = observation_radar_world_image_height,
    scale = 0.254,
    shift = { 0, -0.429 },
    direction_count = 1,
  }, observation_tints[tier])
end

local function set_radar_stats(radar, nearby_range, sector_range, energy_usage, nearby_scan_energy, sector_scan_energy)
  radar.max_distance_of_nearby_sector_revealed = nearby_range
  radar.max_distance_of_sector_revealed = sector_range
  radar.energy_usage = energy_usage
  radar.energy_per_nearby_scan = nearby_scan_energy
  radar.energy_per_sector = sector_scan_energy
end

return {
  observation_tints = observation_tints,
  recon_tints = recon_tints,
  item_icon = item_icon,
  observation_icon = observation_icon,
  tint_animation = tint_animation,
  observation_pictures = observation_pictures,
  set_radar_stats = set_radar_stats,
}
