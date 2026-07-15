# PIO Cortex-Debug

I was a bit frustrated with the built-in debug UI of PlatformIO. It spits out error messages when it should read peripheral register values, and afterward will not update the values anymore. And the disassembly is nice to have, but you cannot really debug on this level. Having worked with a recent version of Cortex-Debug, where all of this works flawlessly, led to the idea of why not try to use Cortex-Debug instead of the PIO debugger UI.

The Python script `cortex-debug.py` is a little hack to make Cortex-Debug available inside PlatformIO/VSC for the case that you use PyAvrOCD as the GDB server. 

After copying it to your project folder and declaring it as an extra script in your `platform.ini` file, you get a **custom** **target** called 'refresh_json'. When you select it, your `launch.json` file is updated with a new configuration called Cortex-Debug, provided the selected debug tool is 'pyavrocd'. After selecting this new configuration, Cortex-Debug will be started when 'Run and Debug' is requested. 

You need to refresh `launch.json` before you restart the debugger each time you have changed your default environment or changed the `platform.ini` file. 

The script should be adaptable to all cases where one uses a GDB server that is compatible with Cortex-Debug, I believe. The assignment of the debug port and the handling of the debug_init_cmds is a bit tricky, however.  