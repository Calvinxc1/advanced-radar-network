local constants = require("prototypes.radar.constants")

for _, spec in pairs(constants.recon_specs) do
  local name = "arn_recon-radar-" .. spec.tier

  local recipe = {
    type = "recipe",
    name = name,
    enabled = false,
    energy_required = 10 + spec.tier * 10,
    ingredients = spec.ingredients,
    results = { { type = "item", name = name, amount = 1 } },
  }

  data:extend({ recipe })
end
