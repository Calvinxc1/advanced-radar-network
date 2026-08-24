-- One subgroup for the mod's radars, so both ladders occupy a single row of
-- their own: observation tiers first, then reconnaissance tiers.
--
-- Vanilla files radar in `defensive-structure` alongside walls, gates and
-- turrets. Both ladders previously inherited that subgroup by reading it off
-- the vanilla radar at load time, which meant they shared a row with every
-- defensive building -- and that if another mod moved the vanilla radar, both
-- families silently followed it wherever it went.
--
-- The `h-a-*` prefix is reserved for this mod. Vanilla's `defensive-structure`
-- sorts at `h`, so this row sits immediately after it. Advanced Power
-- Infrastructure holds `b-a-*` in production, Advanced Fluid Infrastructure
-- `c-a-*` there and `d-b-*` in logistics, and Advanced Energy Grid `d-a-*` in
-- logistics, so no two mods can interleave their rows.
data:extend({
  {
    type = "item-subgroup",
    name = "arn_radar",
    group = "combat",
    order = "h-a-a",
  },
})
