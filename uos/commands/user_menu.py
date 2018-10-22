from ..uos import UOS


class UserMenu:
    def user_menu_commands(self):
        return {
            'MENU': self.command_menu,
            'MENU ADD': self.command_menu_add,
            'MENU EDIT': self.command_menu_edit,
            'MENU REMOVE': self.command_menu_remove,
            'MENU RESET': self.command_menu_reset
        }

    def command_menu(self):
        self.link.action.flip('MenuMenu')

    def command_menu_add(self, menu_name, index, *args):
        if index.isdigit():
            index = int(index)
        else:
            self.writer_add('Index must be an integer')
            return

        default = list(UOS.user.default_menu().keys())
        default.remove('MainMenu')

        # looking for a simple 2 or 3 argruments command
        if len(args) in [2,3]:
            boolean_simple = len(args)
            for arg in args:
                if not isinstance(arg, str):
                    boolean_simple = False
                if ',' in arg:
                    boolean_simple = False
        else:
            boolean_simple = False

        if boolean_simple == 2:
            command = ""
            action, name = args
        elif boolean_simple:
            action, name, command = args
        else:
            arg_split = []
            arg_data = []
            for arg in args:
                if arg.startswith('-') and arg_data != []:
                    arg_split.append(arg_data)
                    arg_data = [arg]
                elif arg.endswith(','):
                    arg_data.append(arg[:-1])
                    arg_split.append(arg_data)
                    arg_data = []
                else:
                    arg_data.append(arg)

            if arg_data != []:
                arg_split.append(arg_data)

            if len(arg_split[0]) == 2:
                action = arg_split[0][0]
                name = arg_split[0][1]
            elif len(arg_split[0]) > 2:
                action = arg_split[0][0]
                name = arg_split[0][1:]

            if len(arg_split) > 1:
                if action in ['-t', 'TEXT']:
                    command = []
                    for arg in arg_split[1:]:
                        command.append((arg[0], ' '.join(arg[1:])))
                else:
                    if len(arg_split[1:]) == 1:
                        command = ' '.join(arg_split[1])
                    else:
                        self.writer_add('To many arguments')
                        return
            else:
                command = ""

        if menu_name not in default:
            if menu_name in UOS.user.current.menu.keys():
                allowed_actions = { '-t': 'Text',
                                  '-m': 'SubMenu',
                                  '-n': 'Nested',
                                  '-s': 'Selection',
                                  'SELECTION': 'Selection',
                                  'SUBMENU': 'SubMenu',
                                  'NESTED': 'Nested',
                                  'TEXT': 'Text'
                                }

                if action in allowed_actions.keys():
                    action = allowed_actions[action]
                else:
                    self.writer_add(action + ' invalid action')
                    return

                UOS.user.current.menu[menu_name].insert(index, [action, name, command])
                # create an empty submenu
                if action == "SubMenu":
                    if not UOS.user.current.menu.get(name, False):
                        UOS.user.current.menu[name] = []
                UOS.user.save()

            else:
                self.writer_add(menu_name + " does not exists")
        else:
            self.writer_add(menu_name + " item can not be added")

    def command_menu_edit(self, menu_name, index, action, *args):
        default = list(UOS.user.default_menu().keys())
        default.remove('MainMenu')
        if index.isdigit():
            index = int(index)
        else:
            self.writer_add('Index must be an integer')
            return

        command = ' '.join(args)
        if menu_name not in default:
            if menu_name in UOS.user.current.menu.keys():
                if action in ['-t', 'TEXT']:
                    item = UOS.user.current.menu[menu_name][index][1]
                    UOS.user.current.menu[menu_name][index][1] = command
                    self.writer_add(item + " been change to " + command)
                    UOS.user.save()
                elif action in ['-s', 'SELECTION']:
                    item = UOS.user.current.menu[menu_name][index][2]
                    UOS.user.current.menu[menu_name][index][2] = command
                    self.writer_add(item + " been change to " + command)
                    UOS.user.save()
            else:
                self.writer_add(menu_name + " does not exists")
        else:
            self.writer_add(menu_name + " item can not be altered")

    def command_menu_remove(self, menu_name, index):
        default = list(UOS.user.default_menu().keys())
        default.remove('MainMenu')
        if index.isdigit():
            index = int(index)
        else:
            self.writer_add('Index must be an integer')
            return

        if menu_name not in default:
            if menu_name in UOS.user.current.menu.keys():
                item = UOS.user.current.menu[menu_name].pop(index)
                self.writer_add(item[1] + " has been removed")
                UOS.user.save()
            else:
                self.writer_add(menu_name + " does not exists")
        else:
            self.writer_add(menu_name + " item can not be removed")

    def command_menu_reset(self):
        UOS.user.current.menu = UOS.user.default_menu()
        self.writer_add("Menu has been reset to default")
        UOS.user.save()
