**Kargs, the argparse <-> Kconfig tool**

This project adds Kconfig support to any project using argparse.
The usage of Kconfig is optional and only a few changes are necessary in the code base.

The tool needs Kconfiglib. This library installs menuconfig, savedefconfig,...

Once the Kconfig is generated from the default values, just run `menuconfig`

**Usage**


```python
import kargs
#...
def  main():
#...
    parser.add_target_argument("--first-argument", action="store_true", help="Test 1")
    parser.add_target_argument("--second-argument", action="store_true", help="Test 2")
#...
    # Reads the Kconfig and .config files and generate the argument list.
    # If either Kconfig or .config are not present, the arguments are only the ones from the command line.
    # Kargs also adds a --config argument to create the Kconfig file from the arguments default values.
    config = kargs.Kargs(parser)
    arg_list = config.create_arg_list()
#...
    args = parser.parse_args(sys.argv[1:] + arg_list)
#...
    # This creates the Kconfig file
    if args.config:
        config.excluded_options = ["build", "flash", "load", "config", "help"]
        config.build_kconfig(args)
#...
```
