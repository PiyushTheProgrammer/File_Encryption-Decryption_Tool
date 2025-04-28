from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

from kivy.utils import get_color_from_hex
import os
from crypto_utils import CryptoUtils

Window.size = (480, 700)

class SplashScreen(MDScreen):
    pass

class MainScreen(MDScreen):
    pass

class AboutUsScreen(MDScreen):
    pass

class HelpScreen(MDScreen):
    pass

class ContentNavigationDrawer(MDBoxLayout):
    pass

class DataCryptApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = "assets/icon.png"
        self.file_manager = None
        self.screen_manager = MDScreenManager()
        self.save_dialog = None
        self.for_decryption = False  # Default mode is for encryption

    def build(self):
        # Set up cybersecurity/hacking theme colors
        # Dark theme - default
        self.theme_cls.primary_palette = "Teal"  # Teal for primary elements
        self.theme_cls.accent_palette = "Green"  # Green for accents
        self.theme_cls.primary_hue = "700"
        self.theme_cls.accent_hue = "A400"
        self.theme_cls.theme_style = "Dark"  # Default to dark mode
        self.theme_cls.material_style = "M3"

        # Define custom colors for cybersecurity theme
        self.cyber_colors = {
            # Dark theme colors - hacker-inspired dark theme
            "dark": {
                "background": "#0A0E17",  # Very dark blue-black background
                "card": "#1A2130",  # Dark navy for cards
                "card_alt": "#162029",  # Alternative dark card color
                "primary": "#00E676",  # Matrix green for primary elements
                "secondary": "#00BCD4",  # Cyan for secondary elements
                "accent1": "#FF5252",  # Red accent
                "accent2": "#FFAB00",  # Amber accent
                "accent3": "#7C4DFF",  # Purple accent
                "text_primary": "#E0E0E0",  # Light gray text
                "text_secondary": "#9E9E9E",  # Medium gray for secondary text
                "text_accent": "#64FFDA",  # Bright teal for accent text
                "success": "#00E676",  # Green for success messages
                "warning": "#FFAB00",  # Amber for warnings
                "error": "#FF1744",  # Red for errors
                "surface": "#162029",  # Surface color for dialogs
                "button_primary": "#00E676",  # Primary button color
                "button_secondary": "#00BCD4",  # Secondary button color
                "button_danger": "#FF5252"  # Danger button color
            },
            # Light theme colors - cybersecurity professional light theme
            "light": {
                "background": "#E0E0E0",  # Light gray for background
                "card": "#F5F5F5",  # Very light gray for cards
                "card_alt": "#EEEEEE",  # Alternative light card color
                "primary": "#455A64",  # Blue-gray for primary elements
                "secondary": "#546E7A",  # Lighter blue-gray for secondary elements
                "accent1": "#D32F2F",  # Darker red accent
                "accent2": "#FFA000",  # Gold accent matching logo
                "accent3": "#5D4037",  # Brown accent for a more serious tone
                "text_primary": "#212121",  # Very dark gray text
                "text_secondary": "#424242",  # Dark gray for secondary text
                "text_accent": "#455A64",  # Blue-gray for accent text
                "success": "#2E7D32",  # Darker green for success messages
                "warning": "#F57F17",  # Darker amber for warnings
                "error": "#C62828",  # Darker red for errors
                "surface": "#F5F5F5",  # Light gray surface for dialogs
                "button_primary": "#455A64",  # Blue-gray button color
                "button_secondary": "#607D8B",  # Lighter blue-gray button color
                "button_danger": "#D32F2F"  # Darker red button color
            }
        }

        # Load KV files
        Builder.load_file("splash_screen.kv")
        Builder.load_file("nav_drawer.kv")
        Builder.load_file("about_us.kv")
        Builder.load_file("help.kv")
        self.screen = Builder.load_file("datacrypt.kv")

        # Create screens
        splash_screen = SplashScreen(name="splash")
        main_screen = MainScreen(name="main")
        about_us_screen = AboutUsScreen(name="about_us")
        help_screen = HelpScreen(name="help")

        # Add main content to main screen
        main_screen.add_widget(self.screen)

        # Add screens to screen manager
        self.screen_manager.add_widget(splash_screen)
        self.screen_manager.add_widget(main_screen)
        self.screen_manager.add_widget(about_us_screen)
        self.screen_manager.add_widget(help_screen)

        # Show splash screen for 3 seconds
        Clock.schedule_once(self.switch_to_main_screen, 3)
        return self.screen_manager

    def switch_to_main_screen(self, dt):
        self.screen_manager.current = "main"

    def toggle_theme(self):
        """Toggle between cybersecurity/hacking-themed light and dark themes"""
        # Toggle theme style
        new_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        self.theme_cls.theme_style = new_style

        # Adjust primary and accent colors based on theme
        if new_style == "Dark":
            # Hacker-inspired dark theme colors
            self.theme_cls.primary_palette = "Teal"
            self.theme_cls.accent_palette = "Green"
            self.theme_cls.primary_hue = "700"
            self.theme_cls.accent_hue = "A400"
        else:
            # Cybersecurity professional light theme
            self.theme_cls.primary_palette = "BlueGray"
            self.theme_cls.accent_palette = "Amber"
            self.theme_cls.primary_hue = "700"
            self.theme_cls.accent_hue = "700"

        # Show a snackbar to confirm theme change
        theme_name = "Hacker Dark" if new_style == "Dark" else "Cybersecurity Light"
        self.show_snackbar(f"Switched to {theme_name} theme")

    def generate_key(self):
        """Generate a new encryption key"""
        self.generated_key = CryptoUtils.generate_key()
        self.show_generated_key_dialog(self.generated_key)

    def show_generated_key_dialog(self, key_text):
        # Create a single clean content box with title inside
        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            padding="16dp",
            size_hint_y=None,
            height="120dp"  # Reduced height
        )

        # Title inside the content
        title = MDLabel(
            text="Generated Key",
            theme_text_color="Primary",
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height="30dp"
        )

        # Key text field with better styling
        key_label = MDTextField(
            text=key_text,
            readonly=True,
            font_size="16sp",
            mode="fill",
            size_hint_y=None,
            height="56dp",
            helper_text="⚠️ This key cannot be recovered if lost!",
            helper_text_mode="persistent",
            helper_text_color_normal=get_color_from_hex("#f44336"),  # Red color for warning
            line_color_normal=self.theme_cls.primary_color,
            line_color_focus=self.theme_cls.primary_color,
            text_color_normal=self.theme_cls.primary_dark,
            text_color_focus=self.theme_cls.primary_dark,
        )

        # Add widgets to content
        content.add_widget(title)
        content.add_widget(key_label)

        # Create a simple dialog with no title
        self.key_dialog = MDDialog(
            title="",  # No title in the dialog itself
            type="custom",
            content_cls=content,
            buttons=[
                MDFillRoundFlatIconButton(
                    text="Save Key",
                    icon="content-save",
                    on_release=self.open_file_manager_for_save,
                    md_bg_color=self.theme_cls.primary_color
                ),
                MDFillRoundFlatIconButton(
                    text="Close",
                    icon="close-circle",
                    on_release=lambda x: self.key_dialog.dismiss(),
                    md_bg_color=get_color_from_hex("#ff9800")
                ),
            ],
            radius=[20, 20, 20, 20],
        )
        self.key_dialog.open()

    def open_file_manager_for_save(self, *args):
        self.key_dialog.dismiss()
        self.for_decryption = False  # We're saving a key file, not decrypting

        # Always recreate the file manager
        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.save_key_to_selected_path,
            preview=False  # Disable thumbnails for a simpler view
        )

        # Get the project directory
        project_dir = CryptoUtils.get_project_dir()

        # Show the file manager starting at the project directory
        self.file_manager.show(project_dir)

    def save_key_to_selected_path(self, path):
        self.close_file_manager()
        self.ask_filename_to_save(path)

    def ask_filename_to_save(self, base_path):
        content = MDBoxLayout(orientation="vertical", spacing="10dp", padding="10dp")
        self.filename_field = MDTextField(
            hint_text="Enter file name",
            text="encryption_key",
            mode="fill",
            size_hint_y=None,
            height="60dp"
        )
        content.add_widget(self.filename_field)

        self.save_dialog = MDDialog(
            title="Save Key As",
            type="custom",
            content_cls=content,
            buttons=[
                MDFillRoundFlatIconButton(
                    text="Save",
                    icon="content-save",
                    on_release=lambda x: self.save_key_file(base_path)
                ),
                MDFillRoundFlatIconButton(
                    text="Cancel",
                    icon="close-circle",
                    on_release=lambda x: self.save_dialog.dismiss()
                )
            ],
            radius=[20, 20, 20, 20],
        )
        self.save_dialog.open()

    def save_key_file(self, base_path):
        filename = self.filename_field.text.strip()
        if filename == "":
            self.show_dialog("Filename cannot be empty!")
            return
        if not filename.endswith(".key"):
            filename += ".key"
        full_path = os.path.join(base_path, filename)
        try:
            with open(full_path, "w") as f:
                f.write(self.generated_key)
            self.show_dialog("Key saved successfully!\n" + full_path)
            self.save_dialog.dismiss()
        except Exception as e:
            self.show_dialog(f"Error saving key: {str(e)}")

    def encrypt_file(self):
        """Encrypt the selected file"""
        key = self.screen.ids.key_input.text.strip()
        filepath = self.screen.ids.file_input.text.strip()

        if not key or not filepath:
            self.show_snackbar("Please enter a key and select a file")
            return

        if not os.path.isfile(filepath):
            self.show_snackbar("Selected file does not exist")
            return

        self.show_loading_dialog("Encrypting File")
        Clock.schedule_once(lambda _: self._perform_encryption(key, filepath), 0.5)

    def _perform_encryption(self, key, filepath):
        """Perform the actual encryption"""
        success, message = CryptoUtils.encrypt_file(filepath, key)
        self.dismiss_loading_dialog()

        if success:
            # Get the directory of the original file
            file_dir = os.path.dirname(filepath)

            # Get the original filename
            original_filename = os.path.basename(filepath)

            # Create encrypted file path with 'encrypted_' prefix in the same directory
            encrypted_path = os.path.join(file_dir, "encrypted_" + original_filename)

            self.show_success_dialog("Encryption Successful",
                                   f"File encrypted and saved as:\n{encrypted_path}")
        else:
            self.show_error_dialog("Encryption Failed", message)

    def decrypt_file(self):
        """Decrypt the selected file"""
        key = self.screen.ids.key_input.text.strip()
        filepath = self.screen.ids.file_input.text.strip()

        if not key:
            self.show_snackbar("Please enter a key")
            return

        if not filepath:
            # Open file manager
            self.open_file_manager()
            return

        if not os.path.isfile(filepath):
            self.show_snackbar("Selected file does not exist")
            return

        self.show_loading_dialog("Decrypting File")
        Clock.schedule_once(lambda _: self._perform_decryption(key, filepath), 0.5)

    def _perform_decryption(self, key, filepath):
        """Perform the actual decryption"""
        success, message = CryptoUtils.decrypt_file(filepath, key)
        self.dismiss_loading_dialog()

        if success:
            # Get the directory of the encrypted file
            file_dir = os.path.dirname(filepath)

            # Get the original filename (remove 'encrypted_' prefix if present)
            original_filename = os.path.basename(filepath)
            if original_filename.startswith("encrypted_"):
                decrypted_filename = original_filename[len("encrypted_"):]
            else:
                decrypted_filename = "decrypted_" + original_filename

            # Create decrypted file path in the same directory
            decrypted_path = os.path.join(file_dir, decrypted_filename)

            self.show_success_dialog("Decryption Successful",
                                   f"File decrypted and saved as:\n{decrypted_path}")
        else:
            self.show_error_dialog("Decryption Failed", message)

    def open_file_manager(self, for_decryption=False):
        """
        Open file manager
        Args:
            for_decryption: Parameter kept for backward compatibility
        """
        # Store the mode for our select_path method
        self.for_decryption = for_decryption

        # Create a new file manager instance with preview disabled for a simpler view
        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.select_path,
            preview=False  # Disable thumbnails for a simpler view
        )

        # Get the project directory
        project_dir = CryptoUtils.get_project_dir()

        # Show the file manager starting at the project directory
        self.file_manager.show(project_dir)

    def select_path(self, path):
        self.screen.ids.file_input.text = path
        self.close_file_manager()

    def close_file_manager(self, *args):
        if self.file_manager:
            self.file_manager.close()
            self.file_manager = None  # Set to None so it will be recreated with proper filters next time

    def show_loading_dialog(self, task_type="Processing"):
        self.loading_dialog = MDDialog(
            title=f"{task_type}...",
            type="custom",
            content_cls=MDSpinner(size_hint=(None, None), size=(46, 46), active=True),
        )
        self.loading_dialog.open()

    def dismiss_loading_dialog(self, *args):
        if hasattr(self, 'loading_dialog') and self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None

    def show_dialog(self, message):
        dialog = MDDialog(
            title="DataCrypt",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def show_success_dialog(self, title, message):
        """Show a success dialog"""
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFillRoundFlatIconButton(
                    text="OK",
                    icon="check",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def show_error_dialog(self, title, message):
        """Show an error dialog"""
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFillRoundFlatIconButton(
                    text="OK",
                    icon="close",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def show_snackbar(self, message):
        """Show a snackbar message"""
        snackbar = Snackbar(
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=0.95
        )
        snackbar.text = message  # Set text after initialization
        snackbar.open()

if __name__ == "__main__":
    DataCryptApp().run()
