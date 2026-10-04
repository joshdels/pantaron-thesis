# AGENTS.md

This repository supports an academic thesis on remotely assessing land and water resources in the Pantaron Range, within the University of Southeastern Philippines (USeP) research context.

## Mission

Develop a feasible, evidence-based land and water resources engineering study using remote sensing, GIS, and available secondary observations. Keep the workspace lightweight and the research traceable.

## Research focus

- Begin with selected catchments associated with Pantaron: terrain and drainage characterization, land-cover mapping, rainfall analysis, and qualified planning implications.
- Treat `docs/research-plan.md` as the working research roadmap. Titles, dates, boundaries, and methods remain proposals until supported and finalized.
- Distinguish mountain-range boundaries from hydrologic catchments. Do not assume Pantaron is one watershed or invent its extent.
- Add advanced modeling only when it serves a specific objective and has adequate data and evaluation evidence.

## Academic writing and USeP alignment

- Write clear, formal academic prose with measurable objectives and consistent terminology.
- Connect the problem, literature gap, objectives, data, methods, results, and conclusions.
- Prefer relevant USeP-authored or USeP-affiliated research where available, supplemented by stronger or necessary Philippine and international primary sources.
- Verify USeP affiliation from the paper or publisher. A paper in a USeP journal is not automatically authored by USeP researchers.
- Do not describe a proposed outline as the official USeP format without verifying a current manual for the student's actual program or college. A curriculum prospectus is not a thesis manual.
- Use future tense for proposed procedures and past tense for completed work. Do not write anticipated outcomes as findings.
- Synthesize literature critically; do not copy a study's methods, weights, accuracy, or conclusions into a different setting without justification.

## Evidence and non-fabrication rules

- Never invent citations, authors, affiliations, DOIs, source contents, numerical results, field observations, institutional requirements, or dataset availability.
- Verify sources through publisher pages, institutional repositories, official agency records, or provider documentation. Search snippets are leads, not sufficient evidence for detailed claims.
- Record what was actually reviewed: metadata, abstract, relevant sections, or full text. Do not imply full-text appraisal when only an abstract was accessible.
- Link factual source-dependent claims to supporting references. Record product versions, periods, units, resolution, and access dates when using data.
- Clearly distinguish verified facts, proposed decisions, assumptions, derived results, and unresolved information.
- Do not claim “no previous research” or “first study” without a defensible search. Describe the specific gap and limits of the review.
- When evidence is unavailable, state what remains unverified and continue work that does not depend on it. Use explicit placeholders rather than invented details.

## Remote assessment standards

- Satellite cover classes are not direct evidence of land ownership, actual land-use practices, or community preferences.
- Rainfall, slope, drainage density, and spectral indices are indicators; they do not by themselves measure usable water supply, groundwater yield, water quality, or erosion rates.
- Keep measured observations, remotely estimated variables, and modeled quantities distinct.
- Document cloud/shadow handling, terrain effects, spatial and temporal compatibility, missing data, parameter choices, and uncertainty.
- Resampling a coarse dataset does not create finer information. Report results at defensible spatial and temporal scales.
- Plan independent reference sampling and accuracy assessment. Keep training and evaluation data separate; disclose limits where field or gauge observations are unavailable.
- Compare derived drainage with reference hydrography and test sensitive processing choices. Preserve complete upstream contributing areas during delineation.
- Avoid causal claims from correlations or map overlays alone. Explain the basis and sensitivity of any screening thresholds or weights.
- Recognize the limits of remote observations for local and Indigenous knowledge. Do not invent community consultation or endorsement.

## Repository structure

- `docs/`: research plan, methods, notes, and chapter drafts
- `literature/`: reference records, critical review notes, and literature matrix
- `scripts/`: traceable processing and analysis scripts
- `outputs/`: actual generated maps, charts, and summary results
- `data/`: datasets added only when needed; preserve originals and document processing
- `reports/`: optional compiled thesis or submission drafts
- `outputs/data/`: generated literature exports and other tabular data products; keep raw downloads and processing notes separate from curated results

## Working principles and workflow

Keep the existing structure. Prefer useful documentation and small scripts over premature scaffolding. Do not create empty chapter files, bulk dataset folders, or a complete modeling system before scope and feasibility are established.

1. Confirm the research question, intended planning use, and study boundary.
2. Review relevant sources and establish a defensible gap.
3. Map each objective to data, methods, outputs, and evaluation evidence.
4. Check data access and run a small pilot.
5. Draft the proposal and incorporate applicable adviser/program requirements.
6. Complete analysis with documented checks and uncertainty.
7. Write results, discussion, and conclusions supported by the outputs.

Prioritize the decisions required by the current research stage. Do not add scope merely because another dataset or technique is available.

## Literature harvesting and scraper rules

- Use documented scholarly APIs or provider export endpoints where possible; do not bypass access controls, CAPTCHAs, robots rules, paywalls, or rate limits.
- Treat harvested metadata as a discovery aid, not as verified evidence. Preserve the query tier and source URL in the user-facing export; provider and record identifiers may remain internal for deduplication and troubleshooting.
- Deduplicate records using DOI first, then normalized title and year. Do not silently overwrite an existing literature matrix.
- Keep the search tiers explicit: Pantaron and nearby local context first, then Philippines, Asia, and global methods. A result's tier is a search strategy label, not proof of geographic relevance.
- Abstracts may be missing or incomplete. Do not infer methods, findings, affiliations, or USeP connection from title keywords alone.
- Generated CSVs belong in `outputs/data/`; scripts and configuration belong in `scripts/`. Record query terms and output filenames in the run log or CSV metadata.
