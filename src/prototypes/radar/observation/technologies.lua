local constants = require("prototypes.radar.constants")
local helpers = require("prototypes.radar.helpers")

for _, spec in pairs(constants.observation_specs) do
  local locale_name = "arn_observation-radar-" .. spec.tier

  if spec.tier == 1 then
    -- Observation radar I keeps the vanilla radar technology's
    -- prerequisites, cost, and unlock-recipe effect ("radar") completely
    -- unchanged -- only the localised text changes -- so the tech tree
    -- position new and existing games land on is identical to vanilla.
    local vanilla_radar_technology = data.raw.technology["radar"]
    vanilla_radar_technology.localised_name = { "technology-name." .. locale_name }
    vanilla_radar_technology.localised_description = { "technology-description." .. locale_name }
  else
    local technology = {
      type = "technology",
      name = locale_name,
      localised_name = { "technology-name." .. locale_name },
      localised_description = { "technology-description." .. locale_name },
      icons = helpers.observation_icon(spec.tier),
      prerequisites = spec.tech.prerequisites,
      effects = {
        { type = "unlock-recipe", recipe = locale_name },
      },
      unit = {
        count = spec.tech.count,
        time = spec.tech.time,
        ingredients = spec.tech.ingredients,
      },
    }

    data:extend({ technology })
  end
end
