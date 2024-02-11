<img src="https://github.com/SenshiSentou/sd-webui-qic-console/blob/main/preview.png" />

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/J3J81VHA2)

# !!! WARNING !!!

This extension was made for developers! If someone ever asks you to install this extension and run any code they send you, **DON'T**. There are no safety checks in place, and malicious code can be ran without restriction.

# QIC Console

The Quick Iterative Code Console (QIC Console) was created to allow devs to quickly test snippets of Python code within the A1111 environment without having to constantly restart the app. For example, you might want to quickly check or manipulate some `shared` state, or run a quick `dir()` to see what attributes are available on an object at run-time.

Unfortunately there is no auto-complete, only syntax highlighting.

# Python

Any Python code entered is executed using `exec` in the extension's context.

# Javascript

Any Javascript code entered is executed using `eval` and gives full access to all the same functions and variables that you do in the developer console. The only reason I added JS is that sometimes it's just nice to have a little more room to type while testing things.

# Installation

Open your A1111 Web UI and go to `Extensions > Install from URL`. Paste in the link to this repo (`https://github.com/SenshiSentou/sd-webui-qic-console.git`), click `Install` and restart the web ui.