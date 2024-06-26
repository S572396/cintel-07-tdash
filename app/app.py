#imports at top
import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 




# Define data frame palmer penguins
df = palmerpenguins.load_penguins()

# Set page options
ui.page_opts(title="Sandra's Penguins dashboard", fillable=True)

# For sidebar
with ui.sidebar(title="Filter controls", style="background-color: #e6e6fa;"):  # Apply background color inline
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    # Links
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/s572396/cintel-07-tdash",
        target="_blank",
        style="font-style: italic;"  # Apply italic style inline
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
        style="font-style: italic;"  # Apply italic style inline
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
        style="font-style: italic;"  # Apply italic style inline
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank", style="font-style: italic;")  # Apply italic style inline
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
        style="font-style: italic;"  # Apply italic style inline
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
        style="font-style: italic;"  # Apply italic style inline
    )

# Main Page Layout

# Favicon
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds"), style="background-color: #c8e6c9"):  # Apply background color inline
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal"), style="background-color: #c8e6c9"):  # Apply background color inline
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical"), style="background-color: #c8e6c9"):  # Apply background color inline
        "Avg bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Scatter Plot
with ui.layout_columns():
    with ui.card(full_screen=True, style="background-color: #ffffcc"):  # Apply background color inline
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Dataframe for Statistics
    with ui.card(full_screen=True, style="background-color: #ffffcc"):  # Apply background color inline
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Define Reactive Calculation
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df








