# Simple Wireplumber GUI

<a href='https://flathub.org/apps/io.github.dyegoaurelio.simple-wireplumber-gui'><img width='240' alt='Download on Flathub' src='https://dl.flathub.org/assets/badges/flathub-badge-en.png'/></a>

With this tool you can easily rename and see the properties of your audio devices if you're running `pipewire` as your audio server and `wireplumber` as it's session and policy manager.

![main window screenshot](/data/screenshots/main-window.png "main window screenshot")

## Installation
### Flathub
See package information [here](https://flathub.org/apps/io.github.dyegoaurelio.simple-wireplumber-gui).

With flatpak installed, run this command.
```BASH
flatpak install flathub io.github.dyegoaurelio.simple-wireplumber-gui
```
### Arch User Repository
This method only works on Arch Linux.
See package information [here](https://aur.archlinux.org/packages/simple-wireplumber-gui).

#### With yay
```BASH
yay -S simple-wireplumber-gui
```

#### Without an AUR helper
Clone the repository
```BASH
git clone https://aur.archlinux.org/simple-wireplumber-gui.git
```
Change directory into the repository
```BASH
cd simple-wireplumber-gui
```
Make the package
```BASH
makepkg -si
```

## Clearing changes

When you uninstall this app, its changes will remain on your system.

If you wish to erase all its changes, you can just run on your terminal:

```BASH
flatpak run io.github.dyegoaurelio.simple-wireplumber-gui --clear-settings
```

And then, reboot your system.
