import json
import os
import re
Import("env")

def deb_tool():
    expl = env.GetProjectOption("debug_tool", default=None)
    if expl:
        return expl
    debug = env.BoardConfig().get('debug',{})
    tools = debug.get('tools',None)
    if not tools:
        return None
    elif len(tools) == 1:
        return list(tools.keys())[0]
    else:
        for x in tools:
            if tools[x].get("default", False):
                return x
        return list(tools.keys())[0]
    

def gen_entry(environment, executable, init_cmds, toolconfig, tc_dir, svdpath, serverpath,
                  serverargs, regex):
    return {
            "name": "Cortex-Debug (" + environment + ")",
            "type": "cortex-debug",
            "servertype": "openocd",
            "cwd": "${workspaceRoot}",
            "request": "launch",
            "executable": executable,
            "configFiles": [
                "nix"
            ],
            "preLaunchCommands": init_cmds,
            "gdbPath": os.path.join(tc_dir, env.get("GDB")),
            "objdumpPath": os.path.join(tc_dir, env.get("GDB").replace("-gdb","-objdump")),
            "serverpath": serverpath,
            "overrideGDBServerStartedRegex": regex,
            "svdFile": svdpath,
            "runToEntryPoint": "main",
            "serverArgs": serverargs,
            "projectEnvName": environment,
            "preLaunchTask": {
                "type": "PlatformIO",
                "task": "Pre-Debug (" + environment + ")"
            }
        }

def refresh_json(*args, **kwargs):
    jsonfile = os.path.join(env.get('PROJECT_DIR', ''), ".vscode", "launch.json")
    if os.path.exists(jsonfile):
        origjson = {}
        with open(jsonfile, "r", encoding="utf-8") as f:
            origjson = json.loads(re.sub("//.*","",f.read(),flags=re.MULTILINE))
        environment = env.get("PIOENV","")
        package_dir = env.get("PROJECT_PACKAGES_DIR", "")
        executable = origjson['configurations'][-1].get('executable', '')
        toolchainbin_dir = origjson['configurations'][-1].get('toolchainBinDir', '')
        svdpath =  origjson['configurations'][-1].get('svdPath', '')
        tool = deb_tool()
        toolconfig = env.BoardConfig().get('debug',{}).get('tools').get(tool, "")
        server_path = os.path.join(package_dir, toolconfig.get('server', {}).get('package', ""),
                                       toolconfig.get('server', {}).get('executable', ""))
        server_args =  toolconfig.get('server', {}).get('arguments', [])
        regex = toolconfig.get('server', {}).get('regex', "")
        init_cmds = [ "monitor debugwire enable" ]
        new_entry = gen_entry(environment, executable, init_cmds, toolconfig, toolchainbin_dir, svdpath,
                                  server_path, server_args, regex)
        if tool != 'pyavrocd': # sorry, works only with pyavrocd 
            if origjson['configurations'][0]['type'] == 'cortex-debug':
                del origjson['configurations'][0]
                new_entry = True
            print("No debug tool or incompatible tool specified")
        elif origjson['configurations'][0]['type'] != 'cortex-debug':
            origjson['configurations'].insert(0, new_entry)
        elif origjson['configurations'][0] != new_entry:
            origjson['configurations'][0] = new_entry
        else:
            new_entry = None
        if new_entry:
            with open(jsonfile, "w", encoding="utf-8") as f:
                print("""// AUTOMATICALLY GENERATED FILE. PLEASE DO NOT MODIFY IT MANUALLY
//
// PlatformIO Debugging Solution
//
// Documentation: https://docs.platformio.org/en/latest/plus/debugging.html
// Configuration: https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/index.html
//
// Updated by Cortex-Debug generation. Choose your launch.json entry wisely""", file=f)
                print(json.dumps(origjson, indent=4), file=f)

env.AddCustomTarget(
    name="refresh_json",
    dependencies=None,
    actions=[
        refresh_json
    ],
    title="Refresh launch.json",
    description="Generate Cortex-Debug launch.json entry"
)

