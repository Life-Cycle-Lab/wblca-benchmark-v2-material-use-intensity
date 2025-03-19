import os
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import base64
import matplotlib.cm as cm

# ✅ Initialize Dash App with Pulse Bootstrap Theme
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.PULSE]  # Apply Pulse theme
)
server = app.server

# # ✅ Define Absolute Paths for Data Files
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
# DATA_DIR = os.path.join(BASE_DIR, "data")
# ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# # ✅ Load Data Files Safely
# wblca_results_path = os.path.join(DATA_DIR, "full_lca_results_02-21-2025_a1_to_a3.csv")
# wblca_meta_data_path = os.path.join(DATA_DIR, "buildings_metadata_02-21-2025_a1_to_a3_new_construction.xlsx")

# # ✅ Ensure Files Exist Before Loading
# if os.path.exists(wblca_results_path):
#     wblca_results_full = pd.read_csv(wblca_results_path, na_values=["NA", "NULL"])
# else:
#     raise FileNotFoundError(f"Missing file: {wblca_results_path}")

# if os.path.exists(wblca_meta_data_path):
#     wblca_meta_data = pd.read_excel(wblca_meta_data_path, na_values=["NA", "NULL"])
# else:
#     raise FileNotFoundError(f"Missing file: {wblca_meta_data_path}")

# # Ensure 'Project Index' is a string for merging
# wblca_results_full['Project Index'] = wblca_results_full['Project Index'].astype(str)
# wblca_meta_data['Project Index'] = wblca_meta_data['Project Index'].astype(str)

# # **Force conversion of specific columns to numeric**
# numeric_cols = ["Inventory Mass (kg)", "Global Warming Potential (kgCO₂e)"]
# for col in numeric_cols:
#     wblca_results_full[col] = pd.to_numeric(wblca_results_full[col], errors='coerce')

# # Perform a left join on 'Project Index'
# merged_df = pd.merge(wblca_results_full, wblca_meta_data, on="Project Index", how="left")

# # Compute derived columns safely
# merged_df['MUI (kg/m²)'] = np.where(
#     merged_df['Constructed Floor Area (m²)'] != 0, merged_df['Inventory Mass (kg)'] / merged_df['Constructed Floor Area (m²)'], np.nan)

# merged_df['ECI (kgCO₂e/m²)'] = np.where(
#     merged_df['Constructed Floor Area (m²)'] != 0, merged_df['Global Warming Potential (kgCO₂e)'] / merged_df['Constructed Floor Area (m²)'], np.nan)



# # Rename some feature names:
# wblca_meta_data.rename(columns={
#     'total_mass_a1_to_a3': 'Total Mass (kg)',
#     'total_gwp_a1_to_a3': 'Total GWP (kgCO₂e)',
#     'total_mui_a1_to_a3': 'Total MUI (kg/m²)',
#     'total_eci_a1_to_a3': 'Total ECI (kgCO₂e/m²)',
# }, inplace=True)


# ✅ Define Absolute Paths for Data Files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# ✅ Load Data Files Safely
merged_df_path = os.path.join(DATA_DIR, "merged_df.parquet")
wblca_meta_data_path = os.path.join(DATA_DIR, "buildings_metadata_02-21-2025_a1_to_a3_new_construction.xlsx")

# ✅ Ensure Files Exist Before Loading
if os.path.exists(merged_df_path):
    merged_df = pd.read_parquet(merged_df_path)
    merged_df.replace(["NA", "NULL"], np.nan, inplace=True)
else:
    raise FileNotFoundError(f"Missing file: {merged_df_path}")

if os.path.exists(wblca_meta_data_path):
    wblca_meta_data = pd.read_excel(wblca_meta_data_path, na_values=["NA", "NULL"])
else:
    raise FileNotFoundError(f"Missing file: {wblca_meta_data_path}")

# Ensure 'Project Index' is a string for merging
merged_df['Project Index'] = merged_df['Project Index'].astype(str)
wblca_meta_data['Project Index'] = wblca_meta_data['Project Index'].astype(str)

# **Force conversion of specific columns to numeric**
numeric_cols = ["Inventory Mass (kg)", "Global Warming Potential (kgCO₂e)"]
for col in numeric_cols:
    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

# Restrict numerical options in the material-level analysis to specific values
material_numerical_options = [
    {"label": "Material Use Intensity", "value": "MUI (kg/m²)"},
    {"label": "Embodied Carbon Intensity", "value": "ECI (kgCO₂e/m²)"}
]

categorical_options = [
    {'label': col, 'value': col} 
    for col in merged_df.select_dtypes(include=['object', 'category']).columns
]

numerical_options = [
    {'label': col, 'value': col} 
    for col in merged_df.select_dtypes(include=['float64', 'int64', 'int32', 'float32']).columns
]

# ✅ Encode Image
def encode_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"
    return None  # Avoid errors if file is missing

image_src = encode_image(os.path.join(ASSETS_DIR, "lcl-header.png"))

# ✅ Load Data Glossary
glossary_path = os.path.join(ASSETS_DIR, "data_glossary.xlsx")
if os.path.exists(glossary_path):
    df_glossary = pd.read_excel(glossary_path)
else:
    df_glossary = pd.DataFrame()  # Avoid errors if missing


# ✅ Define Layout with Bootstrap Components
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(
            src=image_src,
            className="img-fluid mb-3"
        ), width=12)
    ]),

    dbc.Row([
        dbc.Col(html.H1(
            "Embodied Carbon and Material Use Intensity Visualizer",
            className="text-center text-primary mt-3 mb-3",
            style={"fontSize": "30px"}  # ✅ Reduce font size
        ), width=12)
    ]),

    # ✅ Add dcc.Store to store selections across tabs
    dcc.Store(id="material-level-selections"),
    dcc.Store(id="building-level-selections"),
    dcc.Store(id="material-graph-data"),
    dcc.Store(id="building-graph-data"),

    # ✅ Tab Navigation using dbc.Nav

    dbc.Tabs(
        [
            dbc.Tab(label="Introduction", tab_id="instructions",
                    tab_style={"width": "25%", "textAlign": "center"},
                    active_tab_style={"fontWeight": "bold", "textAlign": "center"}),

            dbc.Tab(label="Data Glossary", tab_id="glossary",
                    tab_style={"width": "25%", "textAlign": "center"},
                    active_tab_style={"fontWeight": "bold", "textAlign": "center"}),

            dbc.Tab(label="Material Level Analysis", tab_id="material_analysis",
                    tab_style={"width": "25%", "textAlign": "center"},
                    active_tab_style={"fontWeight": "bold", "textAlign": "center"}),

            dbc.Tab(label="Building Level Analysis", tab_id="building_analysis",
                    tab_style={"width": "25%", "textAlign": "center"},
                    active_tab_style={"fontWeight": "bold", "textAlign": "center"}),
        ],
        id="tabs",
        active_tab="instructions",
        className="mb-3",
        style={"width": "100%"}
    ),

    # ✅ Tab Content
    dbc.Container(id="tab-content", className="p-4 w-100", fluid=True)
], fluid=True)

# ✅ Callback to switch tab content
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    State("material-level-selections", "data"),
    State("material-graph-data", "data"),
)
def render_tab_content(tab, stored_selections, stored_graph):
    if tab == "instructions":
        return dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.P([
                            "This dashboard is developed as part of the ",
                            html.A("Carbon Leadership Forum (CLF)", href="https://www.carbonleadershipforum.org", target="_blank", className="text-primary"),
                            "'s WBLCA Benchmarking Study V2 in collaboration with the ",
                            html.A("Life Cycle Lab", href="https://www.lifecyclelab.org", target="_blank", className="text-primary"),
                            " at the University of Washington, designed primarily for the visualization of Material Use Intensity and Embodied Carbon Intensity. It serves as an interactive platform to explore the environmental impacts of building materials and construction practices. Detailed information on the data sources, methodologies, metadata can be found under references below."
                        ], className="text-justify"),
                        
                        html.H4("Purpose of the Tool:", className="mt-4", style={"fontSize": "18px"}),
                        html.Ul([
                            html.Li("Material Use Intensity (MUI) and Embodied Carbon Intensity (ECI) visualizations for a variety of data grouping options from building characteristics to material categories."),
                            html.Li("Enable dynamic visualization of data (as opposed to static graphics often published in journal articles), according to the methodological framework developed in the referenced journal article."),
                        ]),
                        
                        html.H4("Navigation Overview:", className="mt-4", style={"fontSize": "18px"}),
                        html.Ul([
                            html.Li("'Data Glossary': Contains a list and description of possible selections for numerical and categorical features contained in the background data in use of this dashboard."),
                            html.Li("'Material Level Analysis': Allows detailed examination of material-specific data through filters, aggregation methods, and custom visualizations."),
                            html.Li("'Building Level Analysis': Focuses on building-level data, offering insights through comparisons and analyses of different building characteristics."),
                        ]),
                        
                        html.H4("Using the Dashboard:", className="mt-4", style={"fontSize": "18px"}),
                        html.Ul([
                            html.Li("Select Features: As a minimum, select a metric (i.e., numerical feature) and a category (i.e., categorical feature) to start visualizations."),
                            html.Li("Customize Outputs: Tailor visual outputs through the selection of a stacking feature (i.e., secondary categorical feature), data aggregation methods, graph dimensions, etc."),
                            html.Li("Export Graphs: Download graphs for offline use and further analysis."),
                        ]),
                        
                        html.H4("Scope of Analysis:", className="mt-4", style={"fontSize": "18px"}),
                        html.Ul([
                            html.Li("Life Cycle Assessment (LCA) scope is limited to cradle to gate impacts (A1 to A3)."),
                            html.Li("Building projects are limited to 'new construction' in North America."),
                            html.Li("Mechanical, electrical, and plumbing [MEP], sitework, and furniture, fixtures, and equipment [FF&E] are not covered."),
                            html.Li("Physical scope of buildings included are substructures (B), superstructures (S), enclosures (E), interior constructions (C), and interior finishes (F)."),
                        ]),
                        
                        html.H4("Resources:", className="mt-4", style={"fontSize": "18px"}),
                        html.Ul([
                            html.Li("Ashtiani et al. Material Use and Embodied Carbon Intensity of New Construction Buildings in North America. (Pre-print)"),
                            html.Li(html.A("CLF's WBLCA Benchmark Study v2", 
                                        href="https://carbonleadershipforum.org/clf-wblca-v2/", 
                                        target="_blank", 
                                        className="text-primary")),

                            html.Li(html.A("Benke et al. A Harmonized Dataset of High-resolution Whole Building Life Cycle Assessment Results in North America. (Pre-print)", 
                                        href="https://www.researchsquare.com/article/rs-6108016/v1", 
                                        target="_blank", 
                                        className="text-primary")),

                            html.Li(html.A("Benke et al. A Harmonized Dataset of High-resolution Whole Building Life Cycle Assessment Results in North America: Data only - First Public Release.", 
                                        href="https://figshare.com/articles/dataset/A_Harmonized_Dataset_of_High-Resolution_Whole_Building_Life_Cycle_Assessment_Results_in_North_America_i_Data_only_-_i_i_First_Public_Release_i_/28462145/1", 
                                        target="_blank", 
                                        className="text-primary")),
                        ]),
                        html.Br(),

                        
                        html.P("For questions, contact ashtiani@uw.edu. Enjoy exploring!", className="text-center mt-3"),
                        html.P([
                            "(",
                            html.A("CC BY 4.0", href="http://creativecommons.org/licenses/by/4.0/", className="text-primary"),
                            ") Life Cycle Lab 2025"
                        ], className="text-center text-muted mt-3"),
                    ])
                ], className="shadow-sm border-0 p-4"))
            ])
        ], fluid=True)

    elif tab == "glossary":
        # Define specific widths for each column based on typical content length
        column_styles = [
            {'if': {'column_id': df_glossary.columns[0]}, 'minWidth': '50px', 'width': '60px', 'maxWidth': '80px'},  # Adjusted for minimal content
            {'if': {'column_id': df_glossary.columns[1]}, 'minWidth': '50px', 'width': '150px', 'maxWidth': '100px'},  # Slightly wider
            {'if': {'column_id': df_glossary.columns[2]}, 'minWidth': '50px', 'width': '200px', 'maxWidth': '100px'},  # Medium-sized text
            {'if': {'column_id': df_glossary.columns[3]}, 'minWidth': '50px', 'width': '350px', 'maxWidth': '400px'},  # Description column
            {'if': {'column_id': df_glossary.columns[4]}, 'minWidth': '50px', 'width': '75px', 'maxWidth': '100px'}  # Units column
        ]

        return dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Data Glossary", className="bg-primary text-white", style={"display": "flex", "justifyContent": "center", "alignItems": "center"}),
                    dbc.CardBody([
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": col, "id": col} for col in df_glossary.columns],
                            data=df_glossary.to_dict('records'),

                            # ✅ Keep text aligned properly with proper font size
                            style_cell={
                                'textAlign': 'left',
                                'padding': '5px',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                'fontSize': '12px'  # ✅ Ensures smaller font
                            },

                            # ✅ Keep the table scrollable if needed
                            style_table={
                                'overflowX': 'auto',
                                'width': '100%',
                                'minWidth': '100%',
                            },

                            # ✅ Keep headers styled properly
                            style_header={
                                'backgroundColor': '#f8f9fa',
                                'fontWeight': 'bold',
                                'fontSize': '14px'
                            },

                            # ✅ Ensure proper row styling
                            style_data_conditional=[
                                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                            ],

                            # ✅ Maintain column-specific widths
                            style_cell_conditional=column_styles,
                            
                            fill_width=True
                        )
                    ])
                ], className="shadow-sm border-0 p-4"))
            ])
        ], fluid=True)

    elif tab == "material_analysis":
        return dbc.Container([
            dbc.Row([
                # Left Section: Controls (Dropdowns & Inputs)
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Material Analysis Controls", className="bg-primary text-white"),
                        dbc.CardBody([
                            # ✅ Select Metrics
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Select Metrics (Required):", className="fw-bold"),
                                    dcc.Dropdown(
                                        id='numerical_feature_dropdown',
                                        options=material_numerical_options,
                                        value=(stored_selections or {}).get("material_numerical_options", None),
                                        placeholder="Select a feature...",
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            # ✅ Select Categories
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Select Categories (Required):", className="fw-bold"),
                                    dcc.Dropdown(
                                        id='primary_categorical_feature_dropdown',
                                        options=categorical_options,
                                        value=(stored_selections or {}).get("primary_categorical_feature", None),
                                        placeholder="Select a feature...",
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            html.Hr(),

                            # ✅ Add Stacks (Optional)
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Add Stacks (Optional):", className="fw-bold"),
                                    dcc.Dropdown(
                                        id='secondary_categorical_feature_dropdown',
                                        options=[{'label': 'None', 'value': ''}] + categorical_options,
                                        value=(stored_selections or {}).get("secondary_categorical_feature", None),
                                        placeholder="Select a feature...",
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            # ✅ Filtering Area
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Add Data Filters (Optional):", className="fw-bold"),
                                    dcc.Dropdown(
                                        id="filter-categorical-features-material",
                                        options=[{"label": col, "value": col} for col in merged_df.select_dtypes(include=["object", "category"]).columns],
                                        placeholder="Select a feature...",
                                        multi=True,
                                        persistence=True,
                                        persistence_type="session",
                                    ),
                                    html.Div(id="filter-values-container-material", className="mt-2"),
                                ], width=12)
                            ], className="mb-2"),

                            html.Hr(),

                            # ✅ Aggregation Method
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Aggregation Method:"),
                                    dbc.RadioItems(
                                        id="aggregation-method-material",
                                        options=[
                                            {"label": " Mean", "value": "mean"},
                                            {"label": " Median", "value": "median"},
                                        ],
                                        value="mean",
                                        inline=False,
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            # ✅ Replace Missing Data with Zero
                            dbc.Row([
                                dbc.Col([
                                    dbc.Checkbox(
                                        id="impute-zeros-checkbox",
                                        label="Replace Missing Data with Zero",
                                        persistence=True,
                                        persistence_type="session",
                                        value=False,
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            html.Hr(),

                            # ✅ Logarithmic Y-Axis
                            dbc.Row([
                                dbc.Col([
                                    dbc.Checkbox(
                                        id="log_y_axis",
                                        label="Logarithmic Y-Axis",
                                        persistence=True,
                                        persistence_type="session",
                                        value=False,
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            # ✅ 100% Stacked Bar Chart
                            dbc.Row([
                                dbc.Col([
                                    dbc.Checkbox(
                                        id="stacked_100_percent",
                                        label="100% Stacked Bar Chart",
                                        persistence=True,
                                        persistence_type="session",
                                        value=False,
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            # ✅ Graph Dimensions
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Graph Dimensions:"),
                                ], width=12)
                            ], className="mb-2"),

                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Width", className="mb-1"),
                                    dbc.Input(
                                        id="graph_width",
                                        type="number",
                                        placeholder="e.g., 800",
                                        step=50,
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=6),

                                dbc.Col([
                                    dbc.Label("Height", className="mb-1"),
                                    dbc.Input(
                                        id="graph_height",
                                        type="number",
                                        placeholder="e.g., 600",
                                        step=50,
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=6)
                            ], className="mb-2"),
                        ], style={"padding": "5px", "margin": "0px"})
                    ], className="shadow-sm border-0 mb-3")
                ], width=4),

                # Right Section: Graph Output
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Visualization", 
                                       className="bg-primary text-white", 
                                       style={"display": "flex", "justifyContent": "center", "alignItems": "center"}),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        id='visualization',
                                        config={
                                            'toImageButtonOptions': {
                                                'format': 'png',
                                                'filename': 'stacked_bar_plot',
                                                'height': 600,
                                                'width': 800,
                                                'scale': 3
                                            }
                                        },
                                        figure=go.Figure(**stored_graph) if stored_graph and "data" in stored_graph else go.Figure(),
                                        style={"margin": "auto"}  # Ensures centering
                                    )
                                ], width=10, className="d-flex justify-content-center")
                            ], justify="center")
                        ])
                    ], className="shadow-sm border-0 w-100")
                ], width=8),
            ])
        ], fluid=True)

    elif tab == "building_analysis":
        return dbc.Container([
            dbc.Row([
                # Left Section: Controls (Dropdowns & Inputs)
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Building Analysis Controls", className="bg-primary text-white"),
                        dbc.CardBody([
                            # Select Metrics
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Select Metrics (Required):", className="fw-bold"),
                                    dcc.Dropdown(
                                        id="numerical-variable",
                                        options=[
                                            {"label": col, "value": col}
                                            for col in wblca_meta_data.select_dtypes(include=["number"]).columns
                                        ],
                                        placeholder="Select a feature...",
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            # Select Categories
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Select Categories (Required):", className="fw-bold"),
                                    dcc.Dropdown(
                                        id="categorical-variable",
                                        options=[
                                            {"label": col, "value": col}
                                            for col in wblca_meta_data.select_dtypes(include=["object", "category"]).columns
                                        ],
                                        placeholder="Select a feature...",
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            html.Hr(),

                            # Add Stacks (Optional)
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Add Stacks (Optional):", className="fw-bold"),
                                    dcc.Dropdown(
                                        id="stacking-variable",
                                        options=[
                                            {"label": col, "value": col}
                                            for col in wblca_meta_data.select_dtypes(include=["object", "category"]).columns
                                        ],
                                        placeholder="Select a feature...",
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            # Filtering Area
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Add Data Filters (Optional):", className="fw-bold"),
                                    dcc.Dropdown(
                                        id="filter-categorical-features",
                                        options=[
                                            {"label": col, "value": col}
                                            for col in wblca_meta_data.select_dtypes(include=["object", "category"]).columns
                                        ],
                                        placeholder="Select a feature...",
                                        persistence=True,
                                        persistence_type="session",
                                        multi=True,
                                    ),
                                    html.Div(id="filter-values-container", className="mt-2"),
                                ], width=12)
                            ], className="mb-2"),

                            html.Hr(),

                            # Aggregation Method
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Aggregation Method:"),
                                    dbc.RadioItems(
                                        id="aggregation-method",
                                        options=[
                                            {"label": " Sum", "value": "sum"},
                                            {"label": " Mean", "value": "mean"},
                                            {"label": " Median", "value": "median"},
                                            {"label": " Count", "value": "count"},
                                        ],
                                        value="mean",
                                        inline=False,
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            # Show Error Bars
                            dbc.Row([
                                dbc.Col([
                                    dbc.Checkbox(
                                        id="show-error-bars",
                                        label="Show Error Bars (quartiles)",
                                        value=False,
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            html.Hr(),

                            # Graph Orientation
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Chart Orientation:"),
                                    dbc.RadioItems(
                                        id="graph-orientation",
                                        options=[
                                            {"label": " Vertical", "value": "v"},
                                            {"label": " Horizontal", "value": "h"},
                                        ],
                                        value="v",
                                        inline=False,
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=12)
                            ], className="mb-2"),

                            # Graph Dimensions
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Graph Dimensions:"),
                                ], width=12)
                            ], className="mb-2"),

                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Width", className="mb-1"),
                                    dbc.Input(
                                        id="graph-width",
                                        type="number",
                                        placeholder="e.g., 800",
                                        step=50,
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=6),

                                dbc.Col([
                                    dbc.Label("Height", className="mb-1"),
                                    dbc.Input(
                                        id="graph-height",
                                        type="number",
                                        placeholder="e.g., 600",
                                        step=50,
                                        persistence=True,
                                        persistence_type="session",
                                    )
                                ], width=6)
                            ], className="mb-2"),
                        ], style={"padding": "5px", "margin": "0px"})
                    ], className="shadow-sm border-0 mb-3")
                ], width=4),

                # Right Section: Graph Output
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Visualization", 
                                       className="bg-primary text-white", 
                                       style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
                                       ),
                        dbc.CardBody([
                            dbc.Row(
                                dbc.Col(
                                    dcc.Graph(
                                        id="bar-chart",
                                        config={
                                            'toImageButtonOptions': {
                                                'format': 'png',
                                                'filename': 'stacked_bar_plot',
                                                'height': 600,
                                                'width': 800,
                                                'scale': 3
                                            }
                                        }
                                    ),
                                    width="auto",
                                    className="d-flex justify-content-center"
                                ),
                                justify="center"
                            )
                        ])
                    ], className="shadow-sm border-0")
                ], width=8),
            ])
        ], fluid=True)

# ################# Material Level Callbacks ########################
@app.callback(
    Output("filter-values-container-material", "children"),
    Input("filter-categorical-features-material", "value"),
    State("material-level-selections", "data")  # ✅ Use stored selections
)
def update_filter_values_dropdowns_material(selected_features, stored_selections):
    if not selected_features:
        return []

    stored_selections = stored_selections or {}  # Ensure it's not None

    dropdowns = []
    for feature in selected_features:
        dropdowns.append(
            dbc.Col([
                dbc.Label(f"Filter {feature}:", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id={"type": "filter-value-material", "feature": feature},
                    options=[{"label": val, "value": val} for val in merged_df[feature].dropna().unique()],
                    placeholder=f"Select values for {feature}",
                    multi=True,
                    value=stored_selections.get(feature, None),  # ✅ Restore stored selection
                    persistence=True,
                    persistence_type="session",
                ),
            ], width=6)
        )
    return dbc.Row(dropdowns, className="g-2")  # Apply Bootstrap row layout


@app.callback(
    [
        Output('visualization', 'figure'),
        Output("material-level-selections", "data"),
        Output("material-graph-data", "data"),
    ],
    [
        Input('secondary_categorical_feature_dropdown', 'value'),
        Input('primary_categorical_feature_dropdown', 'value'),
        Input('numerical_feature_dropdown', 'value'),
        Input('graph_width', 'value'),
        Input('graph_height', 'value'),
        Input('log_y_axis', 'value'),
        Input('stacked_100_percent', 'value'),
        Input('aggregation-method-material', "value"),
        Input({"type": "filter-value-material", "feature": dash.ALL}, "value"),
        Input("impute-zeros-checkbox", "value"),
    ],
    [State("filter-categorical-features-material", "value")],
)
def process_data(
    secondary_categorical_feature, primary_categorical_feature, numerical_feature,
    graph_width, graph_height, log_y_axis, stacked_100_percent,
    aggregation_method_material,
    filter_values, impute_zeros,
    filter_features
):

    # ✅ Handle empty selections
    if not primary_categorical_feature or not numerical_feature:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Please select features",
            xaxis_title="",
            yaxis_title="",
            plot_bgcolor="white",
            paper_bgcolor="white",
            width=graph_width if graph_width else 800,
            height=graph_height if graph_height else 600,
            font=dict(family="Open Sans", size=12),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )
        return empty_fig, {}, empty_fig.to_dict()

    filtered_df = merged_df.copy()

    # ✅ Apply filters efficiently
    if filter_features and filter_values:
        for feature, values in zip(filter_features, filter_values):
            if values:
                filtered_df = filtered_df[filtered_df[feature].isin(values)]

    # ✅ Initialize annotation text
    annotation_text = None  

    # ✅ Check conditions only if impute_zeros is NOT selected
    if not impute_zeros and primary_categorical_feature and secondary_categorical_feature:
        if (primary_categorical_feature not in wblca_meta_data.columns) and (secondary_categorical_feature not in wblca_meta_data.columns):
            # Count unique mappings between primary and secondary features
            primary_to_secondary_count = filtered_df.groupby(primary_categorical_feature)[secondary_categorical_feature].nunique()
            secondary_to_primary_count = filtered_df.groupby(secondary_categorical_feature)[primary_categorical_feature].nunique()

            # Validate uniqueness across mappings
            primary_unique_mapping = primary_to_secondary_count.eq(1).all()
            secondary_unique_mapping = secondary_to_primary_count.eq(1).all()

            # If both mappings are NOT unique, set annotation text
            if not primary_unique_mapping and not secondary_unique_mapping:
                annotation_text = "<b>Use Replacement with Zero</b>"

    # ✅ Ensure impute_zeros is a boolean
    impute_zeros = bool(impute_zeros)  

    if impute_zeros:
        # ✅ Identify primary category sources
        if primary_categorical_feature in wblca_meta_data.columns:
            project_primary_df = wblca_meta_data[['Project Index', primary_categorical_feature]].drop_duplicates()
        else:
            project_primary_df = filtered_df[['Project Index', primary_categorical_feature]].drop_duplicates()

        # ✅ Handle imputation for secondary_categorical_feature
        if secondary_categorical_feature:
            unique_secondary_cat = filtered_df[secondary_categorical_feature].dropna().unique()

            # Generate Cartesian product of projects, secondary categories, and primary categories
            full_imputed_df = (
                pd.merge(
                    pd.merge(
                        pd.DataFrame({'Project Index': filtered_df['Project Index'].unique()}),
                        pd.DataFrame({secondary_categorical_feature: unique_secondary_cat}),
                        how='cross'
                    ),
                    project_primary_df,
                    on='Project Index',
                    how='inner'
                )
            )

            # Aggregate data at Project-Primary-Secondary category level
            agg_df = filtered_df.groupby(
                ['Project Index', primary_categorical_feature, secondary_categorical_feature], as_index=False
            )[numerical_feature].sum()

            # Merge and fill missing values with zero
            data_for_aggregation = full_imputed_df.merge(
                agg_df,
                on=['Project Index', primary_categorical_feature, secondary_categorical_feature],
                how='left'
            ).fillna({numerical_feature: 0})

        else:  # ✅ Handle imputation when only primary_categorical_feature is selected
            unique_projects = filtered_df['Project Index'].unique()
            unique_primary_categories = filtered_df[primary_categorical_feature].dropna().unique()

            # Generate Cartesian product for zero imputation
            full_imputed_df = pd.merge(
                pd.DataFrame({'Project Index': unique_projects}),
                pd.DataFrame({primary_categorical_feature: unique_primary_categories}),
                how='cross'  # Ensures all project-category combinations
            )

            # Aggregate data at Project-Primary category level
            agg_df = filtered_df.groupby(
                ['Project Index', primary_categorical_feature], as_index=False
            )[numerical_feature].sum()

            # Merge and fill missing values with zero
            data_for_aggregation = full_imputed_df.merge(
                agg_df,
                on=['Project Index', primary_categorical_feature],
                how='left'
            ).fillna({numerical_feature: 0})

        # ✅ Detect zero-imputation percentage
        total_count = filtered_df.shape[0]
        zero_count = (filtered_df[numerical_feature] == 0).sum()
        zero_percentage = (zero_count / total_count) * 100

        high_imputation = zero_percentage > 10  # Flag if over 10% of values are zero-imputed

    else:
        # ✅ No imputation, use the filtered dataframe directly
        data_for_aggregation = filtered_df.copy()

    # ✅ Handle aggregation and visualization clearly based on imputation checkbox
    if impute_zeros:
        # ✅ Aggregate data based on primary and optional secondary category
        if secondary_categorical_feature:
            agg_df = data_for_aggregation.groupby(
                [primary_categorical_feature, secondary_categorical_feature],
                as_index=False
            )[numerical_feature].agg(aggregation_method_material).rename(columns={numerical_feature: 'aggregated_value'})
        else:
            agg_df = data_for_aggregation.groupby(
                primary_categorical_feature,
                as_index=False
            )[numerical_feature].agg(aggregation_method_material).rename(columns={numerical_feature: 'aggregated_value'})

        # ✅ Normalize for 100% stacking if selected
        if stacked_100_percent:
            agg_df['aggregated_value'] /= agg_df.groupby(primary_categorical_feature)['aggregated_value'].transform('sum')
            y_label = "Percentage Contribution (%)"
        else:
            y_label = numerical_feature

        # ✅ Detect zero-imputation percentage
        total_count = data_for_aggregation.shape[0]
        zero_count = (data_for_aggregation[numerical_feature] == 0).sum()
        zero_percentage = (zero_count / total_count) * 100
        high_imputation = zero_percentage > 60  # Flag if zero-imputation is too high

        # ✅ Ensure consistent category ordering
        category_order_agg = sorted(data_for_aggregation[primary_categorical_feature].dropna().unique())

        # ✅ Create Stacked Bar Chart
        fig = px.bar(
            agg_df,
            x=primary_categorical_feature,
            y='aggregated_value',
            color=secondary_categorical_feature,
            barmode="relative" if stacked_100_percent else "stack",
            labels={"aggregated_value": y_label},
            title=f"Stacked Bar Plot of {secondary_categorical_feature or numerical_feature} by {primary_categorical_feature} ({aggregation_method_material.capitalize()}) [Imputed]",
            color_discrete_sequence=px.colors.qualitative.Vivid,
            category_orders={primary_categorical_feature: category_order_agg}
        )

        # ✅ Reverse legend order for better readability
        fig.data = fig.data[::-1]

        # ✅ Update Layout with Bootstrap Styling Considerations
        fig.update_layout(
            font=dict(family="Open Sans", size=12),
            plot_bgcolor="white",
            paper_bgcolor="white",
            width=graph_width if graph_width else 800,
            height=graph_height if graph_height else 600,
            margin=dict(l=40, r=40, t=60, b=40),
            legend_traceorder="reversed",
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                gridwidth=0.5,
                type="log" if log_y_axis and not stacked_100_percent else "linear",
                tickformat=".0%" if stacked_100_percent else None,
                range=[0, 1] if stacked_100_percent else None  # ✅ Ensures 0-100% range for stacked mode
            )
        )

        # ✅ Conditionally Add Annotation for Missing Data Handling
        if annotation_text:
            fig.add_annotation(
                text=annotation_text,
                xref='paper', yref='paper',
                x=0.5, y=1.055,  # Slightly above the graph
                showarrow=False,
                font=dict(family="Open Sans", color='red', size=14),
                align='center'
            )

        # ✅ Conditionally Add Warning for Excessive Zero Imputation
        if high_imputation:
            warning_text = "<b>Too Many Zero Replacements ⚠️</b>"
            fig.add_annotation(
                text=warning_text,
                xref='paper', yref='paper',
                x=0.5, y=1.055,  # Higher position for better visibility
                showarrow=False,
                font=dict(family="Open Sans", color='red', size=14),
                align='center'
            )

            # ✅ Bootstrap Alert for UI Notification
            bootstrap_warning = dbc.Alert(
                "Warning: Too many zero replacements in the dataset. This may affect data accuracy.",
                color="warning",
                dismissable=True,
                className="mt-2"
            )
        else:
            bootstrap_warning = None

        return fig, {}, fig.to_dict()

    # ✅ Else, follow your original normalization logic:
    else:

        if primary_categorical_feature in wblca_meta_data.columns:
            #### Code 1 ####
            # ✅ Step 1: Compute total material intensity per project
            project_totals = (
                data_for_aggregation.groupby('Project Index')[numerical_feature]
                .sum()
                .reset_index()
                .rename(columns={numerical_feature: 'total_material_intensity'})
            )

            # ✅ Step 2: Merge total intensity with primary categorical feature
            project_totals = project_totals.merge(
                data_for_aggregation[['Project Index', primary_categorical_feature]].drop_duplicates(),
                on='Project Index',
                how='left'
            )

            # ✅ Compute mean or median for total intensity by primary_categorical_feature
            aggregation_function = "mean" if aggregation_method_material == "mean" else "median"
            totals_by_primary_category = (
                project_totals.groupby(primary_categorical_feature)['total_material_intensity']
                .agg(aggregation_function)
                .reset_index()
                .rename(columns={'total_material_intensity': 'primary_category_aggregate'})
            )

            # ✅ If no secondary_categorical_feature, generate a simple bar chart
            if not secondary_categorical_feature:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=totals_by_primary_category[primary_categorical_feature],
                    y=totals_by_primary_category['primary_category_aggregate'],
                    name=aggregation_method_material.capitalize(),
                    marker=dict(color='#49a5c4')
                ))

                # ✅ Reverse legend order for better readability
                fig.data = fig.data[::-1]

                # ✅ Update layout with Bootstrap styling considerations
                fig.update_layout(
                    title=f"Bar Chart of {numerical_feature} by {primary_categorical_feature} ({aggregation_method_material.capitalize()})",
                    xaxis_title=primary_categorical_feature,
                    yaxis_title=numerical_feature,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    width=graph_width if graph_width else 800,
                    height=graph_height if graph_height else 600,
                    margin=dict(l=40, r=40, t=60, b=40),
                    font=dict(family="Open Sans", size=12),
                    legend_traceorder="reversed",
                    xaxis=dict(showgrid=False),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="lightgray",
                        gridwidth=0.5,
                        type="log" if log_y_axis and not stacked_100_percent else "linear",
                        tickformat=".0%" if stacked_100_percent else None,
                        range=[0, 1] if stacked_100_percent else None  # ✅ Ensures 0-100% range for stacked mode
                    )
                )
                return fig, {}, fig.to_dict()

            # ✅ Step 3: Compute contributions of secondary_categorical_feature per project
            contributions = (
                data_for_aggregation.groupby(['Project Index', secondary_categorical_feature])[numerical_feature]
                .sum()
                .reset_index()
            )

            # ✅ Merge project totals
            contributions = contributions.merge(
                project_totals,
                on='Project Index',
                how='left'
            )

            # ✅ Compute contribution fraction per project
            contributions['secondary_category_contribution'] = (
                contributions[numerical_feature] / contributions['total_material_intensity']
            )

            # ✅ Step 4: Compute mean/median contributions by primary_categorical_feature
            contribution_means = (
                contributions.groupby([primary_categorical_feature, secondary_categorical_feature])['secondary_category_contribution']
                .agg(aggregation_function)
                .reset_index()
            )

            # ✅ Step 5: Normalize contributions to sum to 100%
            contribution_means['normalized_contribution'] = (
                contribution_means.groupby(primary_categorical_feature)['secondary_category_contribution'].transform(lambda x: x / x.sum())
            )

            # ✅ Step 6: Compute contributions to totals
            contribution_means = contribution_means.merge(
                totals_by_primary_category,
                on=primary_categorical_feature,
                how='left'
            )

            contribution_means['normalized_agg_contribution'] = (
                contribution_means['normalized_contribution'] * contribution_means['primary_category_aggregate']
            )

            # ✅ Prepare final output for visualization
            output_df = contribution_means[[primary_categorical_feature, secondary_categorical_feature, 'normalized_agg_contribution']]

            # ✅ Normalize values for 100% stacking mode
            if stacked_100_percent:
                total_per_category = output_df.groupby(primary_categorical_feature)['normalized_agg_contribution'].transform('sum')
                output_df['normalized_agg_contribution'] /= total_per_category
                y_label = "Percentage Contribution (%)"
            else:
                y_label = numerical_feature

            # ✅ Generate Color Mapping for Visualization
            def generate_color_map(categories):
                """Generate a distinct color for each category using a colormap"""
                cmap = cm.get_cmap('tab20', len(categories))  # Use a colormap with many distinct colors
                color_map = {category: f"rgb{tuple(int(255*x) for x in cmap(i)[:3])}" for i, category in enumerate(categories)}
                return color_map

            unique_secondary_cat = output_df[secondary_categorical_feature].unique()
            color_mapping = generate_color_map(unique_secondary_cat)

            category_order = sorted(output_df[primary_categorical_feature].dropna().unique())

            # ✅ Create Stacked Bar Chart
            fig = px.bar(
                output_df,
                x=primary_categorical_feature,
                y="normalized_agg_contribution",
                color=secondary_categorical_feature,
                barmode="relative" if stacked_100_percent else "stack",
                labels={primary_categorical_feature: primary_categorical_feature, "normalized_agg_contribution": y_label},
                color_discrete_sequence=px.colors.qualitative.Vivid,
                title=f"Stacked Bar Plot of {secondary_categorical_feature} Contributions by {primary_categorical_feature} ({aggregation_method_material.capitalize()})",
                category_orders={primary_categorical_feature: category_order}  
            )

            # ✅ Reverse legend order for better readability
            fig.data = fig.data[::-1]

            # ✅ Update layout with Bootstrap styling considerations
            fig.update_layout(
                font=dict(family="Open Sans", size=12),
                plot_bgcolor="white",
                paper_bgcolor="white",
                width=graph_width if graph_width else 800,
                height=graph_height if graph_height else 600,
                margin=dict(l=40, r=40, t=60, b=40),
                legend_traceorder="reversed",
                xaxis=dict(showgrid=False, gridcolor="lightgray", gridwidth=0.5),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="lightgray",
                    gridwidth=0.5,
                    type="log" if log_y_axis and not stacked_100_percent else "linear",
                    tickformat=".0%" if stacked_100_percent else None,
                    range=[0, 1] if stacked_100_percent else None  # ✅ Ensures 0-100% range for stacked mode
                ),
            )
            
            # ✅ Conditionally Add Annotation for Missing Data Handling
            if annotation_text:
                fig.add_annotation(
                    text=annotation_text,
                    xref='paper', yref='paper',
                    x=0.5, y=1.055,  
                    showarrow=False,
                    font=dict(family="Open Sans", color='red', size=14),
                    align='center'
                )

            return fig, {}, fig.to_dict()

        else:
            #### Code 2 ####
            # ✅ Compute total per category (mean or median based on user selection)
            project_grouped_prim = (
                data_for_aggregation.groupby(['Project Index', primary_categorical_feature])[numerical_feature]
                .sum()
                .reset_index()
            )

            # ✅ Choose aggregation method based on user selection
            aggregation_function = "mean" if aggregation_method_material == "mean" else "median"
            primary_category_stats = (
                project_grouped_prim.groupby(primary_categorical_feature)[numerical_feature]
                .agg(aggregation_function)
                .reset_index()
                .rename(columns={numerical_feature: 'primary_category_aggregate'})
            )

            # ✅ If no stacking, generate a simple bar chart
            if not secondary_categorical_feature:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=primary_category_stats[primary_categorical_feature],
                    y=primary_category_stats['primary_category_aggregate'],
                    name=aggregation_method_material.capitalize(),
                    marker=dict(color='#49a5c4')
                ))

                # ✅ Reverse legend order for better readability
                fig.data = fig.data[::-1]

                # ✅ Update layout with Bootstrap styling considerations
                fig.update_layout(
                    title=f"Bar Chart of {numerical_feature} by {primary_categorical_feature} ({aggregation_method_material.capitalize()})",
                    xaxis_title=primary_categorical_feature,
                    yaxis_title=numerical_feature,
                    legend_title="Total",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    width=graph_width if graph_width else 800,
                    height=graph_height if graph_height else 600,
                    margin=dict(l=40, r=40, t=60, b=40),
                    legend_traceorder="reversed",
                    font={'family': 'Open Sans'},
                    xaxis=dict(showgrid=False),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='rgba(200, 200, 200, 0.5)',
                        type="log" if log_y_axis else "linear"
                    ) if not stacked_100_percent else dict(
                        showgrid=True, gridcolor='rgba(200, 200, 200, 0.5)'
                    )
                )
                
                # ✅ Conditionally add annotation here
                if annotation_text:
                    fig.add_annotation(
                        text=annotation_text,
                        xref='paper', yref='paper',
                        x=0.5, y=1.055,
                        showarrow=False,
                        font=dict(family="Open Sans", color='red', size=14),
                        align='center'
                    )

                return fig, {}, fig.to_dict()

            # ✅ Compute total per secondary_categorical_feature (mean or median based on user selection)
            project_grouped_sec = (
                data_for_aggregation.groupby(['Project Index', secondary_categorical_feature])[numerical_feature]
                .sum()
                .reset_index()
            )

            secondary_category_stats = (
                project_grouped_sec.groupby(secondary_categorical_feature)[numerical_feature]
                .agg(aggregation_function)
                .reset_index()
                .rename(columns={numerical_feature: 'secondary_aggregate'})
            )

            # ✅ Map secondary_categorical_feature to primary_categorical_feature
            sec_to_primary = data_for_aggregation[[primary_categorical_feature, secondary_categorical_feature]].drop_duplicates()

            # ✅ Merge primary stats with secondary stats via mapping
            secondary_category_stats = secondary_category_stats.merge(sec_to_primary, on=secondary_categorical_feature, how='left')
            secondary_category_stats = secondary_category_stats.merge(primary_category_stats, on=primary_categorical_feature, how='left')

            # ✅ Calculate **contribution percentage** per primary category
            secondary_category_stats['contribution'] = (
                secondary_category_stats['secondary_aggregate'] /
                secondary_category_stats.groupby(primary_categorical_feature)['secondary_aggregate'].transform('sum')
            )

            # ✅ Normalize contributions based on primary_categorical_feature stats
            secondary_category_stats['normalized_agg'] = (
                secondary_category_stats['contribution'] * secondary_category_stats['primary_category_aggregate']
            )

            # ✅ Prepare final dataframe for visualization
            output_df = secondary_category_stats[
                [primary_categorical_feature, secondary_categorical_feature, 'normalized_agg', 'contribution']
            ]

            # ✅ Normalize values for 100% stacking mode
            if stacked_100_percent:
                total_per_category = output_df.groupby(primary_categorical_feature)['normalized_agg'].transform('sum')
                output_df['normalized_agg'] /= total_per_category
                y_label = "Percentage Contribution (%)"
            else:
                y_label = numerical_feature

            # ✅ Consistently sorted category order
            category_order = sorted(
                data_for_aggregation[primary_categorical_feature]
                .dropna()
                .astype(str)
                .unique()
            )

            # ✅ Generate Stacked Bar Chart
            fig = px.bar(
                output_df,
                x=primary_categorical_feature,
                y="normalized_agg",
                color=secondary_categorical_feature,
                category_orders={primary_categorical_feature: category_order},
                barmode="relative" if stacked_100_percent else "stack",
                labels={primary_categorical_feature: primary_categorical_feature, "normalized_agg": y_label},
                color_discrete_sequence=px.colors.qualitative.Vivid,
                title=f"Stacked Bar Plot of {secondary_categorical_feature} Contributions by {primary_categorical_feature} ({aggregation_method_material.capitalize()})",
            )

            # ✅ Reverse legend order for better readability
            fig.data = fig.data[::-1]

            # ✅ Update layout with Bootstrap styling considerations
            fig.update_layout(
                font=dict(family="Open Sans", size=12),
                plot_bgcolor="white",
                paper_bgcolor="white",
                width=graph_width if graph_width else 800,
                height=graph_height if graph_height else 600,
                margin=dict(l=40, r=40, t=60, b=40),
                legend_traceorder="reversed",
                xaxis=dict(showgrid=False, gridcolor="lightgray", gridwidth=0.5),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="lightgray",
                    gridwidth=0.5,
                    type="log" if log_y_axis else "linear",
                    tickformat=".0%" if stacked_100_percent else None,
                    range=[0, 1] if stacked_100_percent else None
                ),
            )

            # ✅ Conditionally add annotation here
            if annotation_text:
                fig.add_annotation(
                    text=annotation_text,
                    xref='paper', yref='paper',
                    x=0.5, y=1.055,
                    showarrow=False,
                    font=dict(family="Open Sans", color='red', size=14),
                    align='center'
                )

            return fig, {}, fig.to_dict()

################## Building Level Callbacks ########################

# ✅ Callback to dynamically generate filter dropdowns based on selected categorical features
@app.callback(
    Output("filter-values-container", "children"),
    Input("filter-categorical-features", "value"),
    State("building-level-selections", "data")  # ✅ Restore stored selections
)
def update_filter_values_dropdowns(selected_features, stored_selections):
    if not selected_features:
        return []

    stored_selections = stored_selections or {}  # Ensure it's not None

    dropdowns = []
    for feature in selected_features:
        dropdowns.append(
            dbc.Col(
                [
                    dbc.Label(f"Filter {feature}:", className="fw-bold mb-1"),
                    dcc.Dropdown(
                        id={"type": "filter-value", "feature": feature},
                        options=[
                            {"label": val, "value": val} for val in wblca_meta_data[feature].dropna().unique()
                        ],
                        value=stored_selections.get(feature, None),  # ✅ Restore previous selection
                        persistence=True,
                        persistence_type="session",
                        placeholder=f"Select values for {feature}",
                        multi=True,
                    ),
                ],
                width=6,
            )
        )
    return dbc.Row(dropdowns, className="g-2")  # ✅ Apply Bootstrap row layout for alignment

@app.callback(
    Output("building-level-selections", "data"),
    Input({"type": "filter-value", "feature": dash.ALL}, "value"),
    State("filter-categorical-features", "value"),
    prevent_initial_call=True  # ✅ Prevent overwriting on first load
)
def store_selected_filter_values(filter_values, selected_features):
    if not selected_features or not filter_values:
        return {}

    return {feature: values for feature, values in zip(selected_features, filter_values) if values}

@app.callback(
    Output("bar-chart", "figure"),
    [
        Input("categorical-variable", "value"),
        Input("numerical-variable", "value"),
        Input("aggregation-method", "value"),
        Input("graph-width", "value"),
        Input("graph-height", "value"),
        Input("graph-orientation", "value"),
        Input({"type": "filter-value", "feature": dash.ALL}, "value"),
        Input("stacking-variable", "value"),
        Input("show-error-bars", "value"),
    ],
    [State("filter-categorical-features", "value")],
)
def update_bar_chart(
    categorical, numerical, aggregation, width, height, orientation, filter_values, stacking, show_error_bars, filter_features
):
    # ✅ If no categorical or numerical feature is selected, return an empty placeholder figure
    if not categorical or not numerical:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Please select features",
            xaxis_title="",
            yaxis_title="",
            plot_bgcolor="white",
            paper_bgcolor="white",
            width=width if width else 800,
            height=height if height else 600,
            font={'family': 'Open Sans'},
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )
        return empty_fig

    # ✅ Filter the data based on selected filters
    filtered_data = wblca_meta_data.copy()
    if filter_features and filter_values:
        for feature, values in zip(filter_features, filter_values):
            if values:
                filtered_data = filtered_data[filtered_data[feature].isin(values)]

    # ✅ Ensure a primary categorical variable is selected
    if not categorical:
        return {}

    # ✅ Get unique sorted categories to maintain consistent order
    sorted_categories = sorted(filtered_data[categorical].dropna().unique())

    if stacking:
        # ✅ Handle stacked bar chart
        if aggregation in ["mean", "median"]:
            # Calculate overall aggregation per primary category
            overall_agg = (
                filtered_data.groupby(categorical)[numerical]
                .agg(aggregation)
                .reset_index()
                .rename(columns={numerical: "OverallAggregate"})
            )

            # Calculate contributions to the overall aggregation
            contributions = (
                filtered_data.groupby([categorical, stacking])[numerical]
                .sum()
                .reset_index()
            )

            # Merge contributions with the overall aggregate
            contributions = contributions.merge(overall_agg, on=categorical)
            contributions["Contribution"] = (
                contributions[numerical] / contributions.groupby(categorical)[numerical].transform("sum")
            ) * contributions["OverallAggregate"]

            x, y, color = categorical, "Contribution", stacking

        elif aggregation == "count":
            contributions = filtered_data.groupby([categorical, stacking]).size().reset_index(name="Count")
            x, y, color = categorical, "Count", stacking

        elif categorical and numerical:
            contributions = (
                filtered_data.groupby([categorical, stacking])[numerical]
                .sum()
                .reset_index()
            )
            x, y, color = categorical, numerical, stacking

        else:
            return {}

    else:
        # ✅ Handle regular bar chart without stacking
        if aggregation == "count":
            grouped_data = filtered_data[categorical].value_counts().reset_index()
            grouped_data.columns = [categorical, "Count"]
            x, y, color = categorical, "Count", None

        elif categorical and numerical:
            grouped_data = filtered_data.groupby(categorical).agg(
                {numerical: [aggregation, "count", lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]}
            ).reset_index()
            grouped_data.columns = [categorical, "Value", "Count", "Q1", "Q3"]

            # ✅ Add error bars only if checkbox is checked
            if show_error_bars and aggregation in ["mean", "median"]:
                grouped_data["ErrorMinus"] = grouped_data["Value"] - grouped_data["Q1"]
                grouped_data["ErrorPlus"] = grouped_data["Q3"] - grouped_data["Value"]
            else:
                grouped_data["ErrorMinus"], grouped_data["ErrorPlus"] = None, None

            x, y, color = categorical, "Value", None

        else:
            return {}

    # ✅ Dynamically set y-axis label
    y_axis_label = f"{numerical} (Contributions by '{stacking}')" if stacking else (numerical if aggregation != "count" else "Count")

    # ✅ Adjust axes for horizontal orientation
    if orientation == "h":
        x, y = y, x
        x_axis_label, y_axis_label = y_axis_label, categorical
        error_bar_args = {
            "error_x": "ErrorPlus" if show_error_bars and aggregation in ["mean", "median"] else None,
            "error_x_minus": "ErrorMinus" if show_error_bars and aggregation in ["mean", "median"] else None,
        }
    else:
        x_axis_label, error_bar_args = categorical, {
            "error_y": "ErrorPlus" if show_error_bars and aggregation in ["mean", "median"] else None,
            "error_y_minus": "ErrorMinus" if show_error_bars and aggregation in ["mean", "median"] else None,
        }

    # ✅ Generate Bar Chart
    fig = px.bar(
        grouped_data if not stacking else contributions,
        x=x,
        y=y,
        color=color,
        barmode="stack" if stacking else "group",
        orientation=orientation,
        title=f"Bar Chart of {numerical if aggregation != 'count' else 'Counts'} by {categorical}"
              + (f" (Stacked by {stacking})" if stacking else ""),
        category_orders={categorical: sorted_categories},  # ✅ Maintain category order
        labels={x: x_axis_label, y: y_axis_label},
        **error_bar_args,  # ✅ Dynamically add error bars
    )

    # ✅ Reverse legend order for better readability
    fig.data = fig.data[::-1]

    # ✅ Apply Bootstrap Styling to Chart Layout
    fig.update_layout(
        font=dict(family="Open Sans", size=12),
        width=width if width else 800,
        height=height if height else 600,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=40, b=40),
        legend_traceorder="reversed",
        xaxis=dict(showgrid=orientation == "h", gridcolor="lightgray", gridwidth=0.5),
        yaxis=dict(showgrid=orientation == "v", gridcolor="lightgray", gridwidth=0.5),
    )

    return fig

# ✅ Run Server
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)