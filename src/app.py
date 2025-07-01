import gi

gi.require_version("Gtk", "4.0")
gi.require_version("GLib", "2.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gio, Adw
from .window import SimpleWireplumberGuiWindow


class SimpleWireplumberGuiApplication(Adw.Application):
    """The main application singleton class."""

    main_window: SimpleWireplumberGuiWindow | None = None

    def __init__(self):
        super().__init__(
            application_id="io.github.dyegoaurelio.simple-wireplumber-gui",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action, ["F1"])
        self.create_action(
            "preferences", self.on_preferences_action, ["<primary>comma"]
        )
        self.create_action("refresh_app", self.on_refresh_app, ["F5", "<primary>r"])

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        if self.main_window is None:
            self.main_window = SimpleWireplumberGuiWindow(application=self)

        win = self.props.active_window
        if not win:
            win = self.main_window
        win.present()

    def on_refresh_app(self, widget, _):
        for window in Gtk.Window.list_toplevels():
            window.destroy()

        self.main_window = SimpleWireplumberGuiWindow(application=self)
        self.main_window.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="Simple Wireplumber GUI",
            application_icon="io.github.dyegoaurelio.simple-wireplumber-gui",
            developer_name="Dyego Aurélio",
            version="0.2.2",
            developers=["dyegoaurelio https://github.com/dyegoaurelio"],
            issue_url="https://github.com/dyegoaurelio/simple-wireplumber-gui/issues",
            copyright="© 2023 dyego",
            application=self,
        )
        # Translator credits. Replace "translator-credits" with your name/username, and optionally an email or URL.
        # One name per line, please do not remove previous names.
        about.set_translator_credits(_("translator-credits"))
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print("app.preferences action activated")

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        self.create_action
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
