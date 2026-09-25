# Research Plan: Remote Assessment of Land and Water Resources in the Pantaron Range

**Status:** proposed research direction; no datasets have been processed and no results are claimed.  
**Source review date:** 25 September 2026.  
**Academic context:** University of Southeastern Philippines (USeP), land and water resources engineering. The student's exact program, campus, adviser requirements, and current thesis manual remain to be confirmed.

## 1. Research direction and academic basis

### Proposed working title

**Remote Sensing and GIS-Based Assessment of Land Cover and Hydroclimatic Characteristics of Selected Catchments in the Pantaron Range, Mindanao, Philippines**

This title makes the proposed measurements explicit. The study will assess land and water resource indicators using satellite observations, elevation data, and existing records. It will initially cover selected catchments associated with the Pantaron Range rather than assume that the entire range is one watershed or has a verified study boundary.

The academic connection is supported by an official USeP Master of Science in Engineering prospectus listing land and water resources engineering and technology, including water resource planning, hydrometeorology, and GIS and remote sensing [S1]. This supports the disciplinary direction; it does not establish the current curriculum or required thesis format.

Two verified USeP-affiliated publications provide useful methodological examples: Cogay et al. (2020) combine GIS and decision criteria for irrigation site suitability [S2]; Auxtero and Villamor (2026) investigate Sentinel-2 image classification in Bohol [S3]. Their study areas, objectives, and results must not be transferred directly to Pantaron.

### Proposed rationale

A catchment-based assessment can organize evidence on land cover, topography, drainage, and rainfall into a common spatial framework for land and water resources planning. The proposed contribution is a reproducible baseline showing the distribution and uncertainty of these indicators within a clearly defined part of Pantaron. Whether this fills an existing research gap must be established through the literature review.

A study in Bendum, within the Pantaron uplands, documents locally varied soil knowledge and conditions [S4]. It provides site-specific context and a reason to avoid treating remotely mapped classes as complete descriptions of soils or community land use. It does not represent the entire range.

**Gap to investigate, not an established claim:** whether existing studies provide a spatially consistent, catchment-level assessment combining land cover, drainage, and rainfall for the selected Pantaron study area and period.

### Main research question

How do land cover, terrain, drainage characteristics, and rainfall vary among selected catchments in the Pantaron Range, and what land and water management concerns can be identified from these indicators and their uncertainties?

### General objective

To assess the spatial distribution of land cover and hydroclimatic characteristics in selected catchments of the Pantaron Range using remote sensing, GIS, and available secondary observations, as a baseline for land and water resources planning.

### Specific objectives and planned evidence

| Specific objective | Proposed analysis | Main outputs | Required checks |
| --- | --- | --- | --- |
| 1. Delineate and characterize selected catchments and their terrain and drainage | Elevation processing, outlet-based catchment delineation, slope and drainage summaries | Study-area map; elevation/slope and drainage maps; catchment statistics | Check outlets and drainage against independent hydrographic references; test sensitivity to stream-extraction thresholds |
| 2. Map land-cover distribution for a selected reference period | Quality-screened satellite composites and a classification approach selected after a pilot | Land-cover map; class area and proportion by catchment | Independent reference samples; confusion matrix; class-level accuracy and area uncertainty |
| 3. Characterize rainfall amount and seasonality over the selected catchments | Area-weighted monthly and annual rainfall summaries for a fixed, complete historical period | Rainfall time series; seasonal summaries; catchment comparison table | Missing-data audit; version consistency; comparison with suitable gauge records if accessible |
| 4. Integrate these indicators to identify areas warranting further land and water management assessment | Transparent comparison of catchments and overlays of relevant indicators | Catchment assessment table; maps of indicator overlap; qualified planning implications | Explain thresholds; assess sensitivity; avoid unsupported composite scores and causal claims |

Land-cover change is an optional extension after one-period mapping works. If retained, revise Objective 2 to include two comparable periods, validate both maps, and quantify change uncertainty. Do not add change detection, erosion modeling, groundwater mapping, and streamflow modeling simultaneously.

## 2. Scope and decisions still required

| Item | Proposed approach or unresolved decision |
| --- | --- |
| Geographic scope | Selected catchments with a documented spatial relationship to Pantaron; exact catchments and outlets to be selected |
| Boundary evidence | Obtain a credible mapped reference for the range and hydrography; record provider, scale, date, and boundary uncertainty |
| Units of analysis | Raster pixels for mapping; catchments for reporting and comparison |
| Land-cover period | Choose after checking usable imagery and reference data; do not select dates solely for a neat interval |
| Rainfall period | Use a sufficiently long, complete period appropriate to the question; exact years to be fixed after availability checks |
| Assessment type | Spatial characterization and screening; no new field campaign assumed |
| Tools | Begin with QGIS and small traceable scripts; use a cloud processing platform only if needed |
| Validation | Independent image interpretation and existing observations where obtainable; explicitly record absence of field validation |
| Academic requirements | Confirm program, current manual, citation style, chapter order, required proposal components, and adviser expectations |
| Schedule | Set target dates after the submission deadline and scope are known |

The mountain-range reference boundary and hydrologic catchments serve different purposes. Delineate complete upstream contributing areas before intersecting them with the range reference; clipping the elevation data to the range first may truncate catchments. Report how much of each catchment intersects the selected Pantaron boundary.

### What the remote assessment will and will not establish

The core study will estimate land-cover classes, terrain derivatives, drainage geometry, and gridded rainfall statistics. These are indicators of resource conditions. The following claims require additional evidence and are outside the initial scope:

- Available water supply, dependable streamflow, or irrigation yield: requires an appropriate hydrologic assessment and supporting observations.
- Groundwater storage, sustainable pumping, or confirmed recharge: cannot be established from a terrain or weighted suitability map alone.
- Potability, pollutant concentration, or compliance with water-quality standards: requires suitable measurements and validated methods.
- Measured soil loss, sediment yield, or flood depths: requires additional models, inputs, and evaluation.
- Land ownership, actual land-use intentions, or community preferences: cannot be inferred from satellite cover classes.

## 3. Chapter 1 — Introduction

### 1.1 Background of the study

Develop a concise narrative from land and water resources planning to the selected Pantaron catchments, then explain the role of remote observations. Support local geographic, environmental, and socioeconomic statements with specific references. Avoid unsupported descriptions such as “severely degraded,” “unexplored,” or “the main water source of Mindanao.”

### 1.2 Statement of the problem

Identify the planning information needed for the selected area, review what existing sources already provide, and explain the remaining limitation. Separate lack of accessible data from proof that no prior study exists.

**Draft to refine after the review:** The proposed study will examine whether available satellite and geospatial datasets can provide a consistent catchment-level baseline of land cover, terrain, drainage, and rainfall for [selected area]. The assessment will evaluate data limitations and identify which planning interpretations are supported by the resulting evidence.

### 1.3 Research question and objectives

Use the question and objectives in Section 1, revising them together whenever scope changes. A descriptive mapping study need not invent a statistical hypothesis. Add testable hypotheses only if the final research design and department require them.

### 1.4 Significance of the study

Explain the potential value of the baseline for watershed assessment, conservation planning, and the identification of locations needing further investigation. Identify actual intended users before claiming institutional demand or endorsement.

### 1.5 Scope and limitations

Specify the boundary, catchments, periods, variables, spatial resolutions, and validation evidence. Discuss clouds, terrain effects, mixed pixels, uncertain reference labels, and the mismatch between fine land-cover imagery and coarse rainfall grids.

### 1.6 Operational definitions

Define land cover, catchment, drainage density, rainfall seasonality, remote assessment, and any management-screening category actually used. Keep mapped land cover distinct from land use.

**Chapter complete when:** the problem is evidence-based, the study area is defensible, and all objectives have feasible data and outputs.

## 4. Chapter 2 — Review of Related Literature and Studies

Synthesize studies by theme rather than arranging unrelated paper summaries.

| Theme | Questions for the review | Starting evidence |
| --- | --- | --- |
| Pantaron and selected catchment context | What local studies and maps exist? What is their geographic coverage? | S4; seek additional primary local studies and agency maps |
| Land-cover mapping in Philippine settings | Which classes are separable? How are clouds, topographic effects, and reference labels handled? | S3 as a USeP-affiliated methodological example; S5 for product documentation |
| Terrain and drainage characterization | How do DEM type, outlet placement, conditioning, and extraction thresholds affect results? | S6 for data properties; obtain additional primary method references before implementation |
| Rainfall characterization | What temporal and spatial scales are appropriate, and what local biases are possible? | S7 and S8 |
| GIS for land and water management | How are indicators selected, combined, and evaluated for a decision? | S2, critically comparing its irrigation-specific purpose with this study |
| Validation and uncertainty | What reference sampling and accuracy measures are appropriate? | Extend the review with primary accuracy-assessment method papers before finalizing the design |

**Proposed conceptual framework:** documented study boundary and source data → preprocessing and quality checks → terrain, land-cover, and rainfall indicators → independent evaluation and sensitivity checks → catchment comparison → qualified management implications.

The framework describes the proposed analytical sequence; it does not establish that land-cover differences caused hydrologic change.

**Chapter complete when:** the research gap is demonstrated, method choices have supporting references, and the relevance and limits of each borrowed approach are explained.

## 5. Chapter 3 — Materials and Methods

### 3.1 Research design

The proposed study will use a quantitative geospatial design based on satellite products and secondary records. It will characterize spatial patterns and compare catchments. Proposal text should use future tense; the completed thesis must describe the actual procedures and deviations.

### 3.2 Candidate datasets

Provider documentation has been located for the products below. Actual coverage, usable observations, and reference-data availability within the final study area have not yet been checked.

| Data | Candidate source and properties | Proposed use | Limitation or decision |
| --- | --- | --- | --- |
| Surface reflectance imagery | Sentinel-2 Level-2A; bands/products at 10, 20, and 60 m [S5] | Land-cover mapping; supporting spectral indices if justified | Select bands and working grid explicitly; resampling does not create finer information |
| Elevation | Copernicus DEM GLO-30, nominal 30 m; a surface model including vegetation and structures [S6] | Terrain, catchments, and drainage | Check surface-model effects, sinks, outlets, and hydrographic consistency |
| Rainfall | CHIRPS v3, 0.05° gridded satellite-and-gauge product with records from 1981 [S7] | Monthly/annual rainfall and seasonality | Fix product version and final-data period; it is not a 10–30 m measurement |
| Study boundary and reference rivers | Suitable agency maps or authoritative geospatial records, to be located | Boundary justification and drainage checks | Do not invent a Pantaron polygon or assume that a map label defines a watershed |
| Independent reference observations | Suitable dated imagery, existing mapped observations, and gauge records, to be located | Classification evaluation and rainfall comparison | Document access, date, uncertainty, and independence from model inputs |

CHIRPS v3 diagnostics include station-density and gap-fill information [S8]. Review these for the study area. If a gauge record contributed to CHIRPS, comparison with that record is not fully independent validation.

### 3.3 Proposed processing sequence

1. **Define the study area.** Document reference boundaries, outlet coordinates, catchment inclusion rules, and the reason for selecting the area. Retain enough surrounding elevation coverage to capture upstream drainage.
2. **Audit the data.** Record provider, product identifier/version, acquisition period, native resolution, coordinate reference system, units, license, missing data, and retrieval date.
3. **Prepare imagery.** Mask invalid observations, clouds, and shadows; inspect terrain-related artifacts; select comparable seasonal windows; record the number of valid observations. Do not classify persistently obscured areas as ordinary land cover.
4. **Derive terrain and drainage.** Select a suitable projected coordinate system for area and length calculations. Document elevation conditioning, flow-routing method, outlet adjustment, and stream threshold. Compare several reasonable thresholds before adopting one.
5. **Map land cover.** Define a modest, distinguishable class scheme after inspection. Pilot a simple supervised classifier, such as random forest, against a simpler baseline if suitable labeled data exist. Keep training, tuning, and evaluation samples separate. Deep learning is not required because a USeP paper used it.
6. **Assess classification accuracy.** Design independent, spatially distributed reference sampling across classes. Document interpretation rules, reference dates, and sample allocation. Report a confusion matrix and producer's/user's accuracy; use an appropriate area-estimation method with uncertainty rather than assuming raw pixel counts are exact. Obtain method references before fixing the sampling design.
7. **Summarize rainfall.** Check complete months and years, compute area-weighted catchment statistics at the native rainfall support, and describe the seasonal cycle from the data. Avoid inventing local wet/dry seasons. Catchments sharing the same few rainfall cells may not support fine spatial comparisons.
8. **Integrate indicators.** Compare class proportions, slope distribution, drainage metrics, and rainfall by catchment. Identify indicator combinations needing further investigation without automatically labeling them degraded, flood-prone, or water-rich.
9. **Evaluate uncertainty.** Report cloud gaps, classification errors, reference uncertainty, DEM sensitivity, rainfall support, and the consequences for management interpretations.
10. **Save reproducible outputs.** Retain source metadata, processing scripts or model settings, tables, map legends, and a brief record of methodological decisions.

### 3.4 Analysis and reporting choices

Use descriptive statistics that answer the objectives before adding significance tests. If inferential tests are introduced, justify the sampling unit and account for spatial dependence rather than treating every neighboring pixel as an independent replicate.

A weighted priority index is optional. Introduce it only after defining the management decision, defending each criterion and weight, and planning sensitivity analysis. The irrigation suitability weights in S2 are not Pantaron watershed weights.

**Chapter complete when:** a pilot produces a checked catchment map, a land-cover output with feasible reference sampling, and a rainfall summary; every retained method has a reference and a documented parameter choice.

## 6. Chapter 4 — Results and Discussion

Draft this chapter's structure now, but insert numerical findings only after analysis.

| Section | Results to present | Discussion to develop |
| --- | --- | --- |
| 4.1 Catchment and terrain characteristics | Boundary, area, elevation, slope, drainage maps and statistics | Meaning of differences; boundary and DEM sensitivity |
| 4.2 Land-cover distribution | Class maps, area estimates, accuracy and uncertainty | Patterns by catchment; comparison with relevant studies; ambiguous classes |
| 4.3 Rainfall characteristics | Annual/monthly summaries and seasonal graphs | Temporal variability; spatial support; agreement with suitable reference records |
| 4.4 Integrated land and water assessment | Catchment comparison and indicator-overlap maps | What warrants further investigation and why; alternative explanations |
| 4.5 Uncertainty and planning implications | Consolidated limitations and robustness checks | Which conclusions remain defensible and which require additional observations |

For each objective, present the result, interpret it, compare it with literature, and state the limit of the interpretation. Report disagreement and weak results as well as strong patterns. If the department requires separate Results and Discussion chapters, split this content without changing the objective-to-evidence links.

**Chapter complete when:** each objective has checked outputs, every numerical claim is traceable, and the discussion does not convert proxies into measured water supply or causal effects.

## 7. Chapter 5 — Conclusions and Recommendations

Conclude in the order of the objectives. Explain what the remote assessment established for the selected catchments and period. Recommend specific follow-up measurements or planning uses only where the findings support them. Keep conclusions within the mapped area; do not generalize selected catchment results to the whole range without justification.

**Chapter complete when:** the main question is answered, no new results appear, and recommendations reflect uncertainty and the scope of the evidence.

Complete the abstract, references, appendices, and required preliminary pages after the main findings stabilize. The chapter arrangement here is a working academic outline, not a verified USeP-wide requirement.

## 8. Verified starting sources and their appropriate use

These are starting references, not a complete RRL. “Verified” means the cited page or document was inspected for the stated information; it does not mean every method has been independently evaluated. Publication details below follow the publisher or institutional document rather than search-engine date labels.

### USeP institutional and research sources

- **S1 — USeP. Undated prospectus.** *Master of Science in Engineering, Major: Land and Water Resources Eng'g and Technology.* [Official prospectus](https://www.usep.edu.ph/coe/wp-content/uploads/sites/4/2022/12/MSE-Prospectus.pdf). Institutional program context only; not a thesis manual or confirmation of the current curriculum.
- **S2 — Cogay, S., Amplayo, I. P., Bayron, R. R., and Cantones, R. V. (2020).** *GIS-Based Land Suitability Analysis for Solar Powered Irrigation System in Non-Irrigated Rice Production Areas of Davao Del Norte.* Southeastern Philippines Journal of Research and Development, 25(1), 47–73. [Publisher record and abstract](https://journal.usep.edu.ph/index.php/Southeastern_Philippines_Journal/article/view/45). DOI: 10.53899/spjrd.v25i1.45. The publisher lists all four authors as USeP-affiliated. Use for a regional GIS decision-analysis example; read the full paper critically before adopting any procedure. Its irrigation suitability findings are not evidence of Pantaron's water availability.
- **S3 — Auxtero, A. M. B., and Villamor, M. M. (2026).** *Deep Learning-Based Methods for Mapping Mangrove Forests in Bohol, Philippines Using Sentinel-2 Imagery.* ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, X-5/W4-2025, 83–89. [Publisher record and abstract](https://isprs-annals.copernicus.org/articles/X-5-W4-2025/83/2026/). DOI: 10.5194/isprs-annals-X-5-W4-2025-83-2026. Both authors list USeP affiliations. Use as an image-mapping example; its mangrove classes and reported performance do not establish accuracy in Pantaron. Full methodological appraisal remains pending.

### Pantaron context and provider documentation

- **S4 — Richelle, L., Visser, M., Bock, L., Walpole, P., Mialhe, F., Colinet, G., and Dendoncker, N. (2018).** *Looking for a dialogue between farmers and scientific soil knowledge: Learnings from an ethno-geomorphopedological study in a Philippine's upland village.* Agroecology and Sustainable Food Systems, 42(1), 2–27. DOI: 10.1080/21683565.2017.1322661. [Institutional full-text copy](https://orbi.uliege.be/bitstream/2268/211801/1/document%281%29.pdf). Abstract and study-area text inspected. Bendum/Pantaron context; not a USeP paper or a range-wide remote assessment.
- **S5 — Copernicus Data Space Ecosystem.** [Sentinel-2 documentation](https://documentation.dataspace.copernicus.eu/Data/SentinelMissions/Sentinel2.html). Product properties for imagery selection and preprocessing.
- **S6 — Copernicus Data Space Ecosystem.** [Copernicus Contributing Missions documentation, DEM section](https://documentation.dataspace.copernicus.eu/Data/Others/CCM.html). Surface-model definition and GLO-30 properties.
- **S7 — Climate Hazards Center, UC Santa Barbara.** [CHIRPS v3 documentation](https://chc.ucsb.edu/data/chirps3). Rainfall product coverage, resolution, and preliminary/final distinctions.
- **S8 — Climate Hazards Center, UC Santa Barbara.** [CHIRPS v3 diagnostics](https://www.chc.ucsb.edu/data/chirps3/diagnostics). Station-density and gap-fill diagnostics for evaluating data support.

**Literature still needed:** authoritative Pantaron boundary/hydrography, studies on the selected catchments, primary terrain-analysis methods, classification sampling and area-accuracy methods, and local rainfall-product evaluation. No claim is made that an equivalent Pantaron study does not exist.

## 9. Completion roadmap

| Stage | Deliverable | Condition for proceeding |
| --- | --- | --- |
| 1. Confirm scope | Selected catchments, boundary sources, revised title and objectives | Geographic relationship to Pantaron and feasibility are defensible |
| 2. Review evidence | Thematic RRL and populated literature matrix | Gap and proposed methods are supported; full texts appraised |
| 3. Test feasibility | Small pilot of terrain, land cover, rainfall, and reference sampling | Essential data and evaluation evidence are usable |
| 4. Prepare proposal | Chapters 1–3 with data inventory and workflow | Adviser feedback and relevant program requirements addressed |
| 5. Complete analysis | Reproducible outputs and uncertainty assessment | All retained objectives have adequate evidence |
| 6. Interpret and write | Results, discussion, conclusions, abstract | Claims match outputs and limitations |
| 7. Revise and submit | Complete manuscript and supporting files | References, figures, review comments, and institutional requirements resolved |

### Immediate tasks

- [ ] Confirm the exact USeP program and obtain its current thesis guidance.
- [ ] Select a defensible catchment study area associated with Pantaron.
- [ ] Read S2 and S3 in full and record their strengths, limitations, and relevance in `literature/literature-matrix.csv`.
- [ ] Find boundary and independent reference data before promising range-wide coverage.
- [ ] Check satellite coverage and rainfall records for the selected area.
- [ ] Run a small pilot before fixing dates, classes, algorithms, or additional models.

Keep planning and chapter drafts in `docs/`, literature notes in `literature/`, processing scripts in `scripts/`, and actual generated maps and tables in `outputs/`. Add datasets only when required. This plan authorizes a research direction; it does not substitute for completed analysis or adviser review.
