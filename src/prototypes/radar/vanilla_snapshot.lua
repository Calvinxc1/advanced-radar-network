-- A pristine deepcopy of the vanilla radar entity, captured before
-- observation/entities.lua mutates data.raw.radar["radar"] in place into
-- Observation Radar I. Recon uses this as its graphics/box template so it
-- keeps vanilla's original 3x3 footprint and layered dish+shadow animation
-- instead of inheriting Observation I's 1x1 footprint and placeholder art.
-- require() caches this module, so whichever file requires it first runs
-- this body -- radar.lua requires it before observation, guaranteeing the
-- snapshot happens first.
return util.table.deepcopy(data.raw.radar["radar"])
