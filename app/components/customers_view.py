import reflex as rx
from app.states.dashboard_state import DashboardState, Customer, Purchase


def customer_stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-6 h-6 text-{color}-600"),
            class_name=f"w-12 h-12 rounded-xl bg-{color}-50 flex items-center justify-center mb-3",
        ),
        rx.el.p(title, class_name="text-sm font-medium text-gray-500 mb-1"),
        rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
    )


def purchase_row(purchase: Purchase) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=purchase["image"],
                class_name="w-10 h-10 rounded-lg object-contain bg-gray-50 border border-gray-100 p-1",
            ),
            rx.el.div(
                rx.el.p(
                    purchase["product_name"],
                    class_name="text-sm font-medium text-gray-900",
                ),
                rx.el.p(purchase["date"], class_name="text-xs text-gray-500"),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-3",
        ),
        rx.el.span(
            f"${purchase['price']}", class_name="text-sm font-semibold text-gray-900"
        ),
        class_name="flex items-center justify-between p-3 rounded-lg bg-gray-50/50 border border-gray-100 mb-2 last:mb-0",
    )


def customer_card(customer: Customer) -> rx.Component:
    is_expanded = DashboardState.expanded_customer_id == customer["id"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=customer["avatar"],
                    class_name="w-12 h-12 rounded-full border-2 border-white shadow-sm",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            customer["name"],
                            class_name="text-base font-semibold text-gray-900",
                        ),
                        rx.el.span(
                            customer["status"],
                            class_name=rx.match(
                                customer["status"],
                                (
                                    "VIP",
                                    "ml-2 px-2 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-700",
                                ),
                                (
                                    "New",
                                    "ml-2 px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700",
                                ),
                                "ml-2 px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-700",
                            ),
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.p(customer["email"], class_name="text-sm text-gray-500"),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("Total Spent", class_name="text-xs text-gray-500"),
                    rx.el.p(
                        f"${customer['total_spent']}",
                        class_name="text-sm font-bold text-gray-900",
                    ),
                    class_name="text-right mr-6",
                ),
                rx.el.button(
                    rx.icon(
                        "chevron-down",
                        class_name=rx.cond(
                            is_expanded,
                            "w-5 h-5 text-gray-500 transition-transform rotate-180",
                            "w-5 h-5 text-gray-500 transition-transform",
                        ),
                    ),
                    on_click=lambda: DashboardState.toggle_customer_expand(
                        customer["id"]
                    ),
                    class_name="p-2 hover:bg-gray-100 rounded-full transition-colors",
                ),
                class_name="flex items-center",
            ),
            class_name="p-6 flex items-center justify-between",
        ),
        rx.cond(
            is_expanded,
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        "Recent Purchases",
                        class_name="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3",
                    ),
                    rx.foreach(customer["purchases"], purchase_row),
                    class_name="px-6 pb-6 pt-2 border-t border-gray-100",
                ),
                class_name="animate-in slide-in-from-top-2 duration-200",
            ),
        ),
        class_name="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all overflow-hidden",
    )


def customers_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Customers", class_name="text-xl font-bold text-gray-900"),
            rx.el.p(
                "Manage customer relationships and history",
                class_name="text-sm text-gray-500",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            customer_stat_card(
                "Total Customers",
                DashboardState.total_customers_count.to_string(),
                "users",
                "blue",
            ),
            customer_stat_card(
                "Total Revenue",
                DashboardState.total_customer_revenue,
                "dollar-sign",
                "green",
            ),
            customer_stat_card(
                "Repeat Customers",
                DashboardState.repeat_customers_count.to_string(),
                "repeat",
                "purple",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.foreach(DashboardState.customers, customer_card),
            class_name="flex flex-col gap-4",
        ),
        class_name="animate-in fade-in duration-500",
    )