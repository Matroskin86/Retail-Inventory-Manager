import reflex as rx
from app.states.dashboard_state import DashboardState


def header() -> rx.Component:
    """The top header component."""
    return rx.el.header(
        rx.el.div(
            rx.el.h2(
                DashboardState.active_tab, class_name="text-xl font-bold text-gray-900"
            ),
            rx.el.p(
                f"Overview of your {DashboardState.active_tab.lower()}",
                class_name="text-sm text-gray-500 hidden sm:block",
            ),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Search inventory...",
                    on_change=DashboardState.set_search,
                    class_name="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all placeholder-gray-400",
                    default_value=DashboardState.search_query,
                ),
                class_name="relative w-full sm:w-64",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("bell", class_name="w-5 h-5 text-gray-500"),
                    rx.el.div(
                        class_name="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-white"
                    ),
                    class_name="p-2 rounded-lg hover:bg-gray-100 relative transition-colors",
                ),
                class_name="flex items-center border-r border-gray-200 pr-4 mr-4 hidden sm:flex",
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-4 h-4"),
                rx.el.span("Add Product", class_name="hidden sm:inline"),
                on_click=DashboardState.open_add_modal,
                class_name="flex items-center gap-2 px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white text-sm font-medium rounded-lg shadow-sm shadow-orange-200 transition-all hover:shadow-md",
            ),
            class_name="flex items-center gap-4 flex-1 justify-end",
        ),
        class_name="h-20 px-8 flex items-center justify-between bg-white border-b border-gray-200 sticky top-0 z-10",
    )