from mcp.server.fastmcp import FastMCP
from service.order_dataset_service import get_all_orders as service_get_all_orders
from chart.barchart import BarChart
from chart.linechart import LineChart
import io

mcp = FastMCP("Thanh server")

@mcp.tool()
def draw_bar_chart(x_data: list, y_data: list, title: str = "", x_label: str = "", y_label: str = "", color: str = "skyblue") -> str:
    """
    Generate a bar chart from the given data and return it as a PNG byte string.

    Parameters:
        x_data (list): A list of categories or labels for the x-axis.
        y_data (list): A list of numerical values corresponding to each x-axis label.
        title (str): The title of the chart (default is an empty string).
        x_label (str): The label for the x-axis (default is an empty string).
        y_label (str): The label for the y-axis (default is an empty string).
        color (str): The color of the bars in the chart (default is "skyblue").

    Returns:
        str: A base64-encoded PNG image of the generated bar chart.
    """
    bar_chart_object = BarChart(title = title, x_label = x_label, y_label = y_label, color = color)
    fig = bar_chart_object.create_chart(x_data, y_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()

@mcp.tool()
def draw_line_chart(x_data: list, y_data: list, title: str = "", x_label: str = "", y_label: str = "", color: str = "blue") -> str:
    """
    Generate a line chart from the given data and return it as a PNG byte string.

    Parameters:
        x_data (list): A list of categories or labels for the x-axis.
        y_data (list): A list of numerical values corresponding to each x-axis label.
        title (str): The title of the chart (default is an empty string).
        x_label (str): The label for the x-axis (default is an empty string).
        y_label (str): The label for the y-axis (default is an empty string).
        color (str): The color of the line in the chart (default is "blue").

    Returns:
        str: A base64-encoded PNG image of the generated line chart.
    """
    line_chart_object = LineChart(title = title, x_label = x_label, y_label = y_label, color = color)
    fig = line_chart_object.create_chart(x_data, y_data)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return buf.read()


if __name__ == "__main__":
    # Register the service with the server
    mcp.run(transport="sse")