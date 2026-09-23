import customtkinter as ctk
from CUSTOMER import CustomerView
from ADMIN import AdminView
#from models import ProductManager, SalesManager

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BigBrew POS & Management System")
        self.geometry("1100x720")
        self.minsize(950, 600)

        # Shared Data Managers
        #self.product_mgr = ProductManager()
        #self.sales_mgr = SalesManager()

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_auth_selection()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_auth_selection(self):
        self.clear_container()

        card = ctk.CTkFrame(self.container, corner_radius=15, width=400, height=400)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="☕ BIGBREW SYSTEM", font=ctk.CTkFont(size=24, weight="bold"), text_color="#FFA500").pack(pady=(40, 10))
        ctk.CTkLabel(card, text="Select Portal to Access:").pack(pady=(0, 20))

        ctk.CTkButton(
            card,
            text="🛒 Customer Ordering",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=260,
            fg_color="#FFA500",
            text_color="black",
            command=self.open_customer_module
        ).pack(pady=10)

        ctk.CTkButton(
            card,
            text="🔐 Admin Portal",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=260,
            fg_color="#333",
            command=self.open_admin_module
        ).pack(pady=10)

    def open_customer_module(self):
        self.clear_container()
        customer_frame = CustomerView(self.container, self, self.product_mgr, self.sales_mgr)
        customer_frame.pack(fill="both", expand=True)

    def open_admin_module(self):
        self.clear_container()
        admin_frame = AdminView(self.container, self, self.product_mgr, self.sales_mgr)
        admin_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()