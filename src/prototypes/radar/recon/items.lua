local constants = require("prototypes.radar.constants")
local helpers = require("prototypes.radar.helpers")

local item_subgroup = data.raw.item["radar"].subgroup or "defensive-structure"

for _, spec in pairs(constants.recon_specs) do
  local name = "arn_recon-radar-" .. spec.tier

  local item = {
    type = "item",
    name = name,
    icons = helpers.item_icon(helpers.recon_tints[spec.tier]),
    subgroup = item_subgroup,
    order = "d[radar]-b[recon]-" .. spec.tier,
    place_result = name,
    stack_size = 50,
  }

  data:extend({ item })
end
