import reflex as rx
from app.states.dashboard_state import DashboardState


def nav_item(icon: str, text: str, tab_name: str) -> rx.Component:
    """A navigation item in the sidebar."""
    is_active = DashboardState.active_tab == tab_name
    return rx.el.button(
        rx.icon(
            icon,
            class_name=rx.cond(
                is_active,
                "w-5 h-5 text-orange-600",
                "w-5 h-5 text-gray-400 group-hover:text-gray-600",
            ),
        ),
        rx.el.span(
            text,
            class_name=rx.cond(
                is_active,
                "font-medium text-gray-900",
                "font-medium text-gray-500 group-hover:text-gray-900",
            ),
        ),
        on_click=lambda: DashboardState.set_active_tab(tab_name),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-3 py-2.5 rounded-lg bg-orange-50 w-full transition-colors",
            "flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-50 w-full transition-colors group",
        ),
    )


def sidebar() -> rx.Component:
    """The main sidebar component."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("box", class_name="w-8 h-8 text-white fill-orange-500"),
                rx.el.div(
                    rx.el.h1(
                        "Inventra",
                        class_name="text-xl font-bold text-gray-900 leading-none",
                    ),
                    rx.el.span(
                        "Retail Manager", class_name="text-xs font-medium text-gray-500"
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3 px-2",
            ),
            class_name="h-16 flex items-center mb-6",
        ),
        rx.el.nav(
            rx.el.div(
                rx.el.p(
                    "MENU",
                    class_name="text-xs font-semibold text-gray-400 mb-4 px-3 tracking-wider",
                ),
                rx.el.div(
                    nav_item("package", "Products", "Products"),
                    nav_item("layers", "Categories", "Categories"),
                    nav_item("users", "Customers", "Customers"),
                    nav_item("bar-chart-3", "Reports", "Reports"),
                    class_name="flex flex-col gap-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.p(
                    "SETTINGS",
                    class_name="text-xs font-semibold text-gray-400 mb-4 px-3 tracking-wider",
                ),
                rx.el.div(
                    nav_item("settings", "Settings", "Settings"),
                    class_name="flex flex-col gap-1",
                ),
            ),
            class_name="flex-1 overflow-y-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src="https://api.dicebear.com/9.x/notionists/svg?seed=Admin",
                    class_name="w-9 h-9 rounded-full bg-gray-100",
                ),
                rx.el.div(
                    rx.el.p(
                        "Jane Admin",
                        class_name="text-sm font-semibold text-gray-900 leading-none",
                    ),
                    rx.el.p("Store Manager", class_name="text-xs text-gray-500"),
                    class_name="flex flex-col gap-1",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.icon(
                "log-out",
                class_name="w-5 h-5 text-gray-400 hover:text-gray-600 cursor-pointer",
            ),
            class_name="mt-auto pt-6 border-t border-gray-100 flex items-center justify-between",
        ),
        class_name="hidden md:flex flex-col w-64 bg-white border-r border-gray-200 h-screen p-6 fixed left-0 top-0 z-20",
    )