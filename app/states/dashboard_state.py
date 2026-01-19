import reflex as rx
from typing import TypedDict
import random
import string
import logging
import csv
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class Product(TypedDict):
    id: str
    name: str
    category: str
    price: float
    stock: int
    image: str
    sku: str


class CategoryStat(TypedDict):
    name: str
    count: int
    images: list[str]


class Purchase(TypedDict):
    product_name: str
    price: float
    date: str
    image: str


class Customer(TypedDict):
    id: str
    name: str
    email: str
    avatar: str
    joined_date: str
    total_spent: float
    status: str
    purchases: list[Purchase]


class DashboardState(rx.State):
    """State for the dashboard."""

    search_query: str = ""
    category_filter: str = ""
    active_tab: str = "Products"
    view_mode: str = "grid"
    is_modal_open: bool = False
    editing_product_id: str = ""
    form_name: str = ""
    form_category: str = ""
    form_price: float = 0.0
    form_stock: int = 0
    form_sku: str = ""
    form_image: str = "/placeholder.svg"
    sort_key: str = "name"
    sort_reverse: bool = False
    expanded_customer_id: str = ""
    customers: list[Customer] = [
        {
            "id": "c1",
            "name": "Alice Freeman",
            "email": "alice.f@example.com",
            "avatar": "https://api.dicebear.com/9.x/notionists/svg?seed=Alice",
            "joined_date": "Jan 15, 2024",
            "total_spent": 1245.5,
            "status": "VIP",
            "purchases": [
                {
                    "product_name": "Pro Workstation Laptop",
                    "price": 1199.0,
                    "date": "Mar 10, 2024",
                    "image": "/professional_product_laptop.png",
                },
                {
                    "product_name": "Artisan Coffee Blend",
                    "price": 46.5,
                    "date": "Feb 22, 2024",
                    "image": "/coffee_product_professional.png",
                },
            ],
        },
        {
            "id": "c2",
            "name": "Bob Smith",
            "email": "bob.smith@example.com",
            "avatar": "https://api.dicebear.com/9.x/notionists/svg?seed=Bob",
            "joined_date": "Feb 02, 2024",
            "total_spent": 89.99,
            "status": "Active",
            "purchases": [
                {
                    "product_name": "Premium Urban Backpack",
                    "price": 89.99,
                    "date": "Feb 05, 2024",
                    "image": "/professional_product_backpack.png",
                }
            ],
        },
        {
            "id": "c3",
            "name": "Charlie Davis",
            "email": "charlie.d@example.com",
            "avatar": "https://api.dicebear.com/9.x/notionists/svg?seed=Charlie",
            "joined_date": "Mar 10, 2024",
            "total_spent": 2450.0,
            "status": "VIP",
            "purchases": [
                {
                    "product_name": "Pro DSLR Camera",
                    "price": 1899.0,
                    "date": "Mar 12, 2024",
                    "image": "/professional_product_photography.png",
                },
                {
                    "product_name": "Ergonomic Desk Chair",
                    "price": 450.0,
                    "date": "Mar 11, 2024",
                    "image": "/product_style_professional.png",
                },
                {
                    "product_name": "Minimalist Desk Lamp",
                    "price": 101.0,
                    "date": "Mar 11, 2024",
                    "image": "/product_white_style.png",
                },
            ],
        },
        {
            "id": "c4",
            "name": "Diana Prince",
            "email": "diana.p@example.com",
            "avatar": "https://api.dicebear.com/9.x/notionists/svg?seed=Diana",
            "joined_date": "Dec 05, 2023",
            "total_spent": 399.0,
            "status": "New",
            "purchases": [
                {
                    "product_name": "Smart Watch Series 5",
                    "price": 399.0,
                    "date": "Jan 02, 2024",
                    "image": "/professional_product_smartphone.png",
                }
            ],
        },
        {
            "id": "c5",
            "name": "Evan Wright",
            "email": "evan.w@example.com",
            "avatar": "https://api.dicebear.com/9.x/notionists/svg?seed=Evan",
            "joined_date": "Jan 20, 2024",
            "total_spent": 154.0,
            "status": "Active",
            "purchases": [
                {
                    "product_name": "Premium Leather Portfolio",
                    "price": 129.5,
                    "date": "Jan 25, 2024",
                    "image": "/leather_professional_product.png",
                },
                {
                    "product_name": "Artisan Coffee Blend",
                    "price": 24.5,
                    "date": "Feb 14, 2024",
                    "image": "/coffee_product_professional.png",
                },
            ],
        },
    ]
    products: list[Product] = [
        {
            "id": "1",
            "name": "Premium Urban Backpack",
            "category": "Accessories",
            "price": 89.99,
            "stock": 45,
            "image": "/product_professional_photography.png",
            "sku": "ACC-BP-001",
        },
        {
            "id": "2",
            "name": "Wireless Noise-Canceling Headphones",
            "category": "Electronics",
            "price": 249.99,
            "stock": 12,
            "image": "/product_professional_photography.png",
            "sku": "ELE-HD-002",
        },
        {
            "id": "3",
            "name": "Pro Workstation Laptop",
            "category": "Electronics",
            "price": 1299.0,
            "stock": 8,
            "image": "/product_professional_photography.png",
            "sku": "ELE-LP-003",
        },
        {
            "id": "4",
            "name": "Artisan Coffee Blend",
            "category": "Food & Beverage",
            "price": 24.5,
            "stock": 150,
            "image": "/coffee_product_professional.png",
            "sku": "FNB-CF-004",
        },
        {
            "id": "5",
            "name": "Smart Watch Series 5",
            "category": "Electronics",
            "price": 399.0,
            "stock": 5,
            "image": "/product_style_professional.png",
            "sku": "ELE-SW-005",
        },
        {
            "id": "6",
            "name": "Premium Leather Portfolio",
            "category": "Office",
            "price": 129.5,
            "stock": 25,
            "image": "/professional_product_leather.png",
            "sku": "OFF-PF-006",
        },
        {
            "id": "7",
            "name": "Ergonomic Desk Chair",
            "category": "Furniture",
            "price": 450.0,
            "stock": 3,
            "image": "/product_style_professional.png",
            "sku": "FUR-CH-007",
        },
        {
            "id": "8",
            "name": "Minimalist Desk Lamp",
            "category": "Furniture",
            "price": 75.0,
            "stock": 42,
            "image": "/product_white_style.png",
            "sku": "FUR-LP-008",
        },
        {
            "id": "9",
            "name": "Pro DSLR Camera",
            "category": "Electronics",
            "price": 1899.0,
            "stock": 4,
            "image": "/product_professional_photography.png",
            "sku": "ELE-CM-009",
        },
        {
            "id": "10",
            "name": "Wireless Bluetooth Earbuds",
            "category": "Electronics",
            "price": 129.99,
            "stock": 25,
            "image": "/professional_e_commerce.png",
            "sku": "ELE-EB-010",
        },
        {
            "id": "11",
            "name": "Mechanical Gaming Keyboard",
            "category": "Electronics",
            "price": 159.99,
            "stock": 15,
            "image": "/lighting_professional_e.png",
            "sku": "ELE-KB-011",
        },
        {
            "id": "12",
            "name": "Premium Sunglasses",
            "category": "Accessories",
            "price": 85.0,
            "stock": 40,
            "image": "/professional_e_commerce.png",
            "sku": "ACC-SG-012",
        },
        {
            "id": "13",
            "name": "Organic Green Tea Collection",
            "category": "Food & Beverage",
            "price": 35.0,
            "stock": 60,
            "image": "/tea_professional_e.png",
            "sku": "FNB-GT-013",
        },
        {
            "id": "14",
            "name": "Modern Standing Desk",
            "category": "Furniture",
            "price": 599.0,
            "stock": 8,
            "image": "/professional_e_commerce.png",
            "sku": "FUR-SD-014",
        },
        {
            "id": "15",
            "name": "Executive Leather Wallet",
            "category": "Accessories",
            "price": 65.0,
            "stock": 55,
            "image": "/professional_e_commerce.png",
            "sku": "ACC-LW-015",
        },
        {
            "id": "16",
            "name": "Portable Bluetooth Speaker",
            "category": "Electronics",
            "price": 79.99,
            "stock": 30,
            "image": "/professional_e_commerce.png",
            "sku": "ELE-BS-016",
        },
        {
            "id": "17",
            "name": "Premium Notebook Journal",
            "category": "Office",
            "price": 24.99,
            "stock": 100,
            "image": "/professional_e_commerce.png",
            "sku": "OFF-NJ-017",
        },
        {
            "id": "18",
            "name": "Fire Safety Extinguisher",
            "category": "Office",
            "price": 149.99,
            "stock": 12,
            "image": "/product_photography_red.png",
            "sku": "OFF-FE-018",
        },
        {
            "id": "19",
            "name": "Retro Instant Camera",
            "category": "Electronics",
            "price": 89.99,
            "stock": 22,
            "image": "/product_photography_vintage.png",
            "sku": "ELE-RC-019",
        },
        {
            "id": "20",
            "name": 'Cast Iron Skillet 12"',
            "category": "Food & Beverage",
            "price": 64.99,
            "stock": 35,
            "image": "/product_photography_cast.png",
            "sku": "FNB-CS-020",
        },
        {
            "id": "21",
            "name": "Pro Makeup Brush Set",
            "category": "Accessories",
            "price": 45.0,
            "stock": 48,
            "image": "/product_photography_rose.png",
            "sku": "ACC-MB-021",
        },
        {
            "id": "22",
            "name": "Educational Building Blocks",
            "category": "Toys",
            "price": 32.99,
            "stock": 75,
            "image": "/blocks_product_photography.png",
            "sku": "TOY-BB-022",
        },
        {
            "id": "23",
            "name": "Performance Running Shoes",
            "category": "Sports",
            "price": 124.99,
            "stock": 20,
            "image": "/product_photography_running.png",
            "sku": "SPT-RS-023",
        },
        {
            "id": "24",
            "name": "Geometric Glass Terrarium",
            "category": "Furniture",
            "price": 42.0,
            "stock": 28,
            "image": "/product_photography_glass.png",
            "sku": "FUR-GT-024",
        },
        {
            "id": "25",
            "name": "Smart Electric Toothbrush",
            "category": "Electronics",
            "price": 89.0,
            "stock": 50,
            "image": "/white_product_photography.png",
            "sku": "ELE-TB-025",
        },
    ]
    available_images: list[str] = [
        "/product_professional_photography.png",
        "/coffee_product_professional.png",
        "/product_style_professional.png",
        "/professional_product_leather.png",
        "/product_white_style.png",
        "/professional_product_backpack.png",
        "/professional_product_wireless.png",
        "/professional_product_laptop.png",
        "/professional_product_coffee.png",
        "/professional_product_smartphone.png",
        "/professional_product_premium.png",
        "/style_professional_product.png",
        "/white_professional_product.png",
        "/professional_product_photography.png",
        "/leather_professional_product.png",
        "/professional_e_commerce.png",
        "/lighting_professional_e.png",
        "/tea_professional_e.png",
        "/product_photography_red.png",
        "/product_photography_vintage.png",
        "/product_photography_cast.png",
        "/product_photography_rose.png",
        "/blocks_product_photography.png",
        "/product_photography_running.png",
        "/product_photography_glass.png",
        "/white_product_photography.png",
        "/placeholder.svg",
    ]

    @rx.var
    def filtered_products(self) -> list[Product]:
        items = self.products
        if self.category_filter:
            items = [p for p in items if p["category"] == self.category_filter]
        if self.search_query:
            query = self.search_query.lower()
            items = [
                p
                for p in items
                if query in p["name"].lower()
                or query in p["category"].lower()
                or query in p["sku"].lower()
            ]
        try:
            return sorted(
                items, key=lambda x: x[self.sort_key], reverse=self.sort_reverse
            )
        except Exception as e:
            logging.exception(f"Error sorting products: {e}")
            return items

    @rx.var
    def total_items(self) -> int:
        return sum((p["stock"] for p in self.products))

    @rx.var
    def total_value(self) -> float:
        return sum((p["price"] * p["stock"] for p in self.products))

    @rx.var
    def total_value_formatted(self) -> str:
        val = self.total_value
        return f"${val:,.2f}"

    @rx.var
    def low_stock_count(self) -> int:
        return sum((1 for p in self.products if p["stock"] < 10))

    @rx.var
    def category_count(self) -> int:
        return len(set((p["category"] for p in self.products)))

    @rx.var
    def unique_categories(self) -> list[str]:
        return sorted(list(set((p["category"] for p in self.products))))

    @rx.var
    def category_stats(self) -> list[CategoryStat]:
        stats = {}
        for p in self.products:
            cat = p["category"]
            if cat not in stats:
                stats[cat] = {"name": cat, "count": 0, "images": []}
            stats[cat]["count"] += 1
            if len(stats[cat]["images"]) < 8:
                stats[cat]["images"].append(p["image"])
        return sorted(list(stats.values()), key=lambda x: x["name"])

    @rx.var
    def stock_level_data(self) -> list[dict[str, str | int]]:
        sorted_products = sorted(self.products, key=lambda p: p["stock"], reverse=True)[
            :10
        ]
        return [
            {
                "name": p["name"].split(" ")[0] + "...",
                "stock": p["stock"],
                "full_name": p["name"],
            }
            for p in sorted_products
        ]

    @rx.var
    def category_distribution_data(self) -> list[dict[str, str | int]]:
        counts = {}
        for p in self.products:
            cat = p["category"]
            counts[cat] = counts.get(cat, 0) + 1
        return [{"name": k, "value": v} for k, v in counts.items()]

    @rx.var
    def low_stock_products(self) -> list[Product]:
        return [p for p in self.products if p["stock"] < 10]

    @rx.var
    def recent_activity(self) -> list[dict[str, str]]:
        return [
            {
                "action": "Restock",
                "item": "Wireless Headphones",
                "time": "2h ago",
                "user": "Jane Admin",
                "type": "success",
            },
            {
                "action": "New Order",
                "item": "Ergonomic Chair",
                "time": "4h ago",
                "user": "System",
                "type": "info",
            },
            {
                "action": "Price Update",
                "item": "Smart Watch",
                "time": "5h ago",
                "user": "Jane Admin",
                "type": "warning",
            },
            {
                "action": "Low Stock",
                "item": "Pro Laptop",
                "time": "1d ago",
                "user": "System",
                "type": "error",
            },
        ]

    @rx.var
    def modal_title(self) -> str:
        return "Edit Product" if self.editing_product_id else "Add New Product"

    @rx.var
    def total_customers_count(self) -> int:
        return len(self.customers)

    @rx.var
    def total_customer_revenue(self) -> str:
        total = sum((c["total_spent"] for c in self.customers))
        return f"${total:,.2f}"

    @rx.var
    def repeat_customers_count(self) -> int:
        return len([c for c in self.customers if len(c["purchases"]) > 1])

    @rx.event
    def toggle_customer_expand(self, customer_id: str):
        if self.expanded_customer_id == customer_id:
            self.expanded_customer_id = ""
        else:
            self.expanded_customer_id = customer_id

    @rx.event
    def set_search(self, query: str):
        self.search_query = query

    @rx.event
    def set_active_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def filter_by_category(self, category: str):
        self.category_filter = category
        self.active_tab = "Products"

    @rx.event
    def clear_category_filter(self):
        self.category_filter = ""
        self.active_tab = "Categories"

    @rx.event
    def toggle_view_mode(self):
        self.view_mode = "table" if self.view_mode == "grid" else "grid"

    @rx.event
    def sort_by(self, key: str):
        if self.sort_key == key:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_key = key
            self.sort_reverse = False

    @rx.event
    def open_add_modal(self):
        self.editing_product_id = ""
        self.form_name = ""
        self.form_category = ""
        self.form_price = 0.0
        self.form_stock = 0
        self.form_sku = ""
        self.form_image = "/placeholder.svg"
        self.is_modal_open = True

    @rx.event
    def open_edit_modal(self, product_id: str):
        self.editing_product_id = product_id
        product = next((p for p in self.products if p["id"] == product_id), None)
        if product:
            self.form_name = product["name"]
            self.form_category = product["category"]
            self.form_price = product["price"]
            self.form_stock = product["stock"]
            self.form_sku = product["sku"]
            self.form_image = product["image"]
            self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False

    @rx.event
    def set_form_name(self, value: str):
        self.form_name = value

    @rx.event
    def set_form_category(self, value: str):
        self.form_category = value

    @rx.event
    def set_form_price(self, value: str):
        try:
            self.form_price = float(value)
        except ValueError as e:
            logging.exception(f"Error setting form price: {e}")
            pass

    @rx.event
    def set_form_stock(self, value: str):
        try:
            self.form_stock = int(value)
        except ValueError as e:
            logging.exception(f"Error setting form stock: {e}")
            pass

    @rx.event
    def set_form_sku(self, value: str):
        self.form_sku = value

    @rx.event
    def set_form_image(self, value: str):
        self.form_image = value

    @rx.event
    def save_product(self):
        if self.editing_product_id:
            for p in self.products:
                if p["id"] == self.editing_product_id:
                    p["name"] = self.form_name
                    p["category"] = self.form_category
                    p["price"] = self.form_price
                    p["stock"] = self.form_stock
                    p["sku"] = self.form_sku
                    p["image"] = self.form_image
                    break
        else:
            new_id = "".join(random.choices(string.digits, k=6))
            new_product: Product = {
                "id": new_id,
                "name": self.form_name,
                "category": self.form_category,
                "price": self.form_price,
                "stock": self.form_stock,
                "sku": self.form_sku,
                "image": self.form_image,
            }
            self.products.insert(0, new_product)
        self.is_modal_open = False

    @rx.event
    def delete_product(self, product_id: str):
        self.products = [p for p in self.products if p["id"] != product_id]

    user_name: str = "Jane Admin"
    user_email: str = "jane@inventra.com"
    user_role: str = "Store Manager"
    user_avatar: str = "https://api.dicebear.com/9.x/notionists/svg?seed=Admin"
    dark_mode: bool = False
    notif_email: bool = True
    notif_stock: bool = True
    notif_orders: bool = False
    store_name: str = "Inventra Retail"
    store_currency: str = "USD"
    store_timezone: str = "EST"
    two_factor_auth: bool = False

    @rx.event
    def set_user_name(self, value: str):
        self.user_name = value

    @rx.event
    def set_user_email(self, value: str):
        self.user_email = value

    @rx.event
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

    @rx.event
    def toggle_notif_email(self):
        self.notif_email = not self.notif_email

    @rx.event
    def toggle_notif_stock(self):
        self.notif_stock = not self.notif_stock

    @rx.event
    def toggle_notif_orders(self):
        self.notif_orders = not self.notif_orders

    @rx.event
    def set_store_name(self, value: str):
        self.store_name = value

    @rx.event
    def set_store_currency(self, value: str):
        self.store_currency = value

    @rx.event
    def set_store_timezone(self, value: str):
        self.store_timezone = value

    @rx.event
    def toggle_two_factor(self):
        self.two_factor_auth = not self.two_factor_auth

    @rx.event
    def export_inventory_csv(self):
        """Generates and triggers a download of the current inventory as a CSV."""
        try:
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["ID", "Name", "Category", "Price", "Stock", "SKU"])
            for product in self.products:
                writer.writerow(
                    [
                        product["id"],
                        product["name"],
                        product["category"],
                        product["price"],
                        product["stock"],
                        product["sku"],
                    ]
                )
            csv_content = output.getvalue()
            output.close()
            return rx.download(data=csv_content, filename="inventory_export.csv")
        except Exception as e:
            logging.exception(f"Error exporting CSV: {e}")
            return rx.toast.error("Failed to generate CSV export.")

    @rx.event
    def export_inventory_pdf(self):
        """Generates and triggers a download of a PDF report using ReportLab."""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            header_style = ParagraphStyle(
                "HeaderStyle",
                parent=styles["Heading1"],
                textColor=colors.orange,
                alignment=1,
                spaceAfter=12,
            )
            sub_header_style = ParagraphStyle(
                "SubHeaderStyle",
                parent=styles["Normal"],
                textColor=colors.gray,
                alignment=1,
                spaceAfter=20,
            )
            stats_style = ParagraphStyle(
                "StatsStyle", parent=styles["Normal"], fontSize=10, leading=14
            )
            elements = []
            elements.append(Paragraph("Inventra Inventory Report", header_style))
            elements.append(
                Paragraph(
                    f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    sub_header_style,
                )
            )
            elements.append(Paragraph("<b>Inventory Summary</b>", stats_style))
            summary_data = [
                [
                    f"Total Unique Products: {len(self.products)}",
                    f"Total Items in Stock: {self.total_items}",
                ],
                [
                    f"Total Inventory Value: {self.total_value_formatted}",
                    f"Low Stock Alerts: {self.low_stock_count}",
                ],
                [f"Active Categories: {self.category_count}", ""],
            ]
            summary_table = Table(summary_data, colWidths=[200, 200])
            summary_table.setStyle(
                TableStyle(
                    [
                        ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ]
                )
            )
            elements.append(summary_table)
            elements.append(Spacer(1, 20))
            table_data = [["Product Name", "Category", "Price", "Stock"]]
            for p in self.products:
                table_data.append(
                    [
                        p["name"],
                        p["category"],
                        f"${p['price']:,.2f}",
                        f"{p['stock']} units",
                    ]
                )
            p_table = Table(table_data, repeatRows=1, colWidths=[200, 100, 80, 80])
            p_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.orange),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("ALIGN", (2, 0), (3, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -1), 9),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.whitesmoke],
                        ),
                    ]
                )
            )
            elements.append(p_table)
            doc.build(elements)
            pdf_content = buffer.getvalue()
            buffer.close()
            return rx.download(
                data=pdf_content,
                filename=f"inventory_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            )
        except Exception as e:
            logging.exception(f"Error exporting PDF with ReportLab: {e}")
            return rx.toast.error("Failed to generate PDF report.")

    @rx.event
    def export_settings_csv(self):
        """Generates and triggers a download of store and user settings as a CSV."""
        try:
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Settings Type", "Field", "Value"])
            writer.writerow(["Profile", "Name", self.user_name])
            writer.writerow(["Profile", "Email", self.user_email])
            writer.writerow(["Profile", "Role", self.user_role])
            writer.writerow(["Preferences", "Dark Mode", str(self.dark_mode)])
            writer.writerow(
                ["Preferences", "Email Notifications", str(self.notif_email)]
            )
            writer.writerow(["Preferences", "Stock Alerts", str(self.notif_stock)])
            writer.writerow(["Preferences", "Order Updates", str(self.notif_orders)])
            writer.writerow(["Store", "Store Name", self.store_name])
            writer.writerow(["Store", "Currency", self.store_currency])
            writer.writerow(["Store", "Timezone", self.store_timezone])
            writer.writerow(["Store", "2FA Enabled", str(self.two_factor_auth)])
            csv_content = output.getvalue()
            output.close()
            return rx.download(data=csv_content, filename="store_settings_export.csv")
        except Exception as e:
            logging.exception(f"Error exporting settings CSV: {e}")
            return rx.toast.error("Failed to export settings.")