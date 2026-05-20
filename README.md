# Simple Wireplumber GUI

<a href='https://flathub.org/apps/io.github.dyegoaurelio.simple-wireplumber-gui'><img width='240' alt='Download on Flathub' src='https://dl.flathub.org/assets/badges/flathub-badge-en.png'/></a>

With this tool you can easily rename and see the properties of your audio devices if you're running `pipewire` as your audio server and `wireplumber` as it's session and policy manager.

![main window screenshot](/data/screenshots/main-window.png "main window screenshot")

## Installation
### Flathub
This is the preferred method of installation. See package information [here](https://flathub.org/apps/io.github.dyegoaurelio.simple-wireplumber-gui).

With flatpak installed, run this command:
```BASH
flatpak install flathub io.github.dyegoaurelio.simple-wireplumber-gui
```
### Arch User Repository
This method only works on Arch-based Linux distributions and is community-maintained.
See package information [here](https://aur.archlinux.org/packages/simple-wireplumber-gui).

#### With yay
```BASH
yay -S simple-wireplumber-gui
```

#### Without an AUR helper
Clone the repository:
```BASH
git clone https://aur.archlinux.org/simple-wireplumber-gui.git
```
Change directory into the repository:
```BASH
cd simple-wireplumber-gui
```
Make the package:
```BASH
makepkg -si
```

### Compiling from Source
You may want to compile Simple Wireplumber GUI from source.

Clone the repository and change directory into it:
```BASH
git clone https://www.github.com/dyegoaurelio/simple-wireplumber-gui.git
cd simple-wireplumber-gui
```
Create and set up the build directory:
```BASH
mkdir ../builddir
meson setup ../builddir
```
Compile:
```BASH
meson compile -C ../builddir
```
Finally, as root, install:
```BASH
meson install -C ../builddir
```
If running `simple-wireplumber-gui` gives a "permission denied" error, as root, try:
```BASH
chmod +x /usr/local/bin/simple-wireplumber-gui
```

## Clearing changes

When you uninstall this app, its changes will remain on your system.

If you wish to erase all its changes, you can just run this on your terminal if you installed with flathub:

```BASH
flatpak run io.github.dyegoaurelio.simple-wireplumber-gui --clear-settings
```

And then, reboot your system.
