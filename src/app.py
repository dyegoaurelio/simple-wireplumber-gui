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
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action)
        self.create_action("refresh_app", self.on_refresh_app)

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
        if self.main_window is None:
            return

        self.main_window.destroy()
        self.main_window = SimpleWireplumberGuiWindow(application=self)
        self.main_window.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="simple-wireplumber-gui",
            application_icon="io.github.dyegoaurelio.simple-wireplumber-gui",
            developer_name="dyego",
            version="0.1.0",
            developers=["dyego"],
            copyright="© 2023 dyego",
        )
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