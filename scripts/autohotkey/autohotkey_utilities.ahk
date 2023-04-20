/*
    A collection of autohotkey snippets that I wrote or found on the internet. Credits are given when available.
*/

/* Toggles the system volume when the mouse wheel is scrolled over the taskbar */
#If MouseIsOver("ahk_class Shell_TrayWnd")
WheelUp::Send {Volume_Up}
WheelDown::Send {Volume_Down}

MouseIsOver(WinTitle) {
    MouseGetPos,,, Win
    return WinExist(WinTitle . " ahk_id " . Win)
}