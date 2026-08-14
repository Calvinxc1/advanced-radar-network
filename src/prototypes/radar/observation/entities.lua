local constants = require("prototypes.radar.constants")
local helpers = require("prototypes.radar.helpers")

local vanilla_radar = data.raw.radar["radar"]

for _, spec in pairs(constants.observation_specs) do
  local locale_name = "arn_observation-radar-" .. spec.tier
  local next_name = spec.tier < 3 and "arn_observation-radar-" .. (spec.tier + 1) or nil

  -- Observation radar I replaces the vanilla radar entity in place rather
  -- than adding a new prototype (its internal name stays "radar"; only the
  -- locale text and stats change) so existing saves transition straight
  -- from vanilla radar into it. Every tier still needs the identical 2x2
  -- footprint below -- next_upgrade requires matching bounding boxes along
  -- the whole chain.
  local radar = spec.tier == 1 and vanilla_radar or util.table.deepcopy(vanilla_radar)
  local internal_name = spec.tier == 1 and "radar" or locale_name
  radar.name = internal_name
  radar.localised_name = { "entity-name." .. locale_name }
  radar.localised_description = { "entity-description." .. locale_name }
  radar.icons = helpers.observation_icon(spec.tier)
  if spec.tier > 1 then
    -- Only clear these for brand-new prototypes. Tier I keeps the vanilla
    -- singular icon/icon_size fields intact (even though icons overrides
    -- them for this entity's own display) because other mods -- observed:
    -- Toxic Biters' tb_infected_radar -- read data.raw.radar.radar
    -- .icon/.icon_size directly when building their own prototypes.
    radar.icon = nil
    radar.icon_size = nil
  end
  radar.minable = { mining_time = 0.1, result = internal_name }
  -- Matches vanilla steel-furnace's own 2x2 collision box exactly (a real,
  -- tested vanilla value) rather than a made-up number; selection_box is
  -- a clean grid-aligned 2x2 for a predictable placement highlight.
  radar.collision_box = { { -0.7, -0.7 }, { 0.7, 0.7 } }
  radar.selection_box = { { -1, -1 }, { 1, 1 } }
  radar.fast_replaceable_group = "arn_observation-radar"
  radar.next_upgrade = next_name
  radar.pictures = helpers.observation_pictures(spec.tier)
  -- The vanilla radar (or its deepcopy) still carries integration_patch,
  -- water_reflection, and circuit_connector, all sized/positioned for its
  -- original 3x3 footprint. Left in place, they either draw a mismatched
  -- ground decal/reflection or attach wires outside this entity's own
  -- 2x2 hitbox.
  radar.integration_patch = nil
  radar.water_reflection = nil
  radar.circuit_connector = nil
  radar.circuit_wire_max_distance = nil
  radar.energy_source = {
    type = "electric",
    usage_priority = "secondary-input",
  }
  radar.max_health = 100 + spec.tier * 75
  radar.corpse = vanilla_radar.corpse
  radar.rotation_speed = 0.0015 + spec.tier * 0.001
  radar.is_military_target = false
  helpers.set_radar_stats(radar, spec.range, 0, spec.energy_usage, "1J", "1YJ")

  if spec.tier > 1 then
    data:extend({ radar })
  end
end
