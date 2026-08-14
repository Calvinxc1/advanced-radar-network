local function science_pack(name)
  return { name, 1 }
end

-- Observation radar I is the vanilla "radar" entity/item/recipe/technology,
-- mutated in place (see observation/entities.lua etc.) rather than a new
-- prototype, so existing saves transition straight from vanilla radar into
-- it. It still gets the same 1x1 footprint and placeholder art as tiers II
-- and III -- Factorio's next_upgrade chain requires every step to share the
-- same bounding box, so a 3x3 tier I feeding into a 1x1 tier II is invalid.
local observation_specs = {
  {
    tier = 1,
    range = 4,
    energy_usage = "75kW",
    ingredients = {
      { type = "item", name = "iron-plate", amount = 4 },
      { type = "item", name = "copper-cable", amount = 6 },
      { type = "item", name = "electronic-circuit", amount = 2 },
    },
    tech = {
      count = 75,
      time = 20,
      prerequisites = { "automation-science-pack" },
      ingredients = {
        science_pack("automation-science-pack"),
      },
    },
  },
  {
    tier = 2,
    range = 6,
    energy_usage = "300kW",
    ingredients = {
      { type = "item", name = "radar", amount = 1 },
      { type = "item", name = "steel-plate", amount = 8 },
      { type = "item", name = "advanced-circuit", amount = 5 },
      { type = "item", name = "battery", amount = 10 },
    },
    tech = {
      count = 200,
      time = 30,
      prerequisites = { "radar", "chemical-science-pack" },
      ingredients = {
        science_pack("automation-science-pack"),
        science_pack("logistic-science-pack"),
        science_pack("chemical-science-pack"),
      },
    },
  },
  {
    tier = 3,
    range = 10,
    energy_usage = "1MW",
    ingredients = {
      { type = "item", name = "arn_observation-radar-2", amount = 1 },
      { type = "item", name = "processing-unit", amount = 8 },
      { type = "item", name = "low-density-structure", amount = 8 },
      { type = "item", name = "supercapacitor", amount = 4 },
    },
    tech = {
      count = 500,
      time = 45,
      prerequisites = { "arn_observation-radar-2", "electromagnetic-science-pack" },
      ingredients = {
        science_pack("automation-science-pack"),
        science_pack("logistic-science-pack"),
        science_pack("chemical-science-pack"),
        science_pack("utility-science-pack"),
        science_pack("space-science-pack"),
        science_pack("electromagnetic-science-pack"),
      },
    },
  },
}

-- Reconnaissance is a fully independent three-tier line with no tie to the
-- vanilla radar prototype at all; Reconnaissance I is a new prototype here,
-- not a mutation of anything vanilla.
local recon_specs = {
  {
    tier = 1,
    scan_range = 12,
    nearby_range = 2,
    energy_usage = "700kW",
    nearby_scan_energy = "250kJ",
    sector_scan_energy = "3MJ",
    ingredients = {
      { type = "item", name = "radar", amount = 1 },
      { type = "item", name = "steel-plate", amount = 8 },
      { type = "item", name = "advanced-circuit", amount = 5 },
      { type = "item", name = "accumulator", amount = 5 },
    },
    tech = {
      count = 200,
      time = 30,
      prerequisites = { "radar", "chemical-science-pack" },
      ingredients = {
        science_pack("automation-science-pack"),
        science_pack("logistic-science-pack"),
        science_pack("chemical-science-pack"),
      },
    },
  },
  {
    tier = 2,
    scan_range = 24,
    nearby_range = 3,
    energy_usage = "2MW",
    nearby_scan_energy = "250kJ",
    sector_scan_energy = "2MJ",
    ingredients = {
      { type = "item", name = "arn_recon-radar-1", amount = 1 },
      { type = "item", name = "processing-unit", amount = 5 },
      { type = "item", name = "low-density-structure", amount = 5 },
      { type = "item", name = "electric-engine-unit", amount = 5 },
      { type = "item", name = "accumulator", amount = 5 },
    },
    tech = {
      count = 350,
      time = 45,
      prerequisites = { "arn_recon-radar-1", "utility-science-pack", "space-science-pack" },
      ingredients = {
        science_pack("automation-science-pack"),
        science_pack("logistic-science-pack"),
        science_pack("chemical-science-pack"),
        science_pack("utility-science-pack"),
        science_pack("space-science-pack"),
      },
    },
  },
  {
    tier = 3,
    scan_range = 40,
    nearby_range = 5,
    energy_usage = "6MW",
    nearby_scan_energy = "250kJ",
    sector_scan_energy = "1MJ",
    ingredients = {
      { type = "item", name = "arn_recon-radar-2", amount = 1 },
      { type = "item", name = "quantum-processor", amount = 4 },
      { type = "item", name = "supercapacitor", amount = 8 },
      { type = "item", name = "low-density-structure", amount = 12 },
    },
    tech = {
      count = 800,
      time = 60,
      prerequisites = { "arn_recon-radar-2", "cryogenic-science-pack", "quantum-processor" },
      ingredients = {
        science_pack("automation-science-pack"),
        science_pack("logistic-science-pack"),
        science_pack("chemical-science-pack"),
        science_pack("utility-science-pack"),
        science_pack("space-science-pack"),
        science_pack("electromagnetic-science-pack"),
        science_pack("cryogenic-science-pack"),
      },
    },
  },
}

return {
  science_pack = science_pack,
  observation_specs = observation_specs,
  recon_specs = recon_specs,
}
