import reflex as rx
from app.states.dashboard_state import DashboardState, CategoryStat


def category_card(category: CategoryStat) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.match(
                category["name"],
                ("Electronics", rx.icon("cpu", class_name="w-6 h-6 text-orange-600")),
                (
                    "Accessories",
                    rx.icon("shopping-bag", class_name="w-6 h-6 text-orange-600"),
                ),
                (
                    "Food & Beverage",
                    rx.icon("coffee", class_name="w-6 h-6 text-orange-600"),
                ),
                ("Office", rx.icon("briefcase", class_name="w-6 h-6 text-orange-600")),
                (
                    "Furniture",
                    rx.icon("armchair", class_name="w-6 h-6 text-orange-600"),
                ),
                ("Toys", rx.icon("blocks", class_name="w-6 h-6 text-orange-600")),
                ("Sports", rx.icon("dumbbell", class_name="w-6 h-6 text-orange-600")),
                rx.icon("layers", class_name="w-6 h-6 text-orange-600"),
            ),
            class_name="w-12 h-12 rounded-xl bg-orange-50 flex items-center justify-center mb-4",
        ),
        rx.el.h3(category["name"], class_name="text-lg font-bold text-gray-900 mb-1"),
        rx.el.p(
            f"{category['count']} Products", class_name="text-sm text-gray-500 mb-4"
        ),
        rx.el.div(
            rx.foreach(
                category["images"],
                lambda img: rx.image(
                    src=img,
                    class_name="w-8 h-8 rounded-full border-2 border-white object-contain bg-gray-50 -ml-3 first:ml-0 hover:scale-110 transition-transform shadow-sm min-w-[2rem]",
                ),
            ),
            class_name="flex items-center pl-1 overflow-x-auto pb-2 scrollbar-hide",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm hover:shadow-md hover:border-orange-200 transition-all cursor-pointer flex flex-col h-full",
        on_click=lambda: DashboardState.filter_by_category(category["name"]),
    )


def category_view() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Product Categories", class_name="text-xl font-bold text-gray-900 mb-6"
        ),
        rx.el.div(
            rx.foreach(DashboardState.category_stats, category_card),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6",
        ),
    )