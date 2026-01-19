import reflex as rx
from app.states.dashboard_state import DashboardState, Product
from app.components.product_grid import status_badge


def table_header(label: str, sort_key: str, align: str = "left") -> rx.Component:
    return rx.el.th(
        rx.el.button(
            rx.el.span(label, class_name="mr-1"),
            rx.cond(
                DashboardState.sort_key == sort_key,
                rx.icon(
                    rx.cond(DashboardState.sort_reverse, "arrow-up", "arrow-down"),
                    class_name="w-3 h-3",
                ),
                rx.icon("arrow-up-down", class_name="w-3 h-3 opacity-30"),
            ),
            on_click=lambda: DashboardState.sort_by(sort_key),
            class_name="flex items-center hover:text-orange-600 transition-colors",
        ),
        class_name=f"px-6 py-3 text-{align} text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50/50 cursor-pointer select-none",
    )


def table_row(product: Product) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=product["image"],
                    class_name="w-10 h-10 rounded-lg object-contain bg-gray-50 border border-gray-100 p-1",
                ),
                rx.el.div(
                    rx.el.p(
                        product["name"], class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.p(product["sku"], class_name="text-xs text-gray-500"),
                    class_name="flex flex-col ml-4",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                product["category"],
                class_name="text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded-md",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"${product['price']}", class_name="text-sm font-semibold text-gray-900"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            status_badge(product["stock"]), class_name="px-6 py-4 whitespace-nowrap"
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        "pencil",
                        class_name="w-4 h-4 text-gray-500 hover:text-orange-600",
                    ),
                    on_click=lambda: DashboardState.open_edit_modal(product["id"]),
                    class_name="p-2 rounded-full hover:bg-orange-50 transition-colors",
                ),
                rx.el.button(
                    rx.icon(
                        "trash-2", class_name="w-4 h-4 text-gray-500 hover:text-red-600"
                    ),
                    on_click=lambda: DashboardState.delete_product(product["id"]),
                    class_name="p-2 rounded-full hover:bg-red-50 transition-colors",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
        class_name="hover:bg-gray-50/80 transition-colors border-b border-gray-100 last:border-0",
    )


def product_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    table_header("Product", "name"),
                    table_header("Category", "category"),
                    table_header("Price", "price"),
                    table_header("Stock", "stock"),
                    rx.el.th(
                        "Actions",
                        class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50/50",
                    ),
                ),
                class_name="border-b border-gray-200",
            ),
            rx.el.tbody(
                rx.foreach(DashboardState.filtered_products, table_row),
                class_name="bg-white divide-y divide-gray-200",
            ),
            class_name="min-w-full",
        ),
        class_name="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm",
    )