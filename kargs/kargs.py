import os
import kconfiglib

class Kargs():
    def __init__(self, parser, kconfig="Kconfig", config=".config"):
        self.excluded_groups = []
        self.excluded_options = []
        self.menu_name = "Autogenerated Kconfig"

        self._kconfig = kconfig
        self._config = config
        self._parser = parser

        parser.add_target_argument("--config", action="store_true", help="Generate a Kconfig file")

    def get_group_dict(self, args):
        arg_groups = {}
        for group in self._parser._action_groups:
            if group.title not in self.excluded_groups:
                group_dict = {a.dest : (getattr(args, a.dest, None), a.help) for a in group._group_actions}
                for opt in self.excluded_options:
                    if opt in group_dict:
                        del group_dict[opt]
                if bool(group_dict):
                    arg_groups[group.title] = group_dict
        return arg_groups

    def get_exclusivity_list(self):
        exclusive_groups = []
        for group in self._parser._mutually_exclusive_groups:
            same_group = []
            for action in group._group_actions:
                same_group.append(action.dest)
            exclusive_groups.append(same_group)
        return exclusive_groups

    def get_exclusive_symbols(self, symbol, exclusive_groups):
        depends = {}
        for i, group in enumerate(exclusive_groups):
            for symbol in group:
                cond = []
                if i == 0:
                    cond = None
                else:
                    for g in range(i):
                        for s in exclusive_groups[g]:
                            cond.append(f"!{s.upper()}")
                depends[symbol] = " && ".join(cond) if cond != None else None

        return depends

    def build_kconfig(self, args, kconfig_name="Kconfig"):
        arg_groups = self.get_group_dict(args)
        exclusive_groups = self.get_exclusivity_list()

        with open(kconfig_name, "w") as f:
            f.write(f'mainmenu "{self.menu_name}"\n\n')
            for m in arg_groups:
                f.write(f'menu "{m}"\n\n')
                argdict = arg_groups[m]
                for t in argdict:
                    val, help = argdict[t]
                    is_exclusive = any(t in l for l in exclusive_groups)
                    if is_exclusive:
                        depends = self.get_exclusive_symbols(t, exclusive_groups)
                    if isinstance(val, bool):
                        f.write(f'config {t.upper()}\n')
                        f.write(f'\tbool "{t.upper()}"\n')
                        f.write(f'\tdefault {"y" if val else "n"}\n')
                    elif isinstance(val, str):
                        f.write(f'config {t.upper()}\n')
                        f.write(f'\tstring "{t.upper()}"\n')
                        s = val
                        if s == "default":
                            s = ""
                        f.write(f'\tdefault "{s}"\n')
                    # Assume that an empty string is None
                    elif val == None:
                        f.write(f'config {t.upper()}\n')
                        f.write(f'\tstring "{t.upper()}"\n')
                        f.write(f'\tdefault ""\n')
                    elif isinstance(val, int):
                        f.write(f'config {t.upper()}\n')
                        f.write(f'\tint "{t.upper()}"\n')
                        f.write(f'\tdefault {val}\n')
                    elif isinstance(val, float):
                        f.write(f'config {t.upper()}\n')
                        f.write(f'\tstring "{t.upper()}"\n')
                        f.write(f'\tdefault "{val}"\n')
                    else:
                        # print(f"{t} {type(argdict[t])} {val} {help}")
                        pass
                    if is_exclusive:
                        if depends[t]:
                            f.write(f'\tdepends on {depends[t]}\n')
                    if help:
                        f.write(f'\thelp\n\t  {help}\n')
                f.write("endmenu\n")

    def create_arg_list(self):
        arg_list = []
        if os.path.isfile(self._kconfig) and os.path.isfile(self._config):
            kconf = kconfiglib.Kconfig(self._kconfig)
            kconf.load_config(self._config)
            for sym in kconf.unique_defined_syms:
                if sym.type == kconfiglib.BOOL:
                    if sym.str_value == "y":
                        arg_list.append("--" + sym.name.replace("_", "-").lower())
                if sym.type == kconfiglib.INT:
                    name = sym.name.replace("_", "-").lower()
                    arg_list.append(f"--{name}={sym.str_value}")
                if sym.type == kconfiglib.STRING:
                    if sym.str_value != "":
                        name = sym.name.replace("_", "-").lower()
                        arg_list.append(f"--{name}={sym.str_value}")
        return arg_list
