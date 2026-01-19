import reflex as rx
from app.states.dashboard_state import DashboardState, Product
from app.components.charts import stock_level_chart, category_distribution_chart


def export_button(
    label: str, icon: str, on_click_handler: rx.EventHandler
) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="w-4 h-4"),
        rx.el.span(label),
        class_name="flex items-center gap-2 px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 hover:text-gray-900 hover:border-gray-300 transition-all shadow-sm",
        on_click=on_click_handler,
    )


def low_stock_item(product: Product) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("trending_down", class_name="w-4 h-4 text-orange-600"),
                class_name="w-8 h-8 rounded-lg bg-orange-50 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.h4(
                    product["name"],
                    class_name="text-sm font-medium text-gray-900 truncate",
                ),
                rx.el.p(
                    f"Stock: {product['stock']} units",
                    class_name="text-xs text-red-600 font-medium",
                ),
                class_name="min-w-0 flex-1",
            ),
            class_name="flex items-center gap-3",
        ),
        rx.el.button(
            "Reorder",
            class_name="px-2.5 py-1.5 text-xs font-medium text-orange-600 bg-orange-50 rounded-md hover:bg-orange-100 transition-colors",
            on_click=rx.toast(f"Reorder request sent for {product['name']}"),
        ),
        class_name="flex items-center justify-between p-3 rounded-lg border border-gray-100 hover:border-orange-100 hover:bg-orange-50/30 transition-all",
    )


def activity_item(activity: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name=rx.match(
                    activity["type"],
                    ("success", "w-2 h-2 rounded-full bg-green-500"),
                    ("warning", "w-2 h-2 rounded-full bg-orange-500"),
                    ("error", "w-2 h-2 rounded-full bg-red-500"),
                    "w-2 h-2 rounded-full bg-blue-500",
                )
            ),
            class_name="mt-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(activity["action"], class_name="font-medium text-gray-900"),
                rx.el.span(" - ", class_name="text-gray-400"),
                rx.el.span(activity["item"], class_name="text-gray-600"),
                class_name="text-sm",
            ),
            rx.el.div(
                rx.el.span(activity["user"], class_name="font-medium"),
                rx.el.span(" • ", class_name="mx-1"),
                rx.el.span(activity["time"]),
                class_name="text-xs text-gray-400 flex items-center",
            ),
            class_name="flex flex-col gap-0.5",
        ),
        class_name="flex gap-3 py-3 border-b border-gray-50 last:border-0",
    )


def reports_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Analytics & Reports", class_name="text-xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Monitor inventory performance and health",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                export_button(
                    "Export CSV",
                    "file-spreadsheet",
                    DashboardState.export_inventory_csv,
                ),
                export_button(
                    "Download PDF", "file-text", DashboardState.export_inventory_pdf
                ),
                class_name="flex gap-3",
            ),
            class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8",
        ),
        rx.el.div(
            stock_level_chart(),
            category_distribution_chart(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Low Stock Alerts",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.span(
                        f"{DashboardState.low_stock_products.length()} items",
                        class_name="text-xs font-medium text-red-600 bg-red-50 px-2 py-0.5 rounded-full",
                    ),
                    class_name="flex items-center justify-between mb-4",
                ),
                rx.el.div(
                    rx.foreach(DashboardState.low_stock_products, low_stock_item),
                    class_name="flex flex-col gap-2 overflow-y-auto max-h-[300px] pr-2",
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
            ),
            rx.el.div(
                rx.el.h3(
                    "Recent Activity",
                    class_name="text-sm font-semibold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.foreach(DashboardState.recent_activity, activity_item),
                    class_name="flex flex-col overflow-y-auto max-h-[300px] pr-2",
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        class_name="animate-in fade-in duration-500",
    )