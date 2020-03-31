import pynvim

from .sphinx_nvim import Settings, get_completion_list


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
        return Settings(**settings_dict)

    @pynvim.function("CocSphinxList", sync=True)
    def list(self, args):
        options = args[0]
        filepath = options.get("filepath")
        line = options.get("line")
        colnr = options.get("colnr") - 1

        results = []
        try:
            results = get_completion_list(filepath, line, colnr, self.settings)
            return results
        except Exception as e:
            self.nvim.err_write(f"[sphinx] {e}\n")
        return results
