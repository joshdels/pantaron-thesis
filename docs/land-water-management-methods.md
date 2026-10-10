# Evaluation framework for land and water resource management in Pantaron

## Study logic

The study will evaluate three connected evidence layers within selected Pantaron-linked catchments:

1. **Resource condition:** remotely observed land cover, forest configuration, terrain, erosion susceptibility, drainage, rainfall, surface-water occurrence, and selected field observations.
2. **Pressures and risks:** observed land-cover conversion, forest-edge expansion, steep cultivated areas, exposed surfaces, riparian disturbance, rainfall variability, and reported land/water pressures that are verified for the study area.
3. **Management response:** documented protection, restoration, agricultural conservation, riparian management, monitoring, and water-management actions, including their mapped coverage and implementation evidence.

Remote sensing will assess condition and change. It will not by itself establish that a management program caused an observed condition. Management effectiveness will only be evaluated where intervention location, timing, implementation, and an appropriate comparison are available.

## Proposed objectives

1. Delineate and characterize selected management catchments associated with the Pantaron Range.
2. Evaluate land-resource condition using land-cover/forest change, landscape configuration, terrain constraints, riparian condition, and erosion susceptibility.
3. Evaluate water-resource condition using rainfall variability, drainage characteristics, surface-water occurrence, and targeted field measurements where feasible.
4. Inventory and spatially relate documented management interventions and governance arrangements to the measured land and water indicators.
5. Classify management needs—protection, restoration, sustainable land management, monitoring, or additional hydrologic investigation—using transparent rules and sensitivity analysis.

## Method modules

### Boundary and catchment framework

- Verify a Pantaron reference boundary independently of hydrologic catchments.
- Select two to four complete catchments using documented outlets, management relevance, data quality, and field feasibility.
- Retain complete upstream contributing areas and report the fraction intersecting the range reference.

### Land-resource assessment

- Prepare comparable Sentinel-2 Level-2A seasonal composites after cloud, shadow, invalid-pixel, and terrain-effect checks.
- Map a limited class scheme such as closed/open woody vegetation, other natural vegetation, annual/perennial agriculture where separable, built/bare surface, water, and no data.
- Add change analysis only when both periods have comparable observations and independent reference samples.
- Calculate forest-patch area, edge density, core-area or connectivity metrics only where mapped classes and scale support interpretation.
- Combine slope and mapped cover to screen management constraints. Add RUSLE only when locally defensible R, K, LS, C, and P inputs and evaluation evidence are available; otherwise report erosion susceptibility rather than soil-loss rates.
- Evaluate riparian cover within sensitivity-tested buffers around verified streams.

### Water-resource assessment

- Derive catchments and drainage from a conditioned DEM; test outlet placement and stream-extraction thresholds against reference hydrography.
- Summarize CHIRPS v3 rainfall at its native 0.05-degree support: monthly and annual totals, seasonality, anomalies, and dry-spell indicators for a fixed complete period.
- Map surface-water occurrence from an appropriate product or image series only where cloud and mixed-pixel limitations permit.
- If field work is feasible, measure stream width, depth, velocity/discharge and selected water-quality parameters using calibrated instruments and documented QA/QC. A single visit will be treated as a snapshot, not long-term water availability or compliance.

### Management-response assessment

- Review official plans, protected-area or ancestral-domain instruments, agency project records, restoration and monitoring reports, and applicable policies.
- Record intervention type, responsible institution, location, start/end date, intended outcome, implementation evidence, and monitoring indicator.
- Conduct interviews only after program/adviser approval and research-ethics clearance. Separate reported implementation from independently observed condition.
- Evaluate effectiveness only when intervention exposure, timing, outcome indicators, and a defensible comparison exist; otherwise report management coverage and evidence gaps.

### Validation and integration

- Use independent, spatially distributed land-cover reference samples; keep training, tuning, and evaluation samples separate.
- Target field validation toward uncertain classes, riparian condition, erosion indicators, and accessible streams.
- Report confusion matrices, user's/producer's accuracy, area-adjusted estimates where permitted, and confidence intervals.
- Assign management-need classes through explicit decision rules, not undisclosed weights. Test alternative thresholds.

## Primary outputs

- Verified reference-boundary and catchment map.
- Land-cover/forest-condition and optional comparable change maps.
- Terrain, riparian-condition, and erosion-susceptibility maps.
- Rainfall, drainage, and surface-water summaries.
- Field-validation and water-observation register.
- Management-intervention inventory and coverage map.
- Catchment management-needs matrix with evidence strength and uncertainty.
