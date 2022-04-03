import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401from typing import List  # noqa: F401

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "brave" # My browser of choice
myMusic = 'spotify' # My music Player
myFileManager = 'thunar'
myDefaultLauncher = 'rofi -show run'

wallpaper_change = 'feh --bg-fill -r -z ~/Pictures/wallpapers/'


keys = [
         ### Apps Essentials
         Key([mod], "q",
             lazy.window.kill(),
             desc='Current Window Kill'
             ),
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn(myDefaultLauncher),
             desc='Launches my Default Launcher'
             ),
         Key([mod], "b",
             lazy.spawn(myBrowser),
             desc='Launches my Browser'
             ),
         Key([mod], "s",
             lazy.spawn(myMusic),
             desc='Launches my Music'
             ),
         Key([mod], "Tab",
             lazy.screen.next_group(),
             desc='Toggle through groups'
             ), 
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         ### Switch focus to specific monitor (out of three)
         Key([mod], "w",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "e",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Treetab controls
          Key([mod, "shift"], "h",
             lazy.layout.move_left(),
             desc='Move up a section in treetab'
             ),
         Key([mod, "shift"], "l",
             lazy.layout.move_right(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "k",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "j",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "j",
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
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies'
             ),
          Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
          Key([mod, "shift"], "s", lazy.spawn("scrot 'ArcoLinux-%Y-%m-%d-%s_screenshot_$wx$h.jpg' -e 'mv $f $$(xdg-user-dir PICTURES)'"))
]

groups = [Group("WWW", layout='monadtall'),
          Group("DEV", layout='monadtall'),
          Group("SYS", layout='monadtall'),
          Group("VBOX", layout='monadtall'),
          Group("MUS", layout='monadtall'),
          Group("VID", layout='monadtall')]


# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")


colors = [["#282c34", "#282c34"], # 00 GUNMETAL BG BAR
          ["#1c1f24", "#1c1f24"], # 01 EERIE BLACK
          ["#dfdfdf", "#dfdfdf"], # 02 POLISH Grey
          ["#8f00ff", "#8f00ff"], # 03 VIOLET
          ["#adff02", "#adff02"], # 04 GREEN 
          ["#c678dd", "#c678dd"]] # 05 LAVENDER

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": colors[5],
                "border_normal": colors[0]
                }

layouts = [layout.MonadTall(**layout_theme)]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
        
widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 10,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 8,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Image(
                       filename = "~/Pictures/code-48.png",
                       scale = "False",
                       background = colors[0],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)}
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 8,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 9,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[4],
                       inactive = colors[2],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[3],
                       this_screen_border = colors [4],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 8,
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14
                       ),
             widget.Systray(
                       icon_size = 16,
                       background = colors[0],
                       padding = 10
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 10,
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 10,
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.WindowName(
                       foreground = colors[4],
                       background = colors[0],
                       padding = 0
                       ),
             widget.Mpris2(
                    name='spotify',
                    objname="org.mpris.MediaPlayer2.spotify",
                    display_metadata=['xesam:title', 'xesam:artist'],
                    scroll_chars=60,
                    scroll_wait_intervals=89,
                    foreground = colors[4],
                    background = colors[0],
                    stop_pause_text='Player Paused'
                ),
              widget.Sep(
                       linewidth = 0,
                       padding = 8,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.TextBox(
                       text='',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = colors[0],
                       padding = 0,
                       fontsize = 48
                       ),
              widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "Updates: {updates} ",
                       foreground = colors[1],
                       colour_have_updates = colors[4],
                       colour_no_updates = colors[2],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       padding = 5,
                       background = colors[0]
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = colors[3],
                       padding = 0,
                       fontsize = 48
                       ),
              widget.Memory(
                       foreground = colors[2],
                       background = colors[3],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       fmt = 'Mem: {}',
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[3],
                       foreground = colors[1],
                       padding = 0,
                       fontsize = 48
                       ),
              widget.Volume(
                       foreground = colors[2],
                       background = colors[1],
                       fmt = 'Vol: {}',
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[1],
                       foreground = colors[0],
                       padding = 0,
                       fontsize = 44
                       ),
              widget.Clock(
                       foreground = colors[2],
                       background = colors[0],
                       format = "%A %d, %B - %H:%M ",
                       padding = 5
                       ),
              widget.Notify(
                       background = colors[4],
                       foreground = colors[2],
                       padding = 5
              )
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[0:22]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0, size=6)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=25))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def switch_groups():
    i = qtile.groups.index(qtile.currentGroup)
    if i != 4:
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)
    else:
        qtile.currentWindow.togroup(qtile.groups[0].name)

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

mouse = [
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# Hi There!
# This is parta of a journey creating a work enviroment working for me instead of
# working as other wanted. 
# You can follow my journey on https://github.com/efeuncode/.dotfiles

wmname = "EFE"
