from nuitka.plugins.PluginBase import (  # pyright: ignore[reportMissingTypeStubs]
    NuitkaPluginBase,
)


class UnityPyNuitkaPlugin(NuitkaPluginBase):
    plugin_name = "unitypy-nuitka-plugin"

    def decideCompilation(self, module_name):  # type: ignore
        # Too large generated code.
        # cl.exe hits C1002 (out of heap space in pass 2) trying to compile this to C.
        # Ship as bytecode instead.
        if module_name == "UnityPy.classes.generated":
            return "bytecode"
        return None
