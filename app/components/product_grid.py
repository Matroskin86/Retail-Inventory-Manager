import reflex as rx
from app.states.dashboard_state import DashboardState, Product


def status_badge(stock: int) -> rx.Component:
    return rx.cond(
        stock == 0,
        rx.el.span(
            "Out of Stock",
            class_name="px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600",
        ),
        rx.cond(
            stock < 10,
            rx.el.span(
                "Low Stock",
                class_name="px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-50 text-red-600",
            ),
            rx.el.span(
                "In Stock",
                class_name="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-50 text-green-600",
            ),
        ),
    )


def product_card(product: Product) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=product["image"],
                class_name="w-full h-full object-contain p-4 group-hover:scale-105 transition-transform duration-300",
            ),
            rx.el.div(
                status_badge(product["stock"]), class_name="absolute top-3 left-3"
            ),
            class_name="h-48 bg-gray-50 rounded-t-xl relative overflow-hidden",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    product["category"],
                    class_name="text-xs font-medium text-orange-600 mb-1",
                ),
                rx.el.h3(
                    product["name"],
                    class_name="text-sm font-semibold text-gray-900 line-clamp-2 min-h-[2.5rem]",
                ),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("Price", class_name="text-xs text-gray-500"),
                    rx.el.p(
                        f"${product['price']}",
                        class_name="text-sm font-bold text-gray-900",
                    ),
                ),
                rx.el.div(
                    rx.el.p("Stock", class_name="text-xs text-gray-500 text-right"),
                    rx.el.p(
                        product["stock"],
                        class_name="text-sm font-bold text-gray-900 text-right",
                    ),
                ),
                class_name="flex items-center justify-between border-t border-gray-100 pt-3 mb-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Edit",
                    on_click=lambda: DashboardState.open_edit_modal(product["id"]),
                    class_name="flex-1 py-1.5 text-xs font-medium text-gray-700 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors",
                ),
                rx.el.button(
                    "Delete",
                    on_click=lambda: DashboardState.delete_product(product["id"]),
                    class_name="flex-1 py-1.5 text-xs font-medium text-red-600 bg-red-50 rounded-md hover:bg-red-100 transition-colors",
                ),
                class_name="flex gap-2",
            ),
            class_name="p-4",
        ),
        class_name="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all group",
    )


def product_grid() -> rx.Component:
    return rx.el.div(
        rx.foreach(DashboardState.filtered_products, product_card),
        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
    )