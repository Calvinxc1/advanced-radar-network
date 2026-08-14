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

-- Placeholder art for observation radars' 2x2 footprint, replaced 2026-08-14
-- with a procedural Blender 4.3.2 model (see obs-radar-script.py) rendered
-- with two fixed orthographic cameras -- a three-quarter "product shot" for
-- the icon, and an almost-overhead, front-aligned camera for the placed
-- entity. Because both the camera and the base geometry are locked in the
-- scene (only the dish/trunnion assembly rotates between frames), this
-- supersedes two earlier AI-image approaches that both fought the same
-- problem from different angles: a literal 2D in-plane spin and a
-- squash/mirror-flip "coin spin" trick derived every angle from a single
-- source layer and looked wrong for an obliquely-viewed disc; a later
-- 16-keyframe AI turntable got the angles right but wasn't a pixel-locked
-- camera, so the base drifted a few px frame to frame and needed per-frame
-- re-centering. A true 3D render sidesteps both failure modes at the
-- source. See .governance/local/factorio-workflow.yaml before revisiting
-- this again.
local observation_radar_icon_image = "__advanced-radar-network__/graphics/entity/observation-radar/observation-radar.png"
local observation_radar_icon_image_size = 256
-- Rotating dish: a direction_count/line_length spritesheet, the same
-- technique vanilla radar.png itself uses (direction_count = 64,
-- line_length = 8) -- Factorio steps through discrete frames rather than
-- blending, so no cross-fade is needed. 16 frames at exactly 22.5 degrees
-- apart (frame N = N * 22.5 deg, 0..337.5), a full 360 degree sweep by
-- construction since the render script drives the rotation directly.
local observation_radar_world_image = "__advanced-radar-network__/graphics/entity/observation-radar/observation-radar-world.png"
local observation_radar_world_image_width = 256
local observation_radar_world_image_height = 256
local observation_radar_world_direction_count = 16
local observation_radar_world_line_length = 4

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

-- scale/shift are derived, not eyeballed. Because the camera and base are
-- both fixed in the Blender scene, every one of the 16 frames shares the
-- same bbox: (65,27)-(191,204) at direction 0 loosest, narrowing only in
-- height as the dish's tilt-exposed height changes with rotation phase --
-- width and the bottom edge (204) never move, since the base itself never
-- rotates or resizes. scale puts that shared 126px width at exactly 2
-- tiles edge-to-edge; shift.y accounts for the object's bottom sitting 52px
-- above the 256px canvas's own bottom edge (not flush) and puts it on the
-- 2x2 footprint's bottom edge (selection_box bottom at y=+1.0). See
-- .governance/local/factorio-workflow.yaml for the full derivation.
local function observation_pictures(tier)
  return tint_animation({
    filename = observation_radar_world_image,
    width = observation_radar_world_image_width,
    height = observation_radar_world_image_height,
    scale = 0.507937,
    shift = { 0, -0.206345 },
    direction_count = observation_radar_world_direction_count,
    line_length = observation_radar_world_line_length,
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
