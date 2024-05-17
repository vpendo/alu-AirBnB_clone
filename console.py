#!/usr/bin/python3
"""
This file defines the CommandInterpreter class which will
serve as the entry point of the entire project
"""

from cmd import Cmd
from models import storage
from models.engine.errors import *
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


# Global variable of registered models
registered_models = storage.models


class CommandInterpreter(Cmd):
    """
    The Command Interpreter serves as the main interface for the AirBnb Clone
    All interactions with the system are facilitated through this class"""

    prompt = "(airbnb) "

    """Commands"""
    def do_EOF(self, args):
        """Exit the program in non-interactive mode"""
        return True

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_create(self, args):
        """Create an instance of a Model given its name, e.g.,
        $ create ModelName
        Throws an Error if ModelName is missing or doesn't exist"""
        args, n = parse(args)

        if not n:
            print("** Model name missing **")
        elif args[0] not in registered_models:
            print("** Model doesn't exist **")
        elif n == 1:
            temp = eval(args[0])()
            print(temp.id)
            temp.save()
        else:
            print("** Too many arguments for create **")

    def do_display(self, arg):
        """Displays the specified instance of a Model based on its ModelName and id, e.g.,
        $ display ModelName instance_id
        Prints error message if either ModelName or instance_id is missing
        Prints an Error message for a wrong ModelName or instance_id"""
        args, n = parse(arg)

        if not n:
            print("** Model name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            try:
                instance = storage.find_by_id(*args)
                print(instance)
            except ModelNotFoundError:
                print("** Model doesn't exist **")
            except InstanceNotFoundError:
                print("** No instance found **")
        else:
            print("** Too many arguments for display **")

    def do_remove(self, arg):
        """Deletes an instance of a Model based on its ModelName and id."""
        args, n = parse(arg)

        if not n:
            print("** Model name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            try:
                storage.delete_by_id(*args)
            except ModelNotFoundError:
                print("** Model doesn't exist **")
            except InstanceNotFoundError:
                print("** No instance found **")
        else:
            print("** Too many arguments for remove **")

    def do_list(self, args):
        """Usage: list or list <ModelName> or <ModelName>.list()
        Display string representations of all instances of a given model.
        If no model is specified, displays all instantiated objects."""
        args, n = parse(args)

        if n < 2:
            try:
                print(storage.find_all(*args))
            except ModelNotFoundError:
                print("** Model doesn't exist **")
        else:
            print("** Too many arguments for list **")

    def do_modify(self, arg):
        """Updates an instance based on its id, e.g.,
        $ modify Model id field value
        Throws errors for missing arguments"""
        args, n = parse(arg)
        if not n:
            print("** Model name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            print("** attribute name missing **")
        elif n == 3:
            print("** value missing **")
        else:
            try:
                storage.update_one(*args[0:4])
            except ModelNotFoundError:
                print("** Model doesn't exist **")
            except InstanceNotFoundError:
                print("** No instance found **")

    def do_registered_models(self, arg):
        """Prints all registered Models"""
        print(*registered_models)

    def handle_model_methods(self, arg):
        """Handle Model Methods, e.g., <ModelName>.list(), <ModelName>.display() etc"""

        printable = ("list(", "display(", "count(", "create(")
        try:
            val = eval(arg)
            for x in printable:
                if x in arg:
                    print(val)
                    break
            return
        except AttributeError:
            print("** Invalid method **")
        except InstanceNotFoundError:
            print("** No instance found **")
        except TypeError as te:
            field = te.args[0].split()[-1].replace("_", " ")
            field = field.strip("'")
            print(f"** {field} missing **")
        except Exception as e:
            print("** Invalid syntax **")
            pass

    def default(self, arg):
        """Override default method to handle model methods"""
        if '.' in arg and arg[-1] == ')':
            if arg.split('.')[0] not in registered_models:
                print("** Model doesn't exist **")
                return
            return self.handle_model_methods(arg)
        return Cmd.default(self, arg)

    def emptyline(self):
        """Override empty line to do nothing"""
        return


def parse(line: str):
    """Splits a line by spaces"""
    args = shlex.split(line)
    return args, len(args)


if __name__ == "__main__":
    CommandInterpreter().cmdloop()
