local constants = require("prototypes.radar.constants")
local helpers = require("prototypes.radar.helpers")
local vanilla_snapshot = require("prototypes.radar.vanilla_snapshot")

-- Reconnaissance is a fully independent three-tier line now -- none of its
-- tiers touch the vanilla radar prototype in place (Observation I owns
-- that role; see observation/entities.lua). Each tier deepcopies the
-- pristine pre-mutation vanilla_snapshot as its graphics/box template
-- (original 3x3 footprint, layered dish+shadow animation, integration
-- patch, water reflection, circuit connector all intact), not the live
-- data.raw.radar["radar"], which by this point is Observation I's mutated
-- 1x1 footprint with placeholder art.
for _, spec in pairs(constants.recon_specs) do
  local name = "arn_recon-radar-" .. spec.tier
  local previous_name = spec.tier > 1 and "arn_recon-radar-" .. (spec.tier - 1) or nil
  local next_name = spec.tier < 3 and "arn_recon-radar-" .. (spec.tier + 1) or nil

  local radar = util.table.deepcopy(vanilla_snapshot)
  radar.name = name
  radar.localised_name = { "entity-name." .. name }
  radar.localised_description = { "entity-description." .. name }
  radar.icons = helpers.item_icon(helpers.recon_tints[spec.tier])
  radar.minable = { mining_time = 0.1, result = name }
  radar.fast_replaceable_group = "arn_recon-radar"
  radar.next_upgrade = next_name
  radar.pictures = helpers.tint_animation(vanilla_snapshot.pictures, helpers.recon_tints[spec.tier])
  radar.max_health = 300 + spec.tier * 100
  radar.is_military_target = false
  helpers.set_radar_stats(
    radar,
    spec.nearby_range,
    spec.scan_range,
    spec.energy_usage,
    spec.nearby_scan_energy,
    spec.sector_scan_energy
  )

  if previous_name then
    data.raw.radar[previous_name].next_upgrade = name
  end
  data:extend({ radar })
end
