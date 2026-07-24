"""
Eurocaps -- Raw Material & Order Management System
====================================================
A simple desktop app (Tkinter) for managing raw material stock,
placing orders with suppliers, and generating reports.

Data is stored in three tab-separated CSV files that live next to
this script: inventory.csv, orders.csv and suppliers.csv.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

# ─────────────────────────────────────────
#  FILE PATHS
# ─────────────────────────────────────────
# Resolved relative to this script's own folder, so the app works no matter
# which folder you launch it from -- as long as the CSV files sit next to
# app.py, everything works out of the box.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.csv")
ORDERS_FILE = os.path.join(BASE_DIR, "orders.csv")
SUPPLIERS_FILE = os.path.join(BASE_DIR, "suppliers.csv")

# ─────────────────────────────────────────
#  COLORS & FONTS (Eurocaps theme)
# ─────────────────────────────────────────
ORANGE = "#F47C20"
ORANGE_DARK = "#D4631A"
ORANGE_LIGHT = "#FFF0E0"
WHITE = "#FFFFFF"
BACKGROUND = "#F9F9F9"
TEXT_DARK = "#1A1A1A"
TEXT_GRAY = "#6B6B6B"
RED = "#E03E3E"
GREEN = "#2E9E5B"
BORDER = "#E8E8E8"
SIDEBAR = "#1E1E1E"
SIDEBAR_HOVER = "#2E2E2E"

FONT_TITLE = ("Georgia", 20, "bold")
FONT_SUBTITLE = ("Georgia", 13, "bold")
FONT_LABEL = ("Trebuchet MS", 10)
FONT_LABEL_BOLD = ("Trebuchet MS", 10, "bold")
FONT_BUTTON = ("Trebuchet MS", 10, "bold")
FONT_SMALL = ("Trebuchet MS", 9)
FONT_LARGE = ("Trebuchet MS", 11)

LOGIN_USERNAME = "123"
LOGIN_PASSWORD = "123"


# ─────────────────────────────────────────
#  CSV HELPERS
# ─────────────────────────────────────────
def load_csv(path: str) -> list[dict]:
    """Read a comma-separated CSV file into a list of dicts."""
    with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=","))


def save_csv(path: str, rows: list[dict], fields: list[str]) -> None:
    """Write a list of dicts back to a comma-separated CSV file."""
    with open(path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=",")
        writer.writeheader()
        writer.writerows(rows)


# ─────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────
window = tk.Tk()
window.title("Eurocaps -- Raw Material & Order Management")
window.geometry("1100x650")
window.configure(bg=BACKGROUND)
window.resizable(True, True)

# ─────────────────────────────────────────
#  TREEVIEW (TABLE) STYLE
# ─────────────────────────────────────────
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT_DARK,
    rowheight=28,
    fieldbackground=WHITE,
    font=FONT_SMALL,
    borderwidth=0,
)
style.configure(
    "Treeview.Heading",
    background=ORANGE,
    foreground=WHITE,
    font=FONT_LABEL_BOLD,
    relief="flat",
    padding=(8, 6),
)
style.map("Treeview", background=[("selected", ORANGE_LIGHT)], foreground=[("selected", TEXT_DARK)])
style.map("Treeview.Heading", background=[("active", ORANGE_DARK)])

# ─────────────────────────────────────────
#  LAYOUT: SIDEBAR + CONTENT
# ─────────────────────────────────────────
main_frame = tk.Frame(window, bg=BACKGROUND)
main_frame.pack(fill="both", expand=True)

sidebar = tk.Frame(main_frame, bg=SIDEBAR, width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

logo_frame = tk.Frame(sidebar, bg=ORANGE, height=80)
logo_frame.pack(fill="x")
logo_frame.pack_propagate(False)
tk.Label(logo_frame, text="EUROCAPS", font=("Georgia", 14, "bold"), bg=ORANGE, fg=WHITE).pack(expand=True)
tk.Label(logo_frame, text="Raw Material Management", font=("Trebuchet MS", 8), bg=ORANGE, fg="#FFD5A8").pack()

content = tk.Frame(main_frame, bg=BACKGROUND)
content.pack(side="left", fill="both", expand=True)

# ─────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────
screens = {}
active_button = [None]


def make_sidebar_button(text: str, icon: str, screen_name: str):
    frame = tk.Frame(sidebar, bg=SIDEBAR, cursor="hand2")
    frame.pack(fill="x")

    label = tk.Label(
        frame, text=f"  {icon}  {text}", font=FONT_LABEL, bg=SIDEBAR, fg="#CCCCCC",
        anchor="w", padx=10, pady=14,
    )
    label.pack(fill="x")

    def on_enter(_):
        if active_button[0] != frame:
            frame.configure(bg=SIDEBAR_HOVER)
            label.configure(bg=SIDEBAR_HOVER)

    def on_leave(_):
        if active_button[0] != frame:
            frame.configure(bg=SIDEBAR)
            label.configure(bg=SIDEBAR)

    def on_click(_=None):
        show_screen(screen_name, frame, label)

    for widget in (frame, label):
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<Button-1>", on_click)

    return frame, label


def show_screen(name: str, button_frame, button_label):
    if active_button[0]:
        old_frame, old_label = active_button[0]
        old_frame.configure(bg=SIDEBAR)
        old_label.configure(bg=SIDEBAR, fg="#CCCCCC")

    button_frame.configure(bg=ORANGE)
    button_label.configure(bg=ORANGE, fg=WHITE)
    active_button[0] = (button_frame, button_label)

    for screen in screens.values():
        screen.pack_forget()
    screens[name].pack(fill="both", expand=True)


# ─────────────────────────────────────────
#  REUSABLE UI HELPERS
# ─────────────────────────────────────────
def page_title(parent, title: str, subtitle: str = ""):
    header = tk.Frame(parent, bg=WHITE, pady=15)
    header.pack(fill="x", padx=20, pady=(15, 0))
    tk.Label(header, text=title, font=FONT_TITLE, bg=WHITE, fg=TEXT_DARK).pack(anchor="w")
    if subtitle:
        tk.Label(header, text=subtitle, font=FONT_SMALL, bg=WHITE, fg=TEXT_GRAY).pack(anchor="w")
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=20)


def make_button(parent, text, command, bg, fg, active_bg, width=18):
    return tk.Button(
        parent, text=text, command=command, font=FONT_BUTTON, bg=bg, fg=fg,
        activebackground=active_bg, activeforeground=fg, relief="flat",
        cursor="hand2", width=width, padx=10, pady=6,
    )


def orange_button(parent, text, command, width=18):
    return make_button(parent, text, command, ORANGE, WHITE, ORANGE_DARK, width)


def gray_button(parent, text, command, width=18):
    return make_button(parent, text, command, BORDER, TEXT_DARK, "#D0D0D0", width)


def red_button(parent, text, command, width=18):
    return make_button(parent, text, command, RED, WHITE, "#B03030", width)


def input_field(parent, label_text: str, row: int, var: tk.StringVar, width: int = 30, column_offset: int = 0):
    tk.Label(parent, text=label_text, font=FONT_LABEL_BOLD, bg=WHITE, fg=TEXT_DARK).grid(
        row=row, column=column_offset, sticky="w", padx=(15, 5), pady=6
    )
    entry = tk.Entry(
        parent, textvariable=var, width=width, font=FONT_LARGE, relief="flat",
        bg=BACKGROUND, fg=TEXT_DARK, insertbackground=ORANGE,
        highlightthickness=1, highlightbackground=BORDER, highlightcolor=ORANGE,
    )
    entry.grid(row=row, column=column_offset + 1, sticky="ew", padx=(0, 15), pady=6)
    return entry


def dropdown_field(parent, label_text: str, row: int, var: tk.StringVar, values: list, width: int = 28, column_offset: int = 0):
    tk.Label(parent, text=label_text, font=FONT_LABEL_BOLD, bg=WHITE, fg=TEXT_DARK).grid(
        row=row, column=column_offset, sticky="w", padx=(15, 5), pady=6
    )
    combo = ttk.Combobox(parent, textvariable=var, values=values, width=width, state="readonly", font=FONT_LARGE)
    combo.grid(row=row, column=column_offset + 1, sticky="ew", padx=(0, 15), pady=6)
    return combo


def card(parent, padx=20, pady=10):
    """A white card with a light border, used to frame content."""
    frame = tk.Frame(parent, bg=WHITE, highlightthickness=1, highlightbackground=BORDER)
    frame.pack(fill="both", expand=True, padx=padx, pady=pady)
    return frame


def make_table(parent, columns: list[str], headings: list[str], widths: list[int], height: int = 14):
    """Create a Treeview table with a vertical scrollbar, packed into a card."""
    container = card(parent, pady=5)
    tree = ttk.Treeview(container, columns=columns, show="headings", height=height)
    for col, heading, width in zip(columns, headings, widths):
        tree.heading(col, text=heading)
        tree.column(col, width=width, anchor="center")
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return tree


# ─────────────────────────────────────────
#  SCREEN 1: INVENTORY
# ─────────────────────────────────────────
s_inventory = tk.Frame(content, bg=BACKGROUND)
screens["inventory"] = s_inventory

page_title(s_inventory, "Inventory Overview", "View and filter all raw materials and their stock status")

search_frame = tk.Frame(s_inventory, bg=BACKGROUND)
search_frame.pack(fill="x", padx=20, pady=10)
tk.Label(search_frame, text="Search:", font=FONT_LABEL_BOLD, bg=BACKGROUND, fg=TEXT_DARK).pack(side="left")
search_var = tk.StringVar()
tk.Entry(
    search_frame, textvariable=search_var, width=30, font=FONT_LARGE, relief="flat", bg=WHITE,
    highlightthickness=1, highlightbackground=BORDER, highlightcolor=ORANGE,
).pack(side="left", padx=8, ipady=4)

stats_frame = tk.Frame(s_inventory, bg=BACKGROUND)
stats_frame.pack(fill="x", padx=20, pady=(0, 5))

stat_total = tk.StringVar(value="Total: –")
stat_low = tk.StringVar(value="Low: –")
stat_ok = tk.StringVar(value="OK: –")
for var, color in [(stat_total, TEXT_GRAY), (stat_low, RED), (stat_ok, GREEN)]:
    tk.Label(stats_frame, textvariable=var, font=FONT_SMALL, bg=BACKGROUND, fg=color).pack(side="left", padx=12)

inventory_columns = ("material_id", "name", "category", "current_stock", "minimum_stock", "status")
inventory_headings = ["ID", "Name", "Category", "Current Stock", "Minimum Stock", "Status"]
inventory_widths = [80, 180, 130, 120, 120, 100]
tree_inventory = make_table(s_inventory, inventory_columns, inventory_headings, inventory_widths, height=16)
tree_inventory.tag_configure("low", background="#FFF0F0", foreground=RED)
tree_inventory.tag_configure("ok", background="#F0FFF5", foreground=GREEN)
tree_inventory.column("name", anchor="w")
tree_inventory.column("category", anchor="w")


def load_inventory(filter_text=""):
    tree_inventory.delete(*tree_inventory.get_children())
    rows = load_csv(INVENTORY_FILE)
    total = low = ok = 0
    for row in rows:
        name = row["name"]
        if filter_text.lower() not in name.lower():
            continue
        current = int(row["current_stock"])
        minimum = int(row["minimum_stock"])
        if current < minimum:
            status, tag = "⚠ Low", "low"
            low += 1
        else:
            status, tag = "✓ OK", "ok"
            ok += 1
        total += 1
        tree_inventory.insert(
            "", "end", values=(row["material_id"], name, row["category"], current, minimum, status), tags=(tag,)
        )
    stat_total.set(f"Total: {total}")
    stat_low.set(f"⚠ Low: {low}")
    stat_ok.set(f"✓ OK: {ok}")


search_var.trace_add("write", lambda *_: load_inventory(search_var.get()))
load_inventory()

# ─────────────────────────────────────────
#  SCREEN 2: PLACE ORDER
# ─────────────────────────────────────────
s_order = tk.Frame(content, bg=BACKGROUND)
screens["order"] = s_order

page_title(s_order, "Place Order", "Select a raw material, quantity and supplier")

order_form = tk.Frame(s_order, bg=WHITE, highlightthickness=1, highlightbackground=BORDER)
order_form.pack(fill="x", padx=20, pady=10)
order_form.columnconfigure(1, weight=1)

material_var = tk.StringVar()
quantity_var = tk.StringVar()
supplier_var = tk.StringVar()

material_combo = dropdown_field(order_form, "Material:", 0, material_var, [], 32)
input_field(order_form, "Quantity:", 1, quantity_var, 32)
supplier_combo = dropdown_field(order_form, "Supplier:", 2, supplier_var, [], 32)

# Rush order checkbox
rush_var = tk.BooleanVar(value=False)
rush_frame = tk.Frame(order_form, bg=WHITE)
rush_frame.grid(row=3, column=1, sticky="w", padx=15, pady=6)
tk.Checkbutton(
    rush_frame, text="Rush order", variable=rush_var, font=FONT_LABEL_BOLD, bg=WHITE, fg=RED,
    selectcolor=WHITE, activebackground=WHITE, activeforeground=RED, cursor="hand2",
).pack(side="left")
tk.Label(rush_frame, text="(Urgent delivery -- takes priority)", font=FONT_SMALL, bg=WHITE, fg=TEXT_GRAY).pack(
    side="left", padx=8
)


def refresh_order_dropdowns():
    material_combo["values"] = [r["name"] for r in load_csv(INVENTORY_FILE)]
    supplier_combo["values"] = [r["name"] for r in load_csv(SUPPLIERS_FILE)]


refresh_order_dropdowns()

# Stock info label, updates when a material is chosen
order_info_var = tk.StringVar(value="")
tk.Label(order_form, textvariable=order_info_var, font=FONT_SMALL, bg=WHITE, fg=TEXT_GRAY).grid(
    row=4, column=1, sticky="w", padx=15, pady=4
)


def update_order_info(*_):
    name = material_var.get()
    for row in load_csv(INVENTORY_FILE):
        if row["name"] == name:
            order_info_var.set(f"Current: {row['current_stock']} | Minimum: {row['minimum_stock']}")
            return
    order_info_var.set("")


material_var.trace_add("write", update_order_info)


def place_order():
    material = material_var.get()
    quantity = quantity_var.get()
    supplier = supplier_var.get()

    if not material:
        messagebox.showwarning("Error", "Please select a material.")
        return
    if not supplier:
        messagebox.showwarning("Error", "Please select a supplier.")
        return
    if not quantity.isdigit() or int(quantity) <= 0:
        messagebox.showwarning("Error", "Quantity must be a positive number.")
        return

    orders = load_csv(ORDERS_FILE)
    new_id = str(len(orders) + 1)
    rush = "Yes" if rush_var.get() else "No"
    orders.append(
        {
            "order_id": new_id,
            "material": material,
            "quantity": quantity,
            "supplier": supplier,
            "status": "Rush - Processing" if rush == "Yes" else "Processing",
            "rush": rush,
        }
    )
    save_csv(ORDERS_FILE, orders, ["order_id", "material", "quantity", "supplier", "status", "rush"])

    rush_note = " (RUSH)" if rush == "Yes" else ""
    messagebox.showinfo("Order placed", f"Order for {material} ({quantity} units) has been placed{rush_note}!")
    reset_order_form()
    load_orders()


def reset_order_form():
    material_var.set("")
    quantity_var.set("")
    supplier_var.set("")
    order_info_var.set("")
    rush_var.set(False)


order_buttons = tk.Frame(order_form, bg=WHITE)
order_buttons.grid(row=5, column=0, columnspan=2, pady=12, padx=15, sticky="w")
orange_button(order_buttons, "✓  Place order", place_order).pack(side="left", padx=(0, 8))
gray_button(order_buttons, "✕  Cancel", reset_order_form, 14).pack(side="left")

# Order history
tk.Label(s_order, text="Order History", font=FONT_SUBTITLE, bg=BACKGROUND, fg=TEXT_DARK).pack(
    anchor="w", padx=20, pady=(10, 2)
)

order_columns = ("order_id", "material", "quantity", "supplier", "status", "rush")
order_headings = ["ID", "Material", "Quantity", "Supplier", "Status", "Rush"]
order_widths = [60, 140, 90, 160, 160, 70]
tree_orders = make_table(s_order, order_columns, order_headings, order_widths, height=8)
tree_orders.tag_configure("processing", foreground="#E07000")
tree_orders.tag_configure("delivered", foreground=GREEN)
tree_orders.tag_configure("shipped", foreground="#2060CC")


def load_orders():
    tree_orders.delete(*tree_orders.get_children())
    for row in load_csv(ORDERS_FILE):
        status = row.get("status", "")
        rush = row.get("rush", "No")
        status_lower = status.lower()
        if "processing" in status_lower:
            tag = "processing"
        elif "delivered" in status_lower:
            tag = "delivered"
        else:
            tag = "shipped"
        tree_orders.insert(
            "", "end",
            values=(row.get("order_id", ""), row.get("material", ""), row.get("quantity", ""),
                    row.get("supplier", ""), status, rush),
            tags=(tag,),
        )


load_orders()

# ─────────────────────────────────────────
#  SCREEN 3: SUPPLIERS
# ─────────────────────────────────────────
s_suppliers = tk.Frame(content, bg=BACKGROUND)
screens["suppliers"] = s_suppliers

page_title(s_suppliers, "Suppliers", "View, edit and manage suppliers")

supplier_columns = ("supplier_id", "name", "email", "phone", "contact_person")
supplier_headings = ["ID", "Name", "Email", "Phone", "Contact Person"]
supplier_widths = [50, 180, 200, 130, 160]
tree_suppliers = make_table(s_suppliers, supplier_columns, supplier_headings, supplier_widths, height=14)
for col in ("name", "email", "phone", "contact_person"):
    tree_suppliers.column(col, anchor="w")
tree_suppliers.column("supplier_id", anchor="center", width=50)


def load_suppliers():
    tree_suppliers.delete(*tree_suppliers.get_children())
    for row in load_csv(SUPPLIERS_FILE):
        tree_suppliers.insert("", "end", values=tuple(row[k] for k in supplier_columns))


load_suppliers()

supplier_buttons = tk.Frame(s_suppliers, bg=BACKGROUND)
supplier_buttons.pack(fill="x", padx=20, pady=8)


def edit_supplier():
    selected = tree_suppliers.selection()
    if not selected:
        messagebox.showwarning("Error", "Please select a supplier first.")
        return
    supplier_id, name, email, phone, contact_person = tree_suppliers.item(selected[0])["values"]

    popup = tk.Toplevel(window)
    popup.title(f"Edit: {name}")
    popup.geometry("450x300")
    popup.configure(bg=WHITE)
    popup.resizable(False, False)
    popup.grab_set()

    tk.Frame(popup, bg=ORANGE, height=6).pack(fill="x")
    tk.Label(popup, text="Edit Supplier", font=FONT_SUBTITLE, bg=WHITE, fg=TEXT_DARK).pack(
        anchor="w", padx=20, pady=(15, 5)
    )

    form = tk.Frame(popup, bg=WHITE)
    form.pack(fill="both", expand=True)
    form.columnconfigure(1, weight=1)

    fields = [("Name:", name), ("Email:", email), ("Phone:", phone), ("Contact Person:", contact_person)]
    field_vars = []
    for i, (label, value) in enumerate(fields):
        var = tk.StringVar(value=value)
        input_field(form, label, i, var, 28)
        field_vars.append(var)

    def save():
        new_name, new_email, new_phone, new_contact = (v.get().strip() for v in field_vars)
        if not new_name:
            messagebox.showwarning("Error", "Name cannot be empty.", parent=popup)
            return
        rows = load_csv(SUPPLIERS_FILE)
        for row in rows:
            if str(row["supplier_id"]) == str(supplier_id):
                row["name"] = new_name
                row["email"] = new_email
                row["phone"] = new_phone
                row["contact_person"] = new_contact
        save_csv(SUPPLIERS_FILE, rows, list(supplier_columns))
        popup.destroy()
        load_suppliers()
        refresh_order_dropdowns()
        messagebox.showinfo("Success", f"'{new_name}' has been updated!")

    button_row = tk.Frame(form, bg=WHITE)
    button_row.grid(row=4, column=0, columnspan=2, pady=12, padx=15, sticky="w")
    orange_button(button_row, "✓  Save", save, 14).pack(side="left", padx=(0, 8))
    gray_button(button_row, "✕  Cancel", popup.destroy, 12).pack(side="left")


def delete_supplier():
    selected = tree_suppliers.selection()
    if not selected:
        messagebox.showwarning("Error", "Please select a supplier first.")
        return
    name = tree_suppliers.item(selected[0])["values"][1]
    if not messagebox.askyesno("Confirm", f"Delete supplier '{name}'?"):
        return
    rows = [r for r in load_csv(SUPPLIERS_FILE) if r["name"] != name]
    save_csv(SUPPLIERS_FILE, rows, list(supplier_columns))
    load_suppliers()
    refresh_order_dropdowns()


orange_button(supplier_buttons, "✎  Edit", edit_supplier, 20).pack(side="left", padx=(0, 8))
red_button(supplier_buttons, "✕  Delete", delete_supplier, 20).pack(side="left")

# ─────────────────────────────────────────
#  SCREEN 4: UPDATE STOCK
# ─────────────────────────────────────────
s_update = tk.Frame(content, bg=BACKGROUND)
screens["update"] = s_update

page_title(s_update, "Update Stock", "Adjust the current stock level of a raw material")

update_form = tk.Frame(s_update, bg=WHITE, highlightthickness=1, highlightbackground=BORDER)
update_form.pack(fill="x", padx=20, pady=15)
update_form.columnconfigure(1, weight=1)

update_material_var = tk.StringVar()
update_stock_var = tk.StringVar()

update_combo = dropdown_field(update_form, "Material:", 0, update_material_var, [], 32)
input_field(update_form, "New stock level:", 1, update_stock_var, 32)

update_info_var = tk.StringVar(value="")
tk.Label(update_form, textvariable=update_info_var, font=FONT_SMALL, bg=WHITE, fg=TEXT_GRAY).grid(
    row=2, column=1, sticky="w", padx=15, pady=2
)


def refresh_update_info(*_):
    name = update_material_var.get()
    for row in load_csv(INVENTORY_FILE):
        if row["name"] == name:
            update_info_var.set(f"Current: {row['current_stock']} | Minimum: {row['minimum_stock']}")
            return
    update_info_var.set("")


update_material_var.trace_add("write", refresh_update_info)


def refresh_update_dropdown():
    update_combo["values"] = [r["name"] for r in load_csv(INVENTORY_FILE)]


refresh_update_dropdown()


def clear_update_form():
    update_material_var.set("")
    update_stock_var.set("")
    update_info_var.set("")


def save_stock_update():
    name = update_material_var.get()
    value = update_stock_var.get()
    if not name:
        messagebox.showwarning("Error", "Please select a material.")
        return
    if not value.isdigit() or int(value) < 0:
        messagebox.showwarning("Error", "Stock must be a positive number.")
        return
    rows = load_csv(INVENTORY_FILE)
    for row in rows:
        if row["name"] == name:
            row["current_stock"] = value
    save_csv(INVENTORY_FILE, rows, ["material_id", "name", "current_stock", "minimum_stock", "category"])
    messagebox.showinfo("Success", f"Stock for '{name}' updated to {value}.")
    clear_update_form()
    load_inventory()


update_buttons = tk.Frame(update_form, bg=WHITE)
update_buttons.grid(row=3, column=0, columnspan=2, pady=12, padx=15, sticky="w")
orange_button(update_buttons, "✓  Update", save_stock_update, 16).pack(side="left", padx=(0, 8))
gray_button(update_buttons, "✕  Clear", clear_update_form, 12).pack(side="left")

# ─────────────────────────────────────────
#  SCREEN 5: REPORTS
# ─────────────────────────────────────────
s_report = tk.Frame(content, bg=BACKGROUND)
screens["report"] = s_report

page_title(s_report, "Generate Report", "Generate a summary report of inventory and orders")

report_choice_frame = tk.Frame(s_report, bg=BACKGROUND)
report_choice_frame.pack(fill="x", padx=20, pady=10)

report_type_var = tk.StringVar(value="inventory")


def style_report_buttons():
    if report_type_var.get() == "inventory":
        inventory_report_button.configure(bg=ORANGE, fg=WHITE)
        orders_report_button.configure(bg=BORDER, fg=TEXT_DARK)
    else:
        inventory_report_button.configure(bg=BORDER, fg=TEXT_DARK)
        orders_report_button.configure(bg=ORANGE, fg=WHITE)
    generate_report_preview()


inventory_report_button = tk.Button(
    report_choice_frame, text="Inventory report", font=FONT_BUTTON, bg=ORANGE, fg=WHITE, relief="flat",
    cursor="hand2", padx=15, pady=6,
    command=lambda: [report_type_var.set("inventory"), style_report_buttons()],
)
inventory_report_button.pack(side="left", padx=(0, 8))

orders_report_button = tk.Button(
    report_choice_frame, text="Orders report", font=FONT_BUTTON, bg=BORDER, fg=TEXT_DARK, relief="flat",
    cursor="hand2", padx=15, pady=6,
    command=lambda: [report_type_var.set("orders"), style_report_buttons()],
)
orders_report_button.pack(side="left")

# Preview text box
report_preview_card = card(s_report, pady=5)
report_text = tk.Text(
    report_preview_card, font=("Courier New", 10), bg=WHITE, fg=TEXT_DARK, relief="flat",
    wrap="none", state="disabled", padx=15, pady=10,
)
report_scroll_y = ttk.Scrollbar(report_preview_card, orient="vertical", command=report_text.yview)
report_scroll_x = ttk.Scrollbar(report_preview_card, orient="horizontal", command=report_text.xview)
report_text.configure(yscrollcommand=report_scroll_y.set, xscrollcommand=report_scroll_x.set)
report_scroll_y.pack(side="right", fill="y")
report_scroll_x.pack(side="bottom", fill="x")
report_text.pack(fill="both", expand=True)


def build_inventory_report_lines() -> list[str]:
    lines = [
        "  INVENTORY REPORT",
        "-" * 60,
        f"  {'Name':<25} {'Category':<15} {'Current':>8} {'Minimum':>8} {'Status':<10}",
        "-" * 60,
    ]
    rows = load_csv(INVENTORY_FILE)
    low_count = 0
    for row in rows:
        current = int(row["current_stock"])
        minimum = int(row["minimum_stock"])
        status = "LOW" if current < minimum else "OK"
        if current < minimum:
            low_count += 1
        lines.append(f"  {row['name']:<25} {row['category']:<15} {current:>8} {minimum:>8} {status:<10}")
    lines += [
        "-" * 60,
        f"  Total materials     : {len(rows)}",
        f"  Below minimum       : {low_count}",
        f"  Status OK           : {len(rows) - low_count}",
    ]
    return lines


def build_orders_report_lines() -> list[str]:
    lines = [
        "  ORDERS REPORT",
        "-" * 60,
        f"  {'ID':>4}  {'Material':<20} {'Quantity':>10} {'Supplier':<22} {'Status':<15}",
        "-" * 60,
    ]
    rows = load_csv(ORDERS_FILE)
    status_counts = {}
    for row in rows:
        status = row["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
        lines.append(
            f"  {row['order_id']:>4}  {row['material']:<20} {row['quantity']:>10} "
            f"{row['supplier']:<22} {status:<15}"
        )
    lines += ["-" * 60, f"  Total orders         : {len(rows)}"]
    lines += [f"  {status:<20} : {count}" for status, count in status_counts.items()]
    return lines


def generate_report_preview():
    """Build the report text and display it in the preview box."""
    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    header = ["=" * 60, "  EUROCAPS -- RAW MATERIAL & ORDER MANAGEMENT", "=" * 60, f"  Report generated on: {now}", ""]
    body = build_inventory_report_lines() if report_type_var.get() == "inventory" else build_orders_report_lines()
    footer = ["", "=" * 60, "  End of report", "=" * 60]
    lines = header + body + footer

    report_text.configure(state="normal")
    report_text.delete("1.0", "end")
    report_text.insert("end", "\n".join(lines))
    report_text.configure(state="disabled")


def save_report_to_file():
    filename = f"report_{report_type_var.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    content_ = report_text.get("1.0", "end")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content_)
    messagebox.showinfo("Saved", f"Report saved as:\n{filename}")


generate_report_preview()

report_buttons = tk.Frame(s_report, bg=BACKGROUND)
report_buttons.pack(fill="x", padx=20, pady=8)
orange_button(report_buttons, "Refresh report", generate_report_preview, 20).pack(side="left", padx=(0, 8))
gray_button(report_buttons, "Save as .txt", save_report_to_file, 18).pack(side="left")

# ─────────────────────────────────────────
#  BUILD SIDEBAR NAVIGATION BUTTONS
# ─────────────────────────────────────────
tk.Frame(sidebar, bg=SIDEBAR, height=10).pack()

nav_items = [
    ("Inventory", "📦", "inventory"),
    ("Place Order", "🛒", "order"),
    ("Suppliers", "🏭", "suppliers"),
    ("Update Stock", "✏", "update"),
    ("Reports", "📊", "report"),
]

first_nav_button = None
for label, icon, screen_name in nav_items:
    btn_frame, btn_label = make_sidebar_button(label, icon, screen_name)
    if first_nav_button is None:
        first_nav_button = (screen_name, btn_frame, btn_label)

tk.Frame(sidebar, bg="#333333", height=1).pack(fill="x", pady=20)
tk.Label(sidebar, text="v1.0  •  Eurocaps 2026", font=("Trebuchet MS", 8), bg=SIDEBAR, fg="#555555").pack()

# ─────────────────────────────────────────
#  LOGIN SCREEN
# ─────────────────────────────────────────
def show_login_screen():
    main_frame.pack_forget()

    login_frame = tk.Frame(window, bg=WHITE)
    login_frame.pack(fill="both", expand=True)
    tk.Frame(login_frame, bg=ORANGE, height=8).pack(fill="x")

    center = tk.Frame(login_frame, bg=WHITE)
    center.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(center, text="EUROCAPS", font=("Georgia", 28, "bold"), bg=WHITE, fg=ORANGE).pack(pady=(0, 4))
    tk.Label(
        center, text="Raw Material & Order Management", font=("Trebuchet MS", 11), bg=WHITE, fg=TEXT_GRAY
    ).pack()
    tk.Frame(center, bg=BORDER, height=1, width=320).pack(pady=20)

    tk.Label(center, text="Username", font=FONT_LABEL_BOLD, bg=WHITE, fg=TEXT_DARK, anchor="w").pack(fill="x")
    username_var = tk.StringVar()
    username_entry = tk.Entry(
        center, textvariable=username_var, width=35, font=FONT_LARGE, relief="flat", bg=BACKGROUND,
        highlightthickness=1, highlightbackground=BORDER, highlightcolor=ORANGE,
    )
    username_entry.pack(pady=(4, 12), ipady=6)

    tk.Label(center, text="Password", font=FONT_LABEL_BOLD, bg=WHITE, fg=TEXT_DARK, anchor="w").pack(fill="x")
    password_var = tk.StringVar()
    password_entry = tk.Entry(
        center, textvariable=password_var, width=35, font=FONT_LARGE, relief="flat", bg=BACKGROUND,
        highlightthickness=1, highlightbackground=BORDER, highlightcolor=ORANGE, show="*",
    )
    password_entry.pack(pady=(4, 4), ipady=6)

    error_var = tk.StringVar(value="")
    tk.Label(center, textvariable=error_var, font=FONT_SMALL, bg=WHITE, fg=RED).pack(pady=(4, 12))

    def check_login(_event=None):
        if username_var.get() == LOGIN_USERNAME and password_var.get() == LOGIN_PASSWORD:
            login_frame.destroy()
            main_frame.pack(fill="both", expand=True)
            screen_name, btn_frame, btn_label = first_nav_button
            show_screen(screen_name, btn_frame, btn_label)
        else:
            error_var.set("Incorrect username or password.")
            password_var.set("")
            password_entry.focus()

    tk.Button(
        center, text="Log in", command=check_login, font=FONT_BUTTON, bg=ORANGE, fg=WHITE,
        activebackground=ORANGE_DARK, activeforeground=WHITE, relief="flat", cursor="hand2", width=30, pady=8,
    ).pack()

    window.bind("<Return>", check_login)
    username_entry.focus()


show_login_screen()
window.mainloop()