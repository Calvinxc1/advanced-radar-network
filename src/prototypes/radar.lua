-- Must run before observation, which mutates data.raw.radar["radar"] in
-- place -- see vanilla_snapshot.lua for why.
require("prototypes.radar.vanilla_snapshot")
require("prototypes.radar.observation")
require("prototypes.radar.recon")
