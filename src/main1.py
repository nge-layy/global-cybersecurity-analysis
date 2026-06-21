import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load dataset
df = pd.read_csv(r"C:\Users\User\OneDrive\Desktop\cybersecurity_analyst\Data\Global_Cybersecurity_Threats_2015-2024.csv")

# Initialize app
app = Dash(__name__)

# KPIs
total_incidents = len(df)
total_loss = df["Financial Loss (in Million $)"].sum()
total_users = df["Number of Affected Users"].sum()
avg_resolution = df["Incident Resolution Time (in Hours)"].mean()

# Helper function for value_counts bar charts
def make_bar_chart(series, title, color_col):
    counts = series.value_counts().reset_index()
    counts.columns = [color_col, "Count"]
    return px.bar(counts, x=color_col, y="Count", title=title, color=color_col)

# Layout
app.layout = html.Div([
    html.H1("Cybersecurity Incident Dashboard",
            style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "30px"}),

    dcc.Tabs([
        # Page 1 Executive Summary
        dcc.Tab(label="Executive Summary", children=[
            html.H2("Key Performance Indicators", style={"textAlign": "center", "color": "#34495e"}),
            html.Div([
                html.Div([
                    html.H3("Total Incidents"),
                    html.P(f"{total_incidents:,}")
                ], style={"width": "22%", "display": "inline-block", "textAlign": "center",
                          "backgroundColor": "#f8f9fa", "padding": "20px", "margin": "10px",
                          "borderRadius": "8px", "boxShadow": "2px 2px 5px #ccc"}),

                html.Div([
                    html.H3("Total Financial Loss"),
                    html.P(f"${total_loss:,.2f}M")
                ], style={"width": "22%", "display": "inline-block", "textAlign": "center",
                          "backgroundColor": "#f8f9fa", "padding": "20px", "margin": "10px",
                          "borderRadius": "8px", "boxShadow": "2px 2px 5px #ccc"}),

                html.Div([
                    html.H3("Total Affected Users"),
                    html.P(f"{total_users:,}")
                ], style={"width": "22%", "display": "inline-block", "textAlign": "center",
                          "backgroundColor": "#f8f9fa", "padding": "20px", "margin": "10px",
                          "borderRadius": "8px", "boxShadow": "2px 2px 5px #ccc"}),

                html.Div([
                    html.H3("Avg. Resolution Time"),
                    html.P(f"{avg_resolution:.2f} hrs")
                ], style={"width": "22%", "display": "inline-block", "textAlign": "center",
                          "backgroundColor": "#f8f9fa", "padding": "20px", "margin": "10px",
                          "borderRadius": "8px", "boxShadow": "2px 2px 5px #ccc"}),
            ], style={"textAlign": "center"})
        ]),

        # Page 2 Attack Analysis
        dcc.Tab(label="Attack Analysis", children=[
            dcc.Graph(figure=make_bar_chart(df["Attack Type"], "Attack Types", "Attack Type"),
                      style={"height": "400px", "width": "80%", "margin": "auto"}),
            dcc.Graph(figure=make_bar_chart(df["Attack Source"], "Attack Sources", "Attack Source"),
                      style={"height": "400px", "width": "80%", "margin": "auto"}),
            dcc.Graph(figure=make_bar_chart(df["Security Vulnerability Type"], "Vulnerabilities", "Vulnerability"),
                      style={"height": "400px", "width": "80%", "margin": "auto"}),
        ]),

        # Page 3 Industry Risk
        dcc.Tab(label="Industry Risk", children=[
            dcc.Graph(figure=make_bar_chart(df["Target Industry"], "Attacks by Industry", "Industry"),
                      style={"height": "400px", "width": "80%", "margin": "auto"}),

            dcc.Graph(figure=px.bar(df.groupby("Target Industry")["Financial Loss (in Million $)"].sum().reset_index(),
                                    x="Target Industry", y="Financial Loss (in Million $)",
                                    title="Loss by Industry", color="Target Industry"),
                      style={"height": "400px", "width": "80%", "margin": "auto"}),

            dcc.Graph(figure=px.bar(df.groupby("Target Industry")["Number of Affected Users"].sum().reset_index(),
                                    x="Target Industry", y="Number of Affected Users",
                                    title="Users by Industry", color="Target Industry"),
                      style={"height": "400px", "width": "80%", "margin": "auto"}),
        ]),

        # Page 4 Financial & Incident Impact
        dcc.Tab(label="Financial & Incident Impact", children=[
            dcc.Graph(figure=px.line(df.groupby("Year")["Financial Loss (in Million $)"].sum().reset_index(),
                                     x="Year", y="Financial Loss (in Million $)", title="Financial Loss Trend"),
                      style={"height": "400px", "width": "80%", "margin": "auto"}),

            dcc.Graph(figure=px.line(df.groupby("Year")["Incident Resolution Time (in Hours)"].mean().reset_index(),
                                     x="Year", y="Incident Resolution Time (in Hours)", title="Resolution Time Trend"),
                      style={"height": "400px", "width": "80%", "margin": "auto"}),

            dcc.Graph(figure=px.scatter(df, x="Incident Resolution Time (in Hours)", y="Financial Loss (in Million $)",
                                        color="Attack Type", title="Correlation: Resolution vs Loss"),
                      style={"height": "400px", "width": "80%", "margin": "auto"}),
        ]),

        # Page 5 Recommendations
        dcc.Tab(label="Recommendations", children=[
            html.H2("Strategic Recommendations", style={"textAlign": "center", "color": "#34495e"}),
            html.Ul([
                html.Li("Improve patch management to reduce unpatched software vulnerabilities."),
                html.Li("Strengthen password policies to mitigate weak credential exploitation."),
                html.Li("Invest in AI-based detection systems to accelerate incident response."),
                html.Li("Prioritize protection for Healthcare and Finance sectors due to high attack frequency."),
                html.Li("Enhance monitoring of nation-state attack patterns to minimize economic damage."),
            ], style={"fontSize": "18px", "lineHeight": "1.8", "marginLeft": "20%"})
        ]),
    ])
])

if __name__ == "__main__":
    app.run(debug=True)
