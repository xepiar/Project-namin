import customtkinter as ctk
from tkinter import messagebox

SIZE_MODIFIERS = {
    "Medium (16oz) [-₱5.00]": -5.0,
    "Large (22oz) [₱0.00]": 0.0,
    "Jumbo (1L) [+₱20.00]": 20.0,
}

class CustomerView(ctk.CTkFrame):
    def __init__(self, parent, controller, product_mgr, sales_mgr):
        super().__init__(parent)
        self.controller = controller
        self.product_mgr = product_mgr
        self.sales_mgr = sales_mgr

        self.customer_name = "Guest"
        self.current_order = []
        self.selected_item = None

        self.show_login()

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self._clear()
        card = ctk.CTkFrame(self, corner_radius=15, width=400, height=350)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Customer Portal", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FFA500").pack(pady=(30, 10))
        ctk.CTkLabel(card, text="Enter your name for the order receipt:").pack(pady=5)

        entry = ctk.CTkEntry(card, width=260)
        entry.pack(pady=15)

        def proceed():
            self.customer_name = entry.get().strip() or "Guest Customer"
            self.build_pos_interface()

        ctk.CTkButton(card, text="Start Ordering", fg_color="#FFA500", text_color="black", width=260, command=proceed).pack(pady=10)
        ctk.CTkButton(card, text="← Back to Role Select", fg_color="transparent", command=self.controller.show_auth_selection).pack(pady=5)

    def build_pos_interface(self):
        self._clear()
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(self)
        left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        top_box = ctk.CTkFrame(left, fg_color="transparent")
        top_box.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(top_box, text=f"Welcome, {self.customer_name}", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        ctk.CTkButton(top_box, text="Switch Access", width=100, fg_color="#333", command=self.controller.show_auth_selection).pack(side="right")

        scroll = ctk.CTkScrollableFrame(left, label_text="Available Items")
        scroll.pack(fill="both", expand=True, padx=10, pady=5)

        prods = self.product_mgr.get_all_products()
        for p in prods:
            btn = ctk.CTkButton(scroll, text=f"{p['name']}\n₱{p['base_price']:.2f}",
                                 command=lambda item=p: self._select_product(item))
            btn.pack(fill="x", pady=4, padx=5)

        ctrl = ctk.CTkFrame(left)
        ctrl.pack(fill="x", padx=10, pady=10)

        self.size_var = ctk.StringVar(value="Large (22oz) [₱0.00]")
        ctk.CTkOptionMenu(ctrl, values=list(SIZE_MODIFIERS.keys()), variable=self.size_var).pack(side="left", padx=5)

        self.add_btn = ctk.CTkButton(ctrl, text="Select Item First", state="disabled", command=self._add_to_cart)
        self.add_btn.pack(side="right", padx=5)

        right = ctk.CTkFrame(self)
        right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(right, text="Order Cart", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        self.cart_box = ctk.CTkScrollableFrame(right)
        self.cart_box.pack(fill="both", expand=True, padx=10, pady=5)

        self.tot_lbl = ctk.CTkLabel(right, text="Total: ₱0.00", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2ECC71")
        self.tot_lbl.pack(pady=5)

        pay_box = ctk.CTkFrame(right)
        pay_box.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(pay_box, text="Cash Tendered: ₱").pack(side="left")
        self.cash_ent = ctk.CTkEntry(pay_box, width=100)
        self.cash_ent.pack(side="left", padx=5)

        ctk.CTkButton(right, text="Checkout & Save to DB", fg_color="#2ECC71", command=self._checkout).pack(pady=10, padx=10, fill="x")

    def _select_product(self, product):
        self.selected_item = product
        self.add_btn.configure(state="normal", text=f"Add {product['name']}")

    def _add_to_cart(self):
        if not self.selected_item:
            return
        adj = SIZE_MODIFIERS[self.size_var.get()]
        final_price = float(self.selected_item['base_price']) + adj

        self.current_order.append({
            "name": self.selected_item['name'],
            "price": final_price
        })
        self._render_cart()

    def _render_cart(self):
        for w in self.cart_box.winfo_children():
            w.destroy()
        tot = 0
        for item in self.current_order:
            r = ctk.CTkFrame(self.cart_box)
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=item['name']).pack(side="left", padx=5)
            ctk.CTkLabel(r, text=f"₱{item['price']:.2f}").pack(side="right", padx=5)
            tot += item['price']

        self.tot_lbl.configure(text=f"Total: ₱{tot:.2f}")

    def _checkout(self):
        tot = sum(i['price'] for i in self.current_order)
        if tot == 0:
            return
        try:
            cash = float(self.cash_ent.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Cash Input!")
            return

        if cash < tot:
            messagebox.showerror("Error", "Insufficient Cash!")
            return

        change = cash - tot
        if self.sales_mgr.record_sale(self.customer_name, tot, cash, change):
            messagebox.showinfo("Receipt", f"Transaction Saved to Database!\nCustomer: {self.customer_name}\nTotal: ₱{tot:.2f}\nCash: ₱{cash:.2f}\nChange: ₱{change:.2f}")
            self.current_order = []
            self.cash_ent.delete(0, "end")
            self._render_cart()

