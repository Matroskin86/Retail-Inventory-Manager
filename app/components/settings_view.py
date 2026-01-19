import reflex as rx
from app.states.dashboard_state import DashboardState


def section_header(title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-medium text-gray-900"),
        rx.el.p(description, class_name="text-sm text-gray-500 mt-1"),
        class_name="mb-6",
    )


def toggle_switch(
    label: str, checked: rx.Var, on_change: rx.EventHandler
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(label, class_name="text-sm font-medium text-gray-700"),
            class_name="flex flex-col",
        ),
        rx.el.button(
            rx.el.span(
                class_name=rx.cond(
                    checked,
                    "translate-x-5 inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out",
                    "translate-x-0 inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out",
                )
            ),
            on_click=on_change,
            class_name=rx.cond(
                checked,
                "relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-orange-600 transition-colors duration-200 ease-in-out focus:outline-none",
                "relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-gray-200 transition-colors duration-200 ease-in-out focus:outline-none",
            ),
        ),
        class_name="flex items-center justify-between py-4",
    )


def input_field(
    label: str, value: rx.Var, on_change: rx.EventHandler, type_: str = "text"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            type=type_,
            default_value=value,
            on_change=on_change,
            class_name="w-full px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all",
        ),
        class_name="mb-4",
    )


def profile_section() -> rx.Component:
    return rx.el.div(
        section_header("Profile Settings", "Manage your public profile and role"),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=DashboardState.user_avatar,
                    class_name="w-20 h-20 rounded-full border-4 border-gray-50",
                ),
                rx.el.div(
                    rx.el.button(
                        "Change Avatar",
                        class_name="px-3 py-1.5 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm",
                        on_click=rx.toast("Avatar upload not implemented in demo"),
                    ),
                    rx.el.p(
                        "JPG, GIF or PNG. Max size of 800K",
                        class_name="text-xs text-gray-400 mt-2",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-6 mb-8",
            ),
            rx.el.div(
                input_field(
                    "Full Name", DashboardState.user_name, DashboardState.set_user_name
                ),
                input_field(
                    "Email Address",
                    DashboardState.user_email,
                    DashboardState.set_user_email,
                    "email",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
            rx.el.div(
                rx.el.label(
                    "Role", class_name="block text-sm font-medium text-gray-700 mb-1"
                ),
                rx.el.div(
                    rx.el.span(
                        DashboardState.user_role,
                        class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
                    ),
                    class_name="py-2",
                ),
                class_name="mb-4",
            ),
            class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
        ),
        class_name="mb-8",
    )


def appearance_section() -> rx.Component:
    return rx.el.div(
        section_header("Appearance", "Customize the look and feel of the dashboard"),
        rx.el.div(
            toggle_switch(
                "Dark Mode", DashboardState.dark_mode, DashboardState.toggle_dark_mode
            ),
            class_name="bg-white px-6 rounded-xl border border-gray-200 shadow-sm",
        ),
        class_name="mb-8",
    )


def notification_section() -> rx.Component:
    return rx.el.div(
        section_header("Notifications", "Choose what you want to be notified about"),
        rx.el.div(
            toggle_switch(
                "Email Notifications",
                DashboardState.notif_email,
                DashboardState.toggle_notif_email,
            ),
            rx.el.div(class_name="border-t border-gray-100"),
            toggle_switch(
                "Low Stock Alerts",
                DashboardState.notif_stock,
                DashboardState.toggle_notif_stock,
            ),
            rx.el.div(class_name="border-t border-gray-100"),
            toggle_switch(
                "Order Updates",
                DashboardState.notif_orders,
                DashboardState.toggle_notif_orders,
            ),
            class_name="bg-white px-6 rounded-xl border border-gray-200 shadow-sm divide-y divide-gray-100",
        ),
        class_name="mb-8",
    )


def store_section() -> rx.Component:
    return rx.el.div(
        section_header("Store Settings", "Manage your store details and preferences"),
        rx.el.div(
            input_field(
                "Store Name", DashboardState.store_name, DashboardState.set_store_name
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Currency",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("USD ($)", value="USD"),
                        rx.el.option("EUR (€)", value="EUR"),
                        rx.el.option("GBP (£)", value="GBP"),
                        value=DashboardState.store_currency,
                        on_change=DashboardState.set_store_currency,
                        class_name="w-full px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 appearance-none",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Timezone",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("UTC-5 (Eastern Time)", value="EST"),
                        rx.el.option("UTC-8 (Pacific Time)", value="PST"),
                        rx.el.option("UTC+0 (London)", value="GMT"),
                        value=DashboardState.store_timezone,
                        on_change=DashboardState.set_store_timezone,
                        class_name="w-full px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 appearance-none",
                    ),
                    class_name="mb-4",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
            class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
        ),
        class_name="mb-8",
    )


def security_section() -> rx.Component:
    return rx.el.div(
        section_header("Security", "Ensure your account is secure"),
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    "Change Password",
                    class_name="text-sm font-medium text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.input(
                        type="password",
                        placeholder="Current Password",
                        class_name="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm mb-3",
                    ),
                    rx.el.input(
                        type="password",
                        placeholder="New Password",
                        class_name="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm mb-3",
                    ),
                    rx.el.input(
                        type="password",
                        placeholder="Confirm New Password",
                        class_name="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    "Update Password",
                    on_click=rx.toast("Password update simulated"),
                    class_name="px-4 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition-colors",
                ),
                class_name="p-6 border-b border-gray-100",
            ),
            rx.el.div(
                toggle_switch(
                    "Two-Factor Authentication (2FA)",
                    DashboardState.two_factor_auth,
                    DashboardState.toggle_two_factor,
                ),
                class_name="px-6",
            ),
            class_name="bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        class_name="mb-8",
    )


def data_section() -> rx.Component:
    return rx.el.div(
        section_header("Data Management", "Manage your application data"),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        "Export Data", class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.p(
                        "Download a copy of all your product and sales data.",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.button(
                    rx.icon("download", class_name="w-4 h-4 mr-2"),
                    "Export CSV",
                    on_click=DashboardState.export_settings_csv,
                    class_name="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50",
                ),
                class_name="flex items-center justify-between p-6 border-b border-gray-100",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        "Clear Cache", class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.p(
                        "Remove temporary files and cached images.",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.button(
                    rx.icon("trash", class_name="w-4 h-4 mr-2"),
                    "Clear Cache",
                    on_click=rx.toast("Cache cleared successfully"),
                    class_name="flex items-center px-4 py-2 text-sm font-medium text-red-600 bg-red-50 border border-red-100 rounded-lg hover:bg-red-100",
                ),
                class_name="flex items-center justify-between p-6",
            ),
            class_name="bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
    )


def settings_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Settings", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Manage your account preferences and store configuration.",
                class_name="text-gray-500 mt-1",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            profile_section(),
            appearance_section(),
            notification_section(),
            store_section(),
            security_section(),
            data_section(),
            class_name="max-w-3xl",
        ),
        class_name="animate-in fade-in duration-500 pb-20",
    )