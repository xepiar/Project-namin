import customtkinter as ctk
from db_helper import (
    get_all_sales,
    get_all_menu_items,
    add_menu_item,
    update_menu_item,
    delete_menu_item
)

class AdminPortal(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.selected_item_id = None
        self._build_dashboard()

    def _build_dashboard(self):

        top_bar = ctk.CTkFrame(self, height=60)
        top_bar.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            top_bar,
            text="📊 ADMIN MANAGEMENT DASHBOARD",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFA500"
        ).pack(side="left", padx=15, pady=10)

        ctk.CTkButton(
            top_bar,
            text="Logout",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=80,
            command=self.app.show_auth_selection
        ).pack(side="right", padx=15)


        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.tab_sales = self.tabview.add("Sales History")
        self.tab_menu = self.tabview.add("ADMIN MANAGEMENT")

        self._build_sales_tab()
        self._build_menu_crud_tab()

   #SALE HISTORY
    def _build_sales_tab(self):
        sales = get_all_sales()


        total_revenue = 0.0
        for s in sales:
            if isinstance(s, dict):
                total_revenue += float(s.get("total_amount", s.get("total", 0.0)))
            elif isinstance(s, (tuple, list)):
                total_revenue += float(s[3]) if len(s) > 3 else 0.0

        total_orders = len(sales)

        cards_frame = ctk.CTkFrame(self.tab_sales, fg_color="transparent")
        cards_frame.pack(fill="x", padx=10, pady=10)

        c1 = ctk.CTkFrame(cards_frame, fg_color="#1e1e1e", height=80)
        c1.pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkLabel(c1, text="Total Revenue", font=ctk.CTkFont(size=12)).pack(pady=(10, 0))
        ctk.CTkLabel(c1, text=f"₱{total_revenue:.2f}", font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="#2ECC71").pack(pady=(0, 10))

        c2 = ctk.CTkFrame(cards_frame, fg_color="#1e1e1e", height=80)
        c2.pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkLabel(c2, text="Completed Orders", font=ctk.CTkFont(size=12)).pack(pady=(10, 0))
        ctk.CTkLabel(c2, text=str(total_orders), font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(0, 10))

        logs_box = ctk.CTkScrollableFrame(self.tab_sales, label_text="Sales History Log (MySQL)")
        logs_box.pack(fill="both", expand=True, padx=10, pady=10)

        for s in sales:
            row = ctk.CTkFrame(logs_box, fg_color="#2b2b2b")
            row.pack(fill="x", pady=4, padx=5)

            if isinstance(s, dict):
                order_id = s.get("order_id", "")
                cust = s.get("customer_name", "Guest")
                time_stamp = s.get("timestamp", "")
                amount = float(s.get("total_amount", 0.0))
            else:
                order_id = s[0]
                cust = s[1]
                time_stamp = s[2]
                amount = float(s[3])

            ctk.CTkLabel(row, text=f"Order #{order_id}", font=ctk.CTkFont(size=11, weight="bold"), text_color="#FFA500").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"[{time_stamp}]", font=ctk.CTkFont(size=11), text_color="#AAA").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"Customer: {cust}", font=ctk.CTkFont(size=12)).pack(side="left", padx=15)
            ctk.CTkLabel(row, text=f"₱{amount:.2f}", font=ctk.CTkFont(weight="bold"), text_color="#2ECC71").pack(side="right", padx=10)

    #CRUD NATIN
    def _build_menu_crud_tab(self):
        self.tab_menu.grid_columnconfigure(0, weight=1)
        self.tab_menu.grid_columnconfigure(1, weight=1)
        self.tab_menu.grid_rowconfigure(0, weight=1)

        #ITEM LIST
        left_box = ctk.CTkFrame(self.tab_menu)
        left_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        left_box.grid_rowconfigure(1, weight=1)
        left_box.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left_box, text="Current Menu Items", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.item_list_scroll = ctk.CTkScrollableFrame(left_box)
        self.item_list_scroll.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        #CREATE UPDATE DELETE
        right_box = ctk.CTkFrame(self.tab_menu, fg_color="#1e1e1e")
        right_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(right_box, text="Item Management Form", font=ctk.CTkFont(size=16, weight="bold"), text_color="#FFA500").pack(pady=(15, 10))

        ctk.CTkLabel(right_box, text="Item Name:").pack(anchor="w", padx=20, pady=(5, 0))
        self.entry_name = ctk.CTkEntry(right_box, placeholder_text="e.g. Wintermelon")
        self.entry_name.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(right_box, text="Price (₱):").pack(anchor="w", padx=20, pady=(5, 0))
        self.entry_price = ctk.CTkEntry(right_box, placeholder_text="29.00")
        self.entry_price.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(right_box, text="Category:").pack(anchor="w", padx=20, pady=(5, 0))
        self.combo_category = ctk.CTkComboBox(right_box, values=["Milk Tea", "Iced Coffee", "Fruit Tea"])
        self.combo_category.pack(fill="x", padx=20, pady=(0, 15))

        self.status_lbl = ctk.CTkLabel(right_box, text="", font=ctk.CTkFont(size=12))
        self.status_lbl.pack(pady=5)


        btn_box = ctk.CTkFrame(right_box, fg_color="transparent")
        btn_box.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(btn_box, text="➕ Add New", fg_color="#2ECC71", hover_color="#27AE60", command=self._add_item).pack(fill="x", pady=4)
        ctk.CTkButton(btn_box, text="✏️ Update Selected", fg_color="#F39C12", hover_color="#D68910", command=self._update_item).pack(fill="x", pady=4)
        ctk.CTkButton(btn_box, text="🗑️ Delete Selected", fg_color="#E74C3C", hover_color="#C0392B", command=self._delete_item).pack(fill="x", pady=4)
        ctk.CTkButton(btn_box, text="🔄 Clear Selection", fg_color="#555", hover_color="#666", command=self._clear_form).pack(fill="x", pady=4)

        self._refresh_menu_list()

    def _refresh_menu_list(self):
        for widget in self.item_list_scroll.winfo_children():
            widget.destroy()

        items = get_all_menu_items()
        for item in items:
            item_id, name, price, category = item
            frame = ctk.CTkFrame(self.item_list_scroll, fg_color="#2b2b2b")
            frame.pack(fill="x", pady=3, padx=2)

            info_str = f"[{category}] {name} - ₱{float(price):.2f}"
            lbl = ctk.CTkLabel(frame, text=info_str, font=ctk.CTkFont(size=12))
            lbl.pack(side="left", padx=10, pady=5)

            select_btn = ctk.CTkButton(
                frame,
                text="Select",
                width=60,
                height=24,
                fg_color="#3498DB",
                hover_color="#2980B9",
                command=lambda i=item_id, n=name, p=price, c=category: self._populate_form(i, n, p, c)
            )
            select_btn.pack(side="right", padx=5, pady=5)

    def _populate_form(self, item_id, name, price, category):
        self.selected_item_id = item_id
        self.entry_name.delete(0, "end")
        self.entry_name.insert(0, name)
        self.entry_price.delete(0, "end")
        self.entry_price.insert(0, str(price))
        self.combo_category.set(category)
        self.status_lbl.configure(text=f"Editing Item ID #{item_id}", text_color="#3498DB")

    def _clear_form(self):
        self.selected_item_id = None
        self.entry_name.delete(0, "end")
        self.entry_price.delete(0, "end")
        self.combo_category.set("Milk Tea")
        self.status_lbl.configure(text="", text_color="white")

    def _add_item(self):
        name = self.entry_name.get().strip()
        price_str = self.entry_price.get().strip()
        category = self.combo_category.get()

        if not name or not price_str:
            self.status_lbl.configure(text="Please fill in all fields!", text_color="#E74C3C")
            return

        try:
            price = float(price_str)
        except ValueError:
            self.status_lbl.configure(text="Invalid price format!", text_color="#E74C3C")
            return

        if add_menu_item(name, price, category):
            self.status_lbl.configure(text="Item added successfully!", text_color="#2ECC71")
            self._clear_form()
            self._refresh_menu_list()
        else:
            self.status_lbl.configure(text="Failed to add item to DB.", text_color="#E74C3C")

    def _update_item(self):
        if self.selected_item_id is None:
            self.status_lbl.configure(text="Select an item to update first!", text_color="#E74C3C")
            return

        name = self.entry_name.get().strip()
        price_str = self.entry_price.get().strip()
        category = self.combo_category.get()

        try:
            price = float(price_str)
        except ValueError:
            self.status_lbl.configure(text="Invalid price format!", text_color="#E74C3C")
            return

        if update_menu_item(self.selected_item_id, name, price, category):
            self.status_lbl.configure(text="Item updated successfully!", text_color="#2ECC71")
            self._clear_form()
            self._refresh_menu_list()
        else:
            self.status_lbl.configure(text="Failed to update item.", text_color="#E74C3C")

    def _delete_item(self):
        if self.selected_item_id is None:
            self.status_lbl.configure(text="Select an item to delete first!", text_color="#E74C3C")
            return

        if delete_menu_item(self.selected_item_id):
            self.status_lbl.configure(text="Item deleted successfully!", text_color="#2ECC71")
            self._clear_form()
            self._refresh_menu_list()
        else:
            self.status_lbl.configure(text="Failed to delete item.", text_color="#E74C3C")