from pathlib import Path

import pynvim

from .sphinx_nvim import (
    Settings,
    get_completion_list,
    get_references_list,
    get_roles_list,
)


@pynvim.plugin
class Plugin:
    def __init__(self, nvim):
        self.nvim = nvim

    @property
    def settings(self):
        settings_dict = {
            option: self.nvim.vars.get(f"sphinx_{option}")
            for option in Settings._fields
        }
        # For debug only
        settings_dict["nvim"] = self.nvim
        return Settings(**settings_dict)

    @pynvim.function("CocSphinxList", sync=True)
    def coc_list(self, args):
        options = args[0]
        filepath = options.get("filepath")
        line = options.get("line")
        colnr = options.get("colnr") - 1

        results = []
        try:
            results = get_completion_list(
                filepath,
                line,
                colnr,
                self.settings,
            )
            return results
        except Exception as e:
            error = str(e)
            self.nvim.err_write(f"[sphinx] {error}\n")
        return results

    @pynvim.function("FzfSphinxList", sync=True)
    def fzf_list(self, args):
        role = args[0] if args else None
        results = get_references_list(
            cwd=Path(self.nvim.funcs.getcwd()),
            role=role,
            settings=self.settings,
        )
        return results

    @pynvim.function("SphinxRoles", sync=True)
    def list_roles(self, args):
        results = get_roles_list(
            cwd=Path(self.nvim.funcs.getcwd()),
            settings=self.settings,
        )
        return results
