import reflex as rx
from app.states.dashboard_state import DashboardState


def stat_card(
    title: str, value: str, icon: str, trend: str = None, trend_up: bool = True
) -> rx.Component:
    """A single statistic card."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="w-6 h-6 text-orange-600"),
                class_name="w-12 h-12 rounded-xl bg-orange-50 flex items-center justify-center mb-4",
            ),
            rx.el.div(
                rx.cond(
                    trend,
                    rx.el.span(
                        trend,
                        class_name=rx.cond(
                            trend_up,
                            "text-green-600 bg-green-50 px-2 py-0.5 rounded-full text-xs font-medium",
                            "text-red-600 bg-red-50 px-2 py-0.5 rounded-full text-xs font-medium",
                        ),
                    ),
                    None,
                ),
                class_name="ml-auto",
            ),
            class_name="flex items-start",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500 mb-1"),
            rx.el.h3(
                value, class_name="text-2xl font-bold text-gray-900 tracking-tight"
            ),
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow",
    )


def stats_grid() -> rx.Component:
    """The grid of statistic cards."""
    return rx.el.div(
        stat_card(
            "Total Value",
            DashboardState.total_value_formatted,
            "dollar-sign",
            "+12.5%",
            True,
        ),
        stat_card(
            "Total Items",
            DashboardState.total_items.to_string(),
            "package",
            "+4.3%",
            True,
        ),
        stat_card(
            "Low Stock Alerts",
            DashboardState.low_stock_count.to_string(),
            "trending_down",
            "Action Needed",
            False,
        ),
        stat_card(
            "Active Categories", DashboardState.category_count.to_string(), "layers"
        ),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
    )