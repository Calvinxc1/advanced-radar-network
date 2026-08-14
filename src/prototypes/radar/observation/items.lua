local constants = require("prototypes.radar.constants")
local helpers = require("prototypes.radar.helpers")

local vanilla_radar_item = data.raw.item["radar"]
local item_subgroup = vanilla_radar_item.subgroup or "defensive-structure"

for _, spec in pairs(constants.observation_specs) do
  local locale_name = "arn_observation-radar-" .. spec.tier

  -- Observation radar I replaces the vanilla radar item in place (internal
  -- name stays "radar"); see entities.lua for why, including why icon/
  -- icon_size are left untouched only for tier I.
  local item = spec.tier == 1 and vanilla_radar_item or {
    type = "item",
    name = locale_name,
    subgroup = item_subgroup,
    order = "d[radar]-a[observation]-" .. spec.tier,
    place_result = locale_name,
    stack_size = 50,
  }

  item.icons = helpers.observation_icon(spec.tier)
  if spec.tier == 1 then
    item.localised_name = { "item-name." .. locale_name }
    item.localised_description = { "item-description." .. locale_name }
    item.order = "d[radar]-a[observation]-1"
  else
    data:extend({ item })
  end
end
