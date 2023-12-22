import cmd, logging

from liminalstate.internal.base.base import LiminalBase

logger = logging.getLogger(__name__)


class LiminalCLI(cmd.Cmd):
    intro = "Welcome to the liminal-state-shell. Type help or ? to list commands."
    prompt = "(wow-liminal-state) "

    def __init__(self, config_path: str):
        super().__init__()
        self.base = LiminalBase(config_path)

    def emptyline(self):
        pass

    def do_exit(self, _):
        logger.info("Application exit.")
        return True
    
    def do_lookup(self, _):

        type = input("Enter the type of entry you want to lookup (item, mob): ")

        if type != "item" and type != "mob":
            logger.error(
                f"Invalid entry type. Please enter either item or mob: {type}"
            )
            return
        
        name = input("Enter the name of the item or mob you want to lookup: ")
        
        if type == "item":
            row = self.base.get_single("name", name, self.base.world, "item_template")
            if row is None:
                logger.error(f"Could not find item: {name}")
                return
        elif type == "mob":
            row = self.base.get_single("Name", name, self.base.world, "creature_template")
            if row is None:
                logger.error(f"Could not find mob: {name}")
                return
        
        logger.info(f"ID: {row['entry']}")

    def do_edit(self, line: str):
        args = line.split()
        if len(args) == 0:
            logger.error("Please enter which entry you want to edit (item, mob)")
            return

        if args[0] != "item" and args[0] != "mob":
            logger.error(
                f"Invalid entry type. Please enter either item or mob: {args[0]}"
            )
            return

        id = input("Enter the database entry id you want to edit: ")

        try:
            int(id)
        except ValueError:
            logger.error("Please enter a valid integer.")
            return

        match args[0]:
            case "item":
                row = self.base.get_single(
                    "entry", id, self.base.world, "item_template"
                )
                logger.info(f"Editing item: {row['name']}")
                table = "item_template"
            case "mob":
                row = self.base.get_single("entry", id, self.base.world, "creature_template")
                logger.info(f"Editing mob: {row['Name']}")
                table = "creature_template"
            
        see_all = input("Would you like to view all fields? (y/n): ")

        if see_all == "y":
            for key, value in row.items():
                logger.info(f"{key}: {value}")
        elif see_all == "n":
            pass
        else:
            logger.error("Invalid input.")
            return

        field = input("Enter the field you want to edit: ")
        try:
            field_value = row[field]
        except KeyError:
            logger.error(f"Invalid field: {field}")
            return
        logger.info(f"Editing column: {field}")
        logger.info(f"Current value: {field_value}")
        value = input("Enter the new value: ")
        success = self.base.update_single_field(
            "entry", id, field, value, self.base.world, table
        )
        if not success:
            logger.error("Failed to update field.")
            return
        logger.info("Successfully updated field.")

    def do_duplicate(self, line: str):
        raise NotImplementedError
