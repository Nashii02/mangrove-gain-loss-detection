Reference Sources — Mangrove Labeling Guidance
Per thesis: supplemental sources serve as guidance for building the referencedataset, never as error-free baseline truth.

Source	What it provides	Role
2023 Philippine Mangrove Map (Zablan et al., 2024)	PH-specific mangrove extent	Primary anchor for the 2023/2024 labels
Global Mangrove Watch v3.0 (Bunting et al., 2022)	Annual global layers 1996–2020	Anchor for 2019–2020 labels; cross-check
Aringay MENRO records	Locally known planted/cut/restored areas	Ground context; outranks other sources for local knowledge
High-resolution basemap imagery (Google/Bing hybrid)	Current visual texture	Interpreting unclear boundaries; year-consistent support
Identification decision chain (applied per polygon)
Location — inside the intertidal zone (shoreline, river mouths, tidalchannels)? If not → non-mangrove.
Shape/texture — natural irregular boundary, closed canopy? Geometricwater = fishpond → non-mangrove.
Spectral corroboration — false color (B8,B4,B3) red + high stable NDVI +SWIR moisture behavior (B11): mangrove moderate, water/fishponds near-zero.
Reference cross-check — PH Map / GMW agreement.
Still unsure → uncertain list (never guessed); may be excluded from testing.
MENRO validation protocol (label-freeze gate)
Structured review of researcher-prepared masks by MENRO core officers —focused on fragmented stands, narrow coastal strips, mangrove–waterboundaries, transition zones.
Flagged labels → revised by researchers → re-submitted for confirmation.
Confirmed labels retained as final reference masks.
Validation completed before model training.
Labels frozen — no modifications afterward, for any reason (incl. performance).
