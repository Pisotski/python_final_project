import dash
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State

from query.query import query_player_info, query_players_by_year

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Player Stats Query"

app.layout = html.Div(
    [
        html.H1(
            "Player Stats by Year",
            style={"textAlign": "center", "color": "#f0f0f0", "marginBottom": "30px"},
        ),
        html.Div(
            [
                dcc.Input(
                    id="year-input",
                    type="text",
                    placeholder="Enter year...",
                    debounce=True,
                    style={
                        "padding": "10px",
                        "fontSize": "16px",
                        "borderRadius": "5px",
                        "border": "1px solid #555",
                        "backgroundColor": "#333",
                        "color": "#f0f0f0",
                        "width": "200px",
                        "marginRight": "10px",
                    },
                ),
                html.Button(
                    "Submit",
                    id="submit-button",
                    n_clicks=0,
                    style={
                        "padding": "10px 20px",
                        "fontSize": "16px",
                        "borderRadius": "5px",
                        "border": "none",
                        "backgroundColor": "#007bff",
                        "color": "white",
                        "cursor": "pointer",
                    },
                ),
            ],
            style={"textAlign": "center", "marginBottom": "20px"},
        ),
        html.Div(id="message", style={"textAlign": "center", "marginBottom": "10px"}),
        html.Div(
            [
                html.Div(
                    dash_table.DataTable(
                        id="results-table",
                        columns=[
                            {
                                "name": "Player Name",
                                "id": "Player Name",
                                "presentation": "markdown",
                            },
                            {"name": "Statistic", "id": "Statistic"},
                            {"name": "Value", "id": "Value"},
                        ],
                        data=[],
                        style_table={"overflowX": "auto", "width": "100%"},
                        style_cell={
                            "textAlign": "left",
                            "padding": "8px",
                            "backgroundColor": "#222",
                            "color": "#eee",
                            "fontFamily": "Arial, sans-serif",
                            "fontSize": "14px",
                        },
                        style_header={
                            "backgroundColor": "#444",
                            "fontWeight": "bold",
                            "color": "#fff",
                        },
                        style_data_conditional=[
                            {
                                "if": {"row_index": "odd"},
                                "backgroundColor": "#2a2a2a",
                            },
                            {
                                "if": {"state": "selected"},
                                "backgroundColor": "#007bff",
                                "color": "white",
                            },
                        ],
                        page_size=20,
                    ),
                    style={"flex": 2},
                ),
                html.Div(id="player-info-display", style={"flex": 1}),
            ],
            style={"display": "flex", "gap": "40px"},
        ),
    ],
    style={"backgroundColor": "#121212", "minHeight": "100vh", "padding": "2rem"},
)


@app.callback(
    Output("results-table", "data"),
    Output("message", "children"),
    Input("submit-button", "n_clicks"),
    State("year-input", "value"),
)
def update_output(n_clicks, year):
    if not n_clicks:
        return [], ""

    if not year or not year.isdigit():
        return [], html.Div(
            "Please enter a valid numeric year.",
            style={"color": "red", "fontWeight": "bold"},
        )

    rows = query_players_by_year(int(year))
    if not rows:
        return [], html.Div(f"No data found for year {year}", style={"color": "orange"})

    table_data = [
        {"Player Name": name, "Statistic": stat, "Value": val}
        for name, stat, val in rows
    ]
    return table_data, html.Div(
        f"Showing top {len(table_data)} stats for year {year}",
        style={"color": "lightgreen", "fontWeight": "bold"},
    )


@app.callback(
    Output("player-info-display", "children"),
    Input("results-table", "active_cell"),
    State("results-table", "data"),
)
def on_click_player(active_cell, data):
    if active_cell and active_cell["column_id"] == "Player Name":
        row = active_cell["row"]
        player_name = data[row]["Player Name"]
        info = query_player_info(player_name)
        if not info:
            return html.Div(
                "No data found.", style={"color": "orange", "textAlign": "center"}
            )

        keys = [
            "Birth Name",
            "Nickname",
            "Born On",
            "Born In",
            "Died On",
            "Died In",
            "Cemetery",
            "High School",
            "College",
            "Bats",
            "Throws",
            "Height",
            "Weight",
            "First Game",
            "Last Game",
            "Zodiac Sign",
        ]

        record = [{"Field": k, "Value": v if v else "—"} for k, v in zip(keys, info)]

        return html.Div(
            [
                html.H3(
                    f"Player Details: {player_name}",
                    style={
                        "textAlign": "center",
                        "color": "#f0f0f0",
                        "margin": "0",
                    },
                ),
                dash_table.DataTable(
                    id="player-info-table",
                    columns=[
                        {"name": "Field", "id": "Field"},
                        {"name": "Value", "id": "Value"},
                    ],
                    data=record,
                    style_cell={
                        "textAlign": "left",
                        "paddingLeft": "8px",
                        "backgroundColor": "#1e1e1e",
                        "color": "#eee",
                        "fontFamily": "Arial, sans-serif",
                        "fontSize": "14px",
                    },
                    style_header={
                        "backgroundColor": "#333",
                        "fontWeight": "bold",
                        "color": "#fff",
                    },
                    style_data_conditional=[
                        {
                            "if": {"column_id": "Field"},
                            "fontWeight": "bold",
                            "color": "#bbb",
                        }
                    ],
                    style_table={"width": "80%", "margin": "2rem auto"},
                ),
            ]
        )

    return dash.no_update


if __name__ == "__main__":
    app.run(debug=True)
