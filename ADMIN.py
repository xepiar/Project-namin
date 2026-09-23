import customtkinter as ctk
from tkinter import messagebox, ttk

class AdminView(ctk.CTkFrame):
    def __init__(self, parent, controller, product_mgr, sales_mgr):
        super().__init__(parent)
        self.controller = controller
        self.product_mgr = product_mgr
        self.sales_mgr = sales_mgr

        self.show_login()

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self._clear()
        card = ctk.CTkFrame(self, corner_radius=15, width=400, height=350)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Admin Portal Login", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(30, 10))
        pass_entry = ctk.CTkEntry(card, width=260, show="*")
        pass_entry.pack(pady=15)

        def verify():
            if pass_entry.get() == "BIGBREW":
                self.build_admin_portal()
            else:
                messagebox.showerror("Access Denied", "Invalid Admin Password!")

        ctk.CTkButton(card, text="Login", fg_color="#2ECC71", width=260, command=verify).pack(pady=10)
        ctk.CTkButton(card, text="← Back to Role Select", fg_color="transparent", command=self.controller.show_auth_selection).pack(pady=5)

    def build_admin_portal(self):
        self._clear()

        top_bar = ctk.CTkFrame(self, height=50)
        top_bar.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(top_bar, text="📊 ADMIN CONTROL CENTER", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FFA500").pack(side="left", padx=15)
        ctk.CTkButton(top_bar, text="Logout", fg_color="#E74C3C", width=80, command=self.controller.show_auth_selection).pack(side="right", padx=15)

        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        tab_inventory = tabview.add("Product Inventory (CRUD)")
        tab_sales = tabview.add("Sales Analytics")

        # --- PRODUCT CRUD PANEL ---
        left_crud = ctk.CTkFrame(tab_inventory, width=320)
        left_crud.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(left_crud, text="Manage Product Record", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        cat_var = ctk.StringVar(value="Milk Tea")
        ctk.CTkOptionMenu(left_crud, values=["Milk Tea", "Iced Coffee", "Fruit Tea"], variable=cat_var).pack(pady=5, padx=15, fill="x")

        name_ent = ctk.CTkEntry(left_crud, placeholder_text="Product Name")
        name_ent.pack(pady=5, padx=15, fill="x")

        price_ent = ctk.CTkEntry(left_crud, placeholder_text="Base Price (₱)")
        price_ent.pack(pady=5, padx=15, fill="x")

        selected_prod_id = [None]

        right_table = ctk.CTkFrame(tab_inventory)
        right_table.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        columns = ("ID", "Category", "Name", "Base Price")
        tree = ttk.Treeview(right_table, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)

        def refresh_table():
            for r in tree.get_children():
                tree.delete(r)
            for p in self.product_mgr.get_all_products():
                tree.insert("", "end", values=(p['product_id'], p['category'], p['name'], f"₱{p['base_price']:.2f}"))

        def on_select(event):
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])['values']
                selected_prod_id[0] = item[0]
                cat_var.set(item[1])
                name_ent.delete(0, "end")
                name_ent.insert(0, item[2])
                price_ent.delete(0, "end")
                price_ent.insert(0, str(item[3]).replace("₱", ""))

        tree.bind("<<TreeviewSelect>>", on_select)

        def add_item():
            try:
                p = float(price_ent.get())
                if self.product_mgr.add_product(cat_var.get(), name_ent.get(), p):
                    messagebox.showinfo("Success", "Product added successfully!")
                    refresh_table()
            except ValueError:
                messagebox.showerror("Error", "Invalid price value!")

        def update_item():
            if not selected_prod_id[0]:
                return
            try:
                p = float(price_ent.get())
                if self.product_mgr.update_product(selected_prod_id[0], name_ent.get(), p):
                    messagebox.showinfo("Success", "Product updated!")
                    refresh_table()
            except ValueError:
                messagebox.showerror("Error", "Invalid price value!")

        def delete_item():
            if not selected_prod_id[0]:
                return
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
                if self.product_mgr.delete_product(selected_prod_id[0]):
                    messagebox.showinfo("Deleted", "Product removed.")
                    refresh_table()

        ctk.CTkButton(left_crud, text="➕ Create Record", fg_color="#2ECC71", command=add_item).pack(pady=5, padx=15, fill="x")
        ctk.CTkButton(left_crud, text="✏️ Update Selected", fg_color="#3498DB", command=update_item).pack(pady=5, padx=15, fill="x")
        ctk.CTkButton(left_crud, text="🗑️ Delete Selected", fg_color="#E74C3C", command=delete_item).pack(pady=5, padx=15, fill="x")

        refresh_table()

        # --- SALES ANALYTICS PANEL ---
        sales = self.sales_mgr.get_sales_summary()
        total_rev = sum(s['total_amount'] for s in sales)

        ctk.CTkLabel(tab_sales, text=f"Total System Revenue: ₱{total_rev:.2f}", font=ctk.CTkFont(size=18, weight="bold"), text_color="#2ECC71").pack(pady=15)
        sales_box = ctk.CTkScrollableFrame(tab_sales)
        sales_box.pack(fill="both", expand=True, padx=10, pady=10)

        for s in sales:
            r = ctk.CTkFrame(sales_box)
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=f"[{s['created_at']}] Customer: {s['customer_name']}").pack(side="left", padx=10)
            ctk.CTkLabel(r, text=f"₱{s['total_amount']:.2f}", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=10)