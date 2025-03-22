# wblca-benchmark-v2-material-use-intensity
A dataset of material use and embodied carbon intensity for new construction buildings in North America. This dataset and its accompanying publications are the results of joint collaboration between Carbon Leadership Forum (CLF) and Life Cycle Lab (LCL) through their Whole Building Life Cycle Assessment (WBLCA) Benchmarking V2 study in 2025.

## This repository accompanies the research article:  
**"Ashtiani et. al (2025), Material Use and Embodied Carbon Intensity of New Construction Buildings in North America"**.

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Life-Cycle-Lab/wblca-benchmark-v2-material-use-embodied-carbon-intensity.git
cd wblca-benchmark-v2-material-use-embodied-carbon-intensity

python -m venv env
source env/bin/activate  # Linux/macOS
.\env\Scripts\activate   # Windows

pip install -r dashboard/requirements.txt

```


## 📌 Data Glossary

| Used in Analysis | Feature Parametric Name | Feature Name | Description | Units |
| --- | --- | --- | --- | --- |
| Both | project_index | Project Index | Unique project index number. | NA (string) |
| Building Level | site_country | Country | Country where the project is located. | NA (string) |
| Building Level | site_region | Region | Region where the project is located. Based on the 2019 National Ready Mix Concrete Association regions.  | NA (string) |
| Building Level | site_state_province | State/Province | State or province where the project is located.  | NA (string) |
| Building Level | site_clim_zone | Climate Zone | Climate Zone where the project is located per respective energy code of country.  | NA (string) |
| Building Level | bldg_code_year | Building Code Year | Corresponding year of the international building code (IBC) or other equivalent the project complied with. | number |
| Building Level | bldg_energy_code_year | Energy Code Year | Corresponding year of the international energy conservation code (IECC) or other equivalent the project complied with.  | number |
| Building Level | bldg_compl_year | Completion Year | Year of project’s actual construction completion, certificate of occupancy, or anticipated project completion year. | number |
| Building Level | bldg_proj_type | Project Type | Type of construction which details whether the project is new or a type of modification to an existing building. | NA (string) |
| Building Level | bldg_ibc_type | IBC Classification | Type of construction per IBC.  | NA (string) |
| Building Level | bldg_park_type | Parking Type | Type of attached/integrated parking structure or “parkade”.  | NA (string) |
| Building Level | bldg_cfa | Constructed Floor Area (m²) | Total constructed floor area (CFA) which includes the gross internal floor area (GFA) of the building and the gross floor area of any attached/integrated parking components.   | m² |
| Building Level | bldg_gfa | Gross Floor Area (m²) | Total gross internal floor area (GFA) of the building.  | m² |
| Building Level | bldg_park_gfa | Parking Gross Floor Area (m²) | The total horizontal area occupied by any attached/integrated parking components. | m² |
| Building Level | bldg_added_gfa | Added Gross Floor Area (m²) | The total horizontal area where new floor area was added to an existing building (i.e., the floor area of an addition). | m² |
| Building Level | bldg_prim_use_recat | Primary Building Use (Reclassified) | Recategorized primary classification of the building by principal activity where use types with less than 5 samples included in the "other" category. | NA (string) |
| Building Level | bldg_prim_use_original | Primary Building Use (Original) | Primary classification of the building by principal activity  | NA (string) |
| Building Level | bldg_sec_use | Secondary Building Use | Secondary classification of building by principal activity.  | NA (string) |
| Building Level | bldg_occupants | Number of Occupants | Total building occupancy as derived from building code | NA (string) |
| Building Level | bldg_res_units | Number of Residential Units | Total number of residential units in the building | NA (string) |
| Building Level | bldg_stories_above | Stories Above Grade | Binned categorization of the number of stories above finished ground level.  | NA (string) |
| Building Level | bldg_stories_below | Stories Below Grade | Binned categorization of the number of stories below finished ground level.  | NA (string) |
| Building Level | bldg_height | Building Height (m) | Binned categorization of the total height of the building above finished ground level.  | m |
| Building Level | bldg_therm_env_area | Thermal Envelope Area (m²) | Total area of the building’s thermal envelope.   | m² |
| Building Level | bldg_wwr | Window-to-Wall Ratio | The ratio of total vertical fenestration area to total above-grade wall area  | number |
| Building Level | bldg_rval_walls | R-Value of Walls (m²·K/W) | Average nominal R-value of building’s above-grade walls.   | number |
| Building Level | bldg_rval_roofs | R-Value of Roofs (m²·K/W) | Average nominal R-value of building’s roofs.  | number |
| Building Level | str_seis_site_cls | Seismic Site Classification | Classification of the site for seismic design based on its soil and engineering properties.  | NA (string) |
| Building Level | str_sdc | Seismic Design Category | Categorization of required seismic design based on risk category and site location.  | NA (string) |
| Building Level | str_wind_speed | Design Wind Speed (m/s) | Ultimate wind speed used for ultimate wind design based on location.  | m/s |
| Building Level | str_prim_horiz_sys | Primary Horizontal Structural System | Type of primary horizontal gravity system. Structural floor construction system that supports at least ⅔ of the combined floor and roof area of the superstructure. | NA (string) |
| Building Level | str_prim_vert_sys | Primary Vertical Structural System | Type of primary vertical gravity system. System that transfers gravity loads to the foundation of the building.  | NA (string) |
| Building Level | str_lat_sys | Lateral Load Resisting System | Type of lateral system that resists lateral loads of the building.  | NA (string) |
| Building Level | str_podium | Podium Structure | Designation for whether the project is a podium building – a building with two distinct zones with two different structural materials and systems   | NA (string) |
| Building Level | str_sec_horiz_sys | Secondary Horizontal Structural System | The horizontal gravity system (as defined in Primary Horizontal Gravity System) for the podium portion of the building.  | NA (string) |
| Building Level | str_sec_vert_sys | Secondary Vertical Structural System | The vertical gravity system (as defined in Primary Vertical Gravity System) for the podium portion of the building | NA (string) |
| Building Level | str_grid_long | Longitudinal Grid Spacing (m) | Average center to center spacing of longer typical project column grid.  | m |
| Building Level | str_grid_short | Short Grid Spacing (m) | Average center to center spacing of shorter typical project column grid.   | m |
| Building Level | str_fdn_type | Foundation Type | Type of foundation used to support gravity and lateral loads of project. | NA (string) |
| Building Level | str_sys_summary | Structural System Summary | Simplified summary of the buildings primary horizontal, vertical, and lateral system. | NA (string) |
| Building Level | lca_assessment_year | LCA Assessment Year | Year the LCA was performed | number |
| Building Level | lca_design_phase | LCA Design Phase | The design phase of the project when the LCA was performed  | NA (string) |
| Building Level | lca_rsp | Reference Study Period (Years) | Reference study period for the LCA | years |
| Building Level | lca_software | LCA Software Used | Software tool used for the LCA | NA (string) |
| Building Level | lca_purp_of_assessment | Purpose of LCA Assessment | Primary reason the LCA was undertaken. | NA (string) |
| Building Level | lca_phys_scope | Physical Scope of Assessment | The physical scope (building elements) included in the assessment. | NA (string) |
| Building Level | lca_ec_reductions | Embodied Carbon Reductions Implemented | Yes/No designation to indicate if the WBLCA results reflect efforts by the design or construction team to reduce the embodied carbon of the project during design, procurement, and/or construction of the building. | NA (string) |
| Building Level | lca_ec_reduction_percent | Embodied Carbon Reduction Percentage | Approximate percent reduction in embodied carbon of the building compared to a baseline model, if applicable. | number |
| Building Level | total_mass_a1_to_a3 | Total Mass (kg) | Sum of the project's total mass (inv_mass) for life cycle stages A1 to A3. | kg |
| Building Level | total_gwp_a1_to_a3 | Total GWP (kgCO₂e) | Sum of the project's total global warming potential (gwp) for life cycle stages A1 to A3. | kgCO₂e |
| Building Level | total_mui_a1_to_a3 | Total MUI (kg/m²) | Sum of the project's total material use intensity (mui) over life cycle stages A1-A3. | kg/m² |
| Building Level | total_eci_a1_to_a3 | Total ECI (kgCO₂e/m²) | Embodied carbon intensity. Sum of the project's total global warming potential (gwp) for life cycle stages A1-A3 normalized by constructed floor area. | kgCO₂e/m² |
| Material Level | omniclass_element | OmniClass Element Category | Omniclass building element category as designated by the authors | NA (string) |
| Material Level | mat_group | Material Group | The material group as designated by the authors | NA (string) |
| Material Level | mat_type | Material Type | The material type as designated by the authors | NA (string) |
| Material Level | mat_csi_division | CSI Division | The material's CSI MasterFormat division as reported by the LCA tool.  | NA (string) |
| Material Level | tally_revit_building_element | Tally/Revit Building Element | Building element classification as reported by Tally LCA. Similar in intent to omniclass_element | NA (string) |
| Material Level | tally_material_group | Tally Material Group | Material classification as reported by Tally LCA. Similar in intent to mat_group | NA (string) |
| Material Level | oneclick_omniclass | One Click LCA OmniClass Category | Building element classification as reported by One Click LCA. Similar in intent to omniclass_element | NA (string) |
| Material Level | oneclick_resource_type | One Click LCA Resource Type | Material classification as reported by One Click LCA. Similar in intent to mat_group | NA (string) |
| Material Level | life_cycle_stage | Life Cycle Stage | Life cycle stage(s) of the material | NA (string) |
| Material Level | inv_mass | Inventory Mass (kg) | Total mass of the corresponding material and life cycle stage | kg |
| Material Level | gwp | Global Warming Potential (kgCO₂e) | Total global warming potential of the corresponding material and life cycle stage | kgCO₂e |
| Material Level | MUI (kg/m²) | MUI (kg/m²) | Material use intensity (MUI) of the individual material calculated from material’s mass normalized by constructed floor area. | kgCO₂e/m² |
| Material Level | ECI (kgCO₂e/m²) | ECI (kgCO₂e/m²) | Embodied carbon intensity (ECI) of the individual material calculated from material’s embodied carbon normalized by constructed floor area. | kg/m² |
