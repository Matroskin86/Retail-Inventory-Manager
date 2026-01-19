import reflex as rx
from app.states.dashboard_state import DashboardState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "borderColor": "#E8E8E8",
        "borderRadius": "0.75rem",
        "boxShadow": "0px 4px 12px 0px rgba(0, 0, 0, 0.05)",
        "fontFamily": "sans-serif",
        "fontSize": "0.875rem",
        "fontWeight": "500",
        "padding": "0.5rem 0.75rem",
    },
    "item_style": {"padding": "0", "color": "#1F2937"},
    "label_style": {"color": "#6B7280", "marginBottom": "0.25rem"},
    "separator": "",
    "cursor": False,
}


def stock_level_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Stock Levels (Top Items)",
            class_name="text-sm font-semibold text-gray-900 mb-4",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                vertical=False,
                horizontal=True,
                stroke_dasharray="3 3",
                stroke="#E5E7EB",
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.bar(
                data_key="stock", fill="#F97316", radius=[4, 4, 0, 0], bar_size=40
            ),
            rx.recharts.x_axis(
                data_key="name",
                axis_line=False,
                tick_line=False,
                tick={"fill": "#6B7280", "fontSize": 12},
                dy=10,
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                tick={"fill": "#6B7280", "fontSize": 12},
            ),
            data=DashboardState.stock_level_data,
            width="100%",
            height=300,
            margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm h-full",
    )


def category_distribution_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Category Distribution",
            class_name="text-sm font-semibold text-gray-900 mb-4",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                vertical=True,
                horizontal=False,
                stroke_dasharray="3 3",
                stroke="#E5E7EB",
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.bar(
                data_key="value", fill="#3B82F6", radius=[0, 4, 4, 0], bar_size=30
            ),
            rx.recharts.x_axis(
                type_="number",
                axis_line=False,
                tick_line=False,
                tick={"fill": "#6B7280", "fontSize": 12},
                hide=True,
            ),
            rx.recharts.y_axis(
                data_key="name",
                type_="category",
                width=100,
                axis_line=False,
                tick_line=False,
                tick={"fill": "#4B5563", "fontSize": 12, "fontWeight": 500},
            ),
            layout="vertical",
            data=DashboardState.category_distribution_data,
            width="100%",
            height=300,
            margin={"top": 0, "right": 20, "left": 0, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm h-full",
    )