# -*- coding: utf-8 -*-
import os
import subprocess
import socket
from typing import List
from libqtile import qtile, layout, layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.command import lazy
from libqtile.dgroups import simple_key_binder

mod = "mod4"                # Set mod key to Super
term = "alacritty"          # Set default terminal eumlator to alacritty
browser = "qutebrowser"     # Set default browser to qutebrowser
dgroups_key_binder = simple_key_binder("mod4")

# Colors aliases
PANEL   = 0
TAB     = 1
FONT    = 2
WINDOW  = 3
INACT   = 4


# Colors
colors = [
    ["#282c34", "#282c34"], # Panel background
    ["#3d3f4b", "#434758"], # Active tab
    ["#ffffff", "#ffffff"], # Font color
    ["#e1acff", "#e1acff"], # Window name
    ["#ecbbfb", "#ecbbfb"], # Background for inactive screens
]

# Prompt
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

# Groups
class Groupings:

    def __init__(self):
        self.group_names = self.init_group_names()
        self.groups = self.init_groups()

    def init_group_names(self):
        return [("", {"layout": "monadtall"}),     # Terminals
                ("", {"layout": "monadtall"}),     # Web Browser
                ("", {"layout": "monadtall"}),     # File Manager
                ("", {"layout": "monadtall"}),     # Text Editor
                ("", {"layout": "monadtall"}),     # Media
                ("", {"layout": "monadtall"}),     # Music/Audio
                ("漣", {"layout": "monadtall"})]    # Settings

    def init_groups(self):
        return [Group(name, **kwargs) for name, kwargs in self.group_names]

# groups = []


# Layouts
layout_theme = {
    "border_width": 2,
    "margin": 5,
    "border_focus": "FFFFFF",
    "border_normal": "1D2330"
}

layouts = [
    # layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    # layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    # layout.Matrix(**layout_theme),
    layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    # layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme)
]


# Mouse behavior 
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# KeyBindings
keys = [
    # Qtile bindings
    
    Key([mod], "Tab",
        lazy.next_layout(),
        desc="Switches to next layout in the list"
    ),
    Key([mod, "shift"], "c",
        lazy.window.kill(),
        desc="Closes current window"
    ),
    Key([mod, "shift"], "r",
        lazy.restart(),
        desc="Reloads Qtile"
    ),
    Key([mod, "shift"], "q",
        lazy.shutdown(),
        desc="Shuts down Qtile"
    ),

    # Essentials

    Key([mod], "Return",
        lazy.spawn(term + "-e fish"),
        desc="Launches my terminal"
    ),
    Key([mod, "shift"], "Return",
        lazy.spawn("rofi -show run"),
        desc="Starts rofi"
    ),
    Key([mod, "shift"], "v",
        lazy.spawn("bwmenu"),
        desc="Open bitwarden rofi vault"
    ),

    # Media Keys

    Key([], "XF86MonBrightnessUp",
        lazy.spawn("lux -a 10"),
        desc="increase backlight amount"
    ),
    Key([], "XF86MonBrightnessDown",
        lazy.spawn("lux -s 10"),
        desc="increase backlight amount"
    ),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("pamixer --allow-boost -d 5"),
        desc="Decrease volume"
        ),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("pamixer --allow-boost -i 5"),
        desc="Increase volume"
        ),
    Key([], "XF86AudioMute",
        lazy.spawn("pamixer -t"),
        desc="Mute/Unmute volume"
        ),

    # Windows control

    Key([mod], "j",
        lazy.layout.down(),
        desc='Move focus down in current stack pane'
    ),
    Key([mod], "k",
        lazy.layout.up(),
        desc='Move focus up in current stack pane'
    ),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down(),
        desc='Move windows down in current stack'
    ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up(),
        desc='Move windows up in current stack'
    ),
    Key([mod], "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
    ),
    Key([mod], "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
    ),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc='normalize window size ratios'
    ),
    Key([mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'
    ),
    Key([mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'
    ),
    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        desc='toggle fullscreen'
    )
]

# Default widgets settings
widget_defaults = dict(
    font = "FiraCode Nerd Font",
    font_size = 13,
    padding = 2,
    background_color = colors[FONT]
)

nerd_icon_defaults = dict(
    font = "Iosevka Nerd Font",
    fontsize = 15
)

extension_defaults = widget_defaults.copy()

# Widget list for the home bar
def init_widgets_list():
    widget_list = [
    widget.Sep(
        linewidth = 0,
        padding = 4,
        foreground = colors[FONT],
        background = colors[PANEL]
        ),
    widget.Image(
        filename = "/usr/share/pixmaps/archlinux-logo.png",
        background = colors[PANEL],
        margin = 3
        ),
    widget.GroupBox(
        font = "Iosevka Nerd Font",
        fontsize = 15,
        foreground = colors[FONT],
        background = colors[PANEL],
        borderwidth = 8,
        highlight_method = "text",
        inactive = colors[INACT]
        ),
    widget.Prompt(
        prompt = prompt,
        font = "FiraCode Nerd Font",
        foreground = colors[WINDOW],
        background = colors[PANEL]
        ),
    widget.Sep(
        padding = 10, 
        foreground = colors[FONT],
        background = colors[PANEL]
        ),
    widget.WindowName(
        foreground = colors[WINDOW],
        background = colors[PANEL],
        padding = 15,
        fontsize = 12,
        format = "{name}",
        max_chars = 20
        ),
    widget.Spacer(
        length = 25,
        background = colors[PANEL]
        ), 
 
    widget.Spacer(
        length = 8,
        background = colors[PANEL]
        ),
    widget.TextBox(
        text = " | ",
        foreground = colors[INACT],
        background = colors[PANEL]
        ),
    widget.CurrentLayout(
        background = colors[PANEL],
        foreground = colors[WINDOW],
        padding = 10
        ),
    widget.TextBox(
        text = " | ",
        foreground = colors[INACT],
        background = colors[PANEL]
        ),
    widget.TextBox(
        font = "Iosevka Nerd Font",
        fontsize = 15,
        text = "",
        foreground = colors[INACT],
        background = colors[PANEL]
        ),
    widget.Clock(
        format = '%I:%M:%S %p',
        foreground = colors[FONT],
        background = colors[PANEL]
        ),
    widget.TextBox(
        text = " | ",
        foreground = colors[INACT],
        background = colors[PANEL]
        ),
    widget.Spacer(
        length = 8,
        background = colors[PANEL]
        ),
    widget.Spacer(
        length = bar.STRETCH,
        background = colors[PANEL]
        ),

    # Right Part
    widget.TextBox(
        text = " | ",
        foreground = colors[INACT],
        background = colors[PANEL]
        ),
    widget.TextBox(
        font = "Iosevka Nerd Font",
        fontsize = 15,
        # padding = 15,
        text = "",
        foreground = colors[FONT],
        background = colors[PANEL]
        ),
    widget.Spacer(
        length = 8,
        background = colors[PANEL]
        ),
    widget.Net(
        format = "{down} ↓↑ {up}",
        foreground = colors[FONT],
        background = colors[PANEL],
        update_interval = 2,
        # mouse_callbacks = {
            # 'Button1': lambda : qtile.cmd_spawn(f"networkmanager_dmenu {dmenu_conf}")
        # }
        ),
    widget.Spacer(
        length = 8,
        background = colors[PANEL]
        ),
    widget.TextBox(
        font = "Iosevka Nerd Font",
        fontsize = 15,
        text = "",
        foreground = colors[FONT],
        background = colors[PANEL]
        ),
    widget.Battery(
        foreground = colors[FONT],
        background = colors[PANEL],
        format = "{percent:2.0%}",
        update_intervals = 10
        ),
    widget.Spacer(
        length = 8,
        background = colors[PANEL]
        ),
    widget.TextBox(
        font = "Iosevka Nerd Font",
        fontsize = 15,
        text = "墳",
        foreground = colors[FONT],
        background = colors[PANEL]
        ),
    widget.Volume(
        foreground = colors[FONT],
        background = colors[PANEL]
        ),
    widget.Spacer(
        length = 15,
        background = colors[PANEL]
        )
    ]
    return widget_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[7:8]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"] :
    screens = init_screens() 
    widget_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    groupings = Groupings()
    group_names = groupings.group_names
    groups = groupings.groups

    for i, (name, kwargs) in enumerate(groupings.group_names, 1):
        keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
        keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

# Defaults and rules
dgroups_app_rules = [] # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

# Assign apps to workspaces hook 
# @hook.subscribe.client_new
# def assign_app_group(client):
    # d = {}

    # assign deez apps
    # d[group_names[0][0]] = ['Alacritty', 'xfce4-terminal', 'librewolf']
    # d[group_names[1][0]] = ['Navigator', 'discord', 'midori', 'qutebrowser']
    # d[group_names[2][0]] = ['pcmanfm', 'thunar']
    # d[group_names[3][0]] = ['code', 'geany']
    # d[group_names[4][0]] = ['vlc', 'obs', 'mpv', 'mplayer', 'lxmusic', 'gimp']
    # d[group_names[5][0]] = ['spotify']
    # d[group_names[6][0]] = ['lxappearance', 'gpartedbin', 'lxtask', 'lxrandr', 'arandr', 'pavucontrol', 'xfce4-settings-manager']

    # wm_class = client.window.get_wm_class()[0]
    # for i in range(len(d)):
        # if wm_class in list(d.values())[i]:
            # group = list(d.keys())[i]
            # client.togroup(group)
            # client.group.cmd_toscreen(toggle=False)

# Startup hook
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
