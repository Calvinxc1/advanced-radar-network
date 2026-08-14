local constants = require("prototypes.radar.constants")
local helpers = require("prototypes.radar.helpers")

for _, spec in pairs(constants.recon_specs) do
  local name = "arn_recon-radar-" .. spec.tier

  local technology = {
    type = "technology",
    name = name,
    localised_name = { "technology-name." .. name },
    localised_description = { "technology-description." .. name },
    icons = helpers.item_icon(helpers.recon_tints[spec.tier]),
    prerequisites = spec.tech.prerequisites,
    effects = {
      { type = "unlock-recipe", recipe = name },
    },
    unit = {
      count = spec.tech.count,
      time = spec.tech.time,
      ingredients = spec.tech.ingredients,
    },
  }

  data:extend({ technology })
end
