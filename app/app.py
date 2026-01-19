import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.stats import stats_grid
from app.components.product_grid import product_grid
from app.components.product_table import product_table
from app.components.product_modal import product_modal
from app.components.category_view import category_view
from app.components.reports_view import reports_view
from app.components.settings_view import settings_view
from app.components.customers_view import customers_view
from app.states.dashboard_state import DashboardState


def view_toggle() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.cond(
                DashboardState.category_filter != "",
                rx.el.div(
                    rx.el.h3(
                        DashboardState.category_filter,
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="w-3 h-3"),
                        "Clear",
                        on_click=DashboardState.clear_category_filter,
                        class_name="ml-3 flex items-center gap-1 text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded-md hover:bg-gray-200 transition-colors",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.h3("All Products", class_name="text-lg font-bold text-gray-900"),
            ),
            rx.el.p(
                f"{DashboardState.filtered_products.length()} items found",
                class_name="text-sm text-gray-500 ml-3",
            ),
            class_name="flex items-baseline",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("layout-grid", class_name="w-4 h-4"),
                class_name=rx.cond(
                    DashboardState.view_mode == "grid",
                    "p-2 rounded-lg bg-white text-orange-600 shadow-sm border border-gray-200",
                    "p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-white/50",
                ),
                on_click=DashboardState.toggle_view_mode,
            ),
            rx.el.button(
                rx.icon("list", class_name="w-4 h-4"),
                class_name=rx.cond(
                    DashboardState.view_mode == "table",
                    "p-2 rounded-lg bg-white text-orange-600 shadow-sm border border-gray-200",
                    "p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-white/50",
                ),
                on_click=DashboardState.toggle_view_mode,
            ),
            class_name="flex bg-gray-100/50 p-1 rounded-xl",
        ),
        class_name="flex items-center justify-between mb-6",
    )


def back_button() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon(
                "arrow-left",
                class_name="w-4 h-4 transition-transform group-hover:-translate-x-1",
            ),
            "Back to Categories",
            on_click=DashboardState.clear_category_filter,
            class_name="group flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-orange-600 bg-white border border-gray-200 hover:border-orange-200 hover:bg-orange-50 px-4 py-2.5 rounded-xl shadow-sm transition-all",
        ),
        class_name="mb-6 animate-in slide-in-from-left-2 duration-300",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.cond(DashboardState.category_filter == "", stats_grid(), back_button()),
        view_toggle(),
        rx.cond(DashboardState.view_mode == "grid", product_grid(), product_table()),
        class_name="flex flex-col",
    )


def main_content() -> rx.Component:
    return rx.match(
        DashboardState.active_tab,
        ("Products", dashboard_content()),
        ("Categories", category_view()),
        ("Customers", customers_view()),
        ("Reports", reports_view()),
        ("Settings", settings_view()),
        dashboard_content(),
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(main_content(), class_name="p-8 max-w-[1600px] mx-auto"),
            product_modal(),
            class_name="flex-1 md:ml-64 min-h-screen bg-gray-50/50",
        ),
        class_name="flex font-['Inter'] min-h-screen bg-gray-50",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="orange"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")