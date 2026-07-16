# PIO Cortex-Debug

I was a bit frustrated with the built-in debug UI of PlatformIO. It spits out error messages when it should read peripheral register values, and afterward will not update the values anymore. And the disassembly is nice to have, but you cannot really debug on this level. Having worked with a recent version of Cortex-Debug,[^*] where all of this works flawlessly, led to the idea of why not try to use Cortex-Debug instead of the PIO debugger UI.

The Python script `cortex-debug.py` is a little hack to make Cortex-Debug available inside PlatformIO/VSC for the case that you use PyAvrOCD as the GDB server. 

After copying it to your project folder and declaring it as an extra script in your `platform.ini` file, you get a **custom** **target** called `refresh_json`. When you select it, your `launch.json` file is updated with a new configuration called Cortex-Debug, provided the selected `debug_tool` is `pyavrocd`. After selecting this new configuration, Cortex-Debug will be started when `Run and Debug` (`F5`) is requested. 

You need to refresh `launch.json` before you restart the debugger each time you have changed your default environment or changed the `platform.ini` file. 

The script should be adaptable to other cases where one uses a GDB server that is compatible with Cortex-Debug, I believe. The assignment of the debug port, the handling of the debug_init_cmds and the setting of the server-ready regex is a bit tricky, however.  I chose the `openOCD` style of invoking Cortex-Debug. This means that Cortex-debug chooses the GDB port dynamically, uses it when invoking the server and uses it in the `target extends-remote` command. This means that this port should not be set (or ignored) and that the `init_cmds` needs to be different.

Take the script as an inspiration if you want to use it for other MCU families and debug tools.

[^*]: Although the extension is named Cortex-Debug, it is architecture-agnostic an plays well with other MCUs, such as the AVR family. 