from mcp import ClientSession
from mcp.client.sse import sse_client
from PIL import Image
import io
import ast

async def check_bar_chart():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "draw_bar_chart",
                arguments={
                    "x_data": ["Category A", "Category B", "Category C"],
                    "y_data": {
                        "Series 1": [10, 20, 30],
                        "Series 2": [15, 25, 35],
                    },
                    "title": "Bar Chart Example",
                    "x_label": "Categories",
                    "y_label": "Values",
                    "color": "skyblue",  # Màu sắc của các thanh
                    "type": "grouped",  # Loại biểu đồ (grouped, stacked, simple)
                }
            )

            # Giải mã base64 thành hình ảnh
            text = result.content[0].text
            image_bytes = ast.literal_eval(text)
            image = Image.open(io.BytesIO(image_bytes))
            image.show()

async def check_barh_chart():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "draw_barh_chart",
                arguments={
                    "category": {
                        "Category A": [10, 20, 30],
                        "Category B": [15, 25, 35],
                    },
                    "title": "Barh Chart Example",
                    "x_label": "Values",
                    "y_label": "Categories",
                    "color": ['blue', 'green'],
                    "height": 0.8,
                    "align": "center",
                    "left": 0.0
                }
            )

            text = result.content[0].text
            image_bytes = ast.literal_eval(text)
            image = Image.open(io.BytesIO(image_bytes))
            image.show()

async def check_boxplot_chart():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "draw_boxplot_chart",
                arguments={
                    "data": [[10, 20, 30], [15, 25, 35], [5, 10, 15]],  # Dữ liệu cho boxplot
                    "title": "Boxplot Example",
                    "x_label": "Groups",
                    "y_label": "Values",
                    "showfliers": True,  # Hiển thị outliers
                    "notch": True,  # Sử dụng notch cho boxplot
                    "widths": [0.5, 0.5, 0.5]  # Độ rộng của các hộp
                }
            )

            # Giải mã base64 thành hình ảnh
            text = result.content[0].text
            image_bytes = ast.literal_eval(text)
            image = Image.open(io.BytesIO(image_bytes))
            image.show()

async def check_distribution_chart():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "draw_distribution_chart",
                arguments={
                    "category": {
                        "Group A": [55, 60, 65, 70, 75, 80],
                        "Group B": [50, 55, 60, 65, 70, 75],
                        "Group C": [45, 50, 55, 60, 65, 70]
                    },
                    "title": "Histogram of Scores by Group",
                    "x_label": "Scores",
                    "y_label": "Frequency",
                    "bins": 6,
                    "color": ["blue", "orange", "green"],
                    "alpha": 0.7,
                    "stacked": False
                }
            )

            text = result.content[0].text
            image_bytes = ast.literal_eval(text)
            image = Image.open(io.BytesIO(image_bytes))
            image.show()

async def check_line_chart():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "draw_line_chart",
                arguments={
                    "x": [1, 2, 3, 4, 5],
                    "y": [10, 20, 25, 30, 40],
                    "title": "Line Chart Example",
                    "x_label": "Time (s)",
                    "y_label": "Value",
                    "linestyle": "--",
                    "linewidth": 2.5,
                    "marker": "o",
                    "color": "green",
                    "scalex": True,
                    "scaley": True,
                    "label": "Sample Line"
                }
            )

            text = result.content[0].text
            image_bytes = ast.literal_eval(text)
            image = Image.open(io.BytesIO(image_bytes))
            image.show()

async def check_pie_chart():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "draw_pie_chart",
                arguments={
                    "x": [25, 35, 20, 20],
                    "labels": ["Apples", "Bananas", "Cherries", "Dates"],
                    "explode": [0, 0.1, 0, 0],
                    "colors": ["red", "yellow", "pink", "brown"],
                    "autopct": "%.1f%%",
                    "pctdistance": 0.8,
                    "shadow": True,
                    "labeldistance": 1.1,
                    "startangle": 90,
                    "radius": 1,
                    "counterclock": False,
                    "center": (0, 0),
                    "frame": False,
                    "rotatelabels": False,
                    "normalize": True,
                    "title": "Fruit Distribution"
                }
            )

            text = result.content[0].text
            image_bytes = ast.literal_eval(text)
            image = Image.open(io.BytesIO(image_bytes))
            image.show()

async def check_scatterplot():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "draw_scatter_chart",
                arguments={
                    "x": [1, 2, 3, 4, 5],
                    "y": [5, 4, 3, 2, 1],
                    "s": [100, 200, 300, 400, 500],
                    "c": [1, 2, 3, 4, 5],
                    "marker": 'o',
                    "cmap": 'viridis',
                    "alpha": 0.7,
                    "linewidths": 2,
                    "edgecolors": 'black',
                    "title": "Scatter Plot Example",
                    "x_label": "X Axis",
                    "y_label": "Y Axis"
                }
            )

            text = result.content[0].text
            image_bytes = ast.literal_eval(text)
            image = Image.open(io.BytesIO(image_bytes))
            image.show()

async def check_stackplot():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "draw_stackplot_chart",
                arguments={
                    "x": [1, 2, 3, 4, 5],
                    "category": {
                        "Group A": [1, 3, 4, 5, 4],
                        "Group B": [2, 2, 2, 2, 3],
                        "Group C": [3, 1, 1, 2, 1]
                    },
                    "title": "Stacked Area Chart",
                    "x_label": "Time",
                    "y_label": "Value",
                    "colors": ["#1f77b4", "#ff7f0e", "#2ca02c"],
                    "baseline": "zero"
                }
            )

            text = result.content[0].text
            image_bytes = ast.literal_eval(text)
            image = Image.open(io.BytesIO(image_bytes))
            image.show()

async def check_violinplot():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "draw_violinplot_chart",
                arguments={
                    "category": {
                        "Group A": [60, 62, 65, 70, 72, 75],
                        "Group B": [58, 63, 67, 70, 74, 78],
                        "Group C": [55, 60, 66, 72, 76, 80]
                    },
                    "title": "Violin Plot of Scores",
                    "x_label": "Groups",
                    "y_label": "Scores",
                    "orientation": "vertical",
                    "widths": 0.5,
                    "showmedians": True,
                    "side": "both"
                }
            )

            text = result.content[0].text
            image_bytes = ast.literal_eval(text)
            image = Image.open(io.BytesIO(image_bytes))
            image.show()

async def check_generate_report():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "generate_report_analysis",
                arguments={
                    "data_source": "data/sample.csv",
                    "output_html_file": "output/sample_report.html",
                    "date_cols": ["date"],
                    "cat_threshold": 10,
                    "id_cols": ["id"],
                    "report_title": "Sample Data Report"
                }
            )

            # Kiểm tra kết quả trả về
            text = result.content[0].text
            print("Tool result message:", text)

            # Kiểm tra có thực sự tạo ra file HTML chưa
            import os
            if os.path.exists("output/sample_report.html"):
                print("✅ Report generated successfully.")
            else:
                print("❌ Report file not found!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(check_generate_report())



