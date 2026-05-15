import plotly.express as px

def create_line_chart(df, x, y, title):
    fig = px.line(df, x=x, y=y, title=title, markers=True)
    return fig