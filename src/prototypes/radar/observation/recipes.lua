local constants = require("prototypes.radar.constants")

for _, spec in pairs(constants.observation_specs) do
  local locale_name = "arn_observation-radar-" .. spec.tier

  if spec.tier == 1 then
    -- The vanilla radar recipe otherwise falls back to base game's own
    -- "recipe-name.radar" locale entry ("Radar"), which would read oddly
    -- next to the Observation-flavored item/entity/technology text.
    data.raw.recipe["radar"].localised_name = { "recipe-name." .. locale_name }
  else
    local recipe = {
      type = "recipe",
      name = locale_name,
      enabled = false,
      energy_required = 5 + spec.tier * 5,
      ingredients = spec.ingredients,
      results = { { type = "item", name = locale_name, amount = 1 } },
    }

    data:extend({ recipe })
  end
end
