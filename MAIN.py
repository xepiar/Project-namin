import customtkinter as ctk
from PIL import Image, ImageDraw
from CUSTOMER import CustomerPortal
from ADMIN import AdminPortal

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

def create_placeholder_pil_image(color_hex="#FFA500", size=(80, 80)):
    img = Image.new("RGBA", size, color=color_hex)
    draw = ImageDraw.Draw(img)
    draw.rectangle([2, 2, size[0] - 3, size[1] - 3], outline="white", width=2)
    return img

class BigBrewApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BigBrew POS & Order System")
        self.geometry("1100x720")
        self.minsize(950, 600)

        self._init_image_assets()

        self.user_role = None  # "Customer" or "Admin"
        self.customer_name = "Guest"

        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)

        self.show_auth_selection()

    def _init_image_assets(self):
        pil_logo = create_placeholder_pil_image("#FF8C00", size=(50, 50))
        self.logo_ctk_image = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(40, 40))

        self.category_pil_images = {
            "Milk Tea": create_placeholder_pil_image("#D2B48C", size=(60, 60)),
            "Iced Coffee": create_placeholder_pil_image("#6F4E37", size=(60, 60)),
            "Fruit Tea": create_placeholder_pil_image("#FF6B6B", size=(60, 60)),
        }

        self.ctk_item_images = {}
        for cat, pil_img in self.category_pil_images.items():
            self.ctk_item_images[cat] = ctk.CTkImage(
                light_image=pil_img, dark_image=pil_img, size=(45, 45)
            )

    def _clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_auth_selection(self):
        self._clear_container()

        card = ctk.CTkFrame(self.main_container, corner_radius=15, width=400, height=450)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, image=self.logo_ctk_image, text="").pack(pady=(30, 10))
        ctk.CTkLabel(card, text="WELCOME TO BIGBREW", font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="#FFA500").pack(pady=5)
        ctk.CTkLabel(card, text="Please select your portal to continue", font=ctk.CTkFont(size=12)).pack(pady=(0, 25))

        ctk.CTkButton(
            card,
            text="🛒 Customer Ordering",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=45,
            width=260,
            fg_color="#FFA500",
            hover_color="#CC8400",
            text_color="black",
            command=self.show_customer_login
        ).pack(pady=10)

        ctk.CTkButton(
            card,
            text="🔐 Admin Management",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=45,
            width=260,
            fg_color="#333333",
            hover_color="#444444",
            command=self.show_admin_login
        ).pack(pady=10)

    def show_customer_login(self):
        self._clear_container()

        card = ctk.CTkFrame(self.main_container, corner_radius=15, width=400, height=450)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Customer Portal", font=ctk.CTkFont(size=22, weight="bold"), text_color="#FFA500").pack(pady=(30, 10))
        ctk.CTkLabel(card, text="Enter your name to personalize your order receipt:").pack(pady=5)

        name_entry = ctk.CTkEntry(card, width=280)
        name_entry.pack(pady=15)

        def proceed_as_customer():
            val = name_entry.get().strip()
            self.customer_name = val if val else "Guest Customer"
            self.user_role = "Customer"
            self.build_pos_interface()

        ctk.CTkButton(
            card,
            text="Start Ordering",
            fg_color="#FFA500",
            hover_color="#CC8400",
            text_color="black",
            font=ctk.CTkFont(weight="bold"),
            width=280,
            height=40,
            command=proceed_as_customer
        ).pack(pady=10)

        ctk.CTkButton(card, text="← Back", fg_color="transparent", width=100, command=self.show_auth_selection).pack(pady=10)

    def show_admin_login(self):
        self._clear_container()

        card = ctk.CTkFrame(self.main_container, corner_radius=15, width=400, height=450)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Admin Login", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 10))

        pass_entry = ctk.CTkEntry(card, width=280, show="*")
        pass_entry.pack(pady=15)

        err_label = ctk.CTkLabel(card, text="", text_color="#E74C3C")
        err_label.pack(pady=2)

        def verify_admin():
            if pass_entry.get() == "BIGBREW":
                self.user_role = "Admin"
                self.build_admin_dashboard()
            else:
                err_label.configure(text="Invalid Password!")

        ctk.CTkButton(
            card,
            text="Login as Admin",
            fg_color="#2ECC71",
            hover_color="#27AE60",
            font=ctk.CTkFont(weight="bold"),
            width=280,
            height=40,
            command=verify_admin
        ).pack(pady=10)

        ctk.CTkButton(card, text="← Back", fg_color="transparent", width=100, command=self.show_auth_selection).pack(pady=5)

    def build_admin_dashboard(self):
        self._clear_container()
        admin_portal = AdminPortal(self.main_container, self)
        admin_portal.pack(fill="both", expand=True)

    def build_pos_interface(self):
        self._clear_container()
        customer_portal = CustomerPortal(self.main_container, self)
        if hasattr(customer_portal, 'update_cart_title'):
            customer_portal.update_cart_title()
        if hasattr(customer_portal, 'RefreshMenu'):
            customer_portal.RefreshMenu()
        customer_portal.pack(fill="both", expand=True)

    def show_customer_portal(self):
        #ETO YUNG CUSTOMER PORTAL
        self.build_pos_interface()

    def show_admin_portal(self):
        # ETO YUNG ADMIN PORTAL
        self.build_admin_dashboard()

if __name__ == "__main__":
    app = BigBrewApp()
    app.mainloop()