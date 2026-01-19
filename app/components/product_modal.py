import reflex as rx
from app.states.dashboard_state import DashboardState


def form_field(
    label: str,
    placeholder: str,
    value_var: rx.Var,
    on_change_handler: rx.EventHandler,
    type_: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            type=type_,
            placeholder=placeholder,
            default_value=value_var,
            on_change=on_change_handler,
            class_name="w-full px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all placeholder-gray-400",
        ),
        class_name="mb-4",
    )


def image_select() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Product Image", class_name="block text-sm font-medium text-gray-700 mb-1"
        ),
        rx.el.div(
            rx.el.img(
                src=DashboardState.form_image,
                class_name="w-16 h-16 rounded-lg border border-gray-200 bg-gray-50 object-contain p-2",
            ),
            rx.el.select(
                rx.foreach(
                    DashboardState.available_images,
                    lambda img: rx.el.option(img, value=img),
                ),
                value=DashboardState.form_image,
                on_change=DashboardState.set_form_image,
                class_name="flex-1 px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 appearance-none",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="mb-4",
    )


def product_modal() -> rx.Component:
    return rx.cond(
        DashboardState.is_modal_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 transition-opacity",
                on_click=DashboardState.close_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        DashboardState.modal_title,
                        class_name="text-xl font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon(
                            "x", class_name="w-5 h-5 text-gray-400 hover:text-gray-600"
                        ),
                        on_click=DashboardState.close_modal,
                    ),
                    class_name="flex items-center justify-between mb-6",
                ),
                rx.el.div(
                    form_field(
                        "Product Name",
                        "Enter product name",
                        DashboardState.form_name,
                        DashboardState.set_form_name,
                    ),
                    rx.el.div(
                        form_field(
                            "Category",
                            "Enter category",
                            DashboardState.form_category,
                            DashboardState.set_form_category,
                        ),
                        form_field(
                            "SKU",
                            "e.g. ELE-001",
                            DashboardState.form_sku,
                            DashboardState.set_form_sku,
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        form_field(
                            "Price ($)",
                            "0.00",
                            DashboardState.form_price.to_string(),
                            DashboardState.set_form_price,
                            "number",
                        ),
                        form_field(
                            "Stock",
                            "0",
                            DashboardState.form_stock.to_string(),
                            DashboardState.set_form_stock,
                            "number",
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    image_select(),
                    class_name="max-h-[60vh] overflow-y-auto pr-2",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=DashboardState.close_modal,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Save Product",
                        on_click=DashboardState.save_product,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-orange-600 rounded-lg hover:bg-orange-700 shadow-sm shadow-orange-200",
                    ),
                    class_name="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-gray-100",
                ),
                class_name="bg-white rounded-xl shadow-2xl w-full max-w-lg p-6 relative z-50 animate-in fade-in zoom-in-95 duration-200",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
        ),
        rx.fragment(),
    )