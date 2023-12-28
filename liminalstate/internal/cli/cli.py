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
        """
        Exit the application.
        """

        logger.info("Application exit.")
        return True

    def cmdloop(self):
        """
        Override the default cmdloop method to handle KeyboardInterrupt.
        """

        print(self.intro)

        while True:
            try:
                super().cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("^C")
                continue

    def do_lookup(self, line):
        """
        Lookup an item or mob by name - will rturn all entries with that name and their respective fields/values.
        """

        if len(line) == 0:
            logger.error("Please enter which entry you want to lookup (item, mob)")
            return

        split_line = line.split()

        if split_line[0] != "item" and split_line[0] != "mob":
            logger.error(
                f"Invalid entry type. Please enter either item or mob, not: {split_line[0]}"
            )
            return

        name = input("Enter the name of the item or mob you want to lookup: ")

        if split_line[0] == "item":
            row = self.base.get_multiple("name", name, "world", "item_template")
            if row is None:
                logger.error(f"Could not find item: {name}")
                return
        elif split_line[0] == "mob":
            row = self.base.get_multiple("Name", name, "world", "creature_template")
            if row is None:
                logger.error(f"Could not find mob: {name}")
                return

        logger.info(f"Found {len(row)} entries.")

        for entry in row:
            for key, value in entry.items():
                logger.info(f"{key}: {value}")
            logger.info("--------------------")

    def do_edit(self, line: str):
        """
        Edit an item or mob by id. Will list all fields and their values, and allow you to edit them.
        """
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

        while True:
            match args[0]:
                case "item":
                    row = self.base.get_single("entry", id, "world", "item_template")
                    logger.info(f"Editing item: {row['name']}")
                    table = "item_template"
                case "mob":
                    row = self.base.get_single(
                        "entry", id, "world", "creature_template"
                    )
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
                continue

            field = input("Enter the field you want to edit: ")
            try:
                field_value = row[field]
            except KeyError:
                logger.error(f"Invalid field: {field}")
                continue

            logger.info(f"Editing column: {field}")
            logger.info(f"Current value: {field_value}")

            if field in [
                "MinLevelHealth",
                "MaxLevelHealth",
                "MinLevelMana",
                "MaxLevelMana",
            ]:
                increase_percent = input("Enter the percent increase: ")
                try:
                    increase_percent = float(increase_percent)
                except ValueError:
                    logger.error("Not a valid float value.")
                    continue
                value = int(field_value * (1 + increase_percent))
            else:
                value = input("Enter the new value: ")

            success = self.base.update_single_field(
                "entry", id, field, value, "world", table
            )

            if not success:
                logger.error("Failed to update field.")
            else:
                logger.info(f"Successfully updated field to {value}.")

            again = input("Would you like to edit another field? (y/n): ")
            if again == "y":
                continue
            elif again == "n":
                break
            else:
                logger.error("Invalid input.")
                continue

    def do_wizard(self, line):
        """
        Wizard to easily create/dupe items, mobs and quests.
        """

        if len(line) == 0:
            logger.error(
                "Please enter which entry you want to create (item, mob, quest)"
            )
            return

        split_line = line.split()

        if (
            split_line[0] != "item"
            and split_line[0] != "mob"
            and split_line[0] != "quest"
        ):
            logger.error(
                f"Invalid entry type. Please enter either item, mob or quest, not: {split_line[0]}"
            )
            return

        logger.info(
            "You are in the wizard. The wizard will guide you through the process of creating a new entry. In order to create a new entry, you must duplicate an existing one. Please enter the id of the entry you want to duplicate."
        )

        if split_line[0] == "item":
            table = "item_template"
        elif split_line[0] == "mob":
            table = "creature_template"
        elif split_line[0] == "quest":
            table = "quest_template"

        while True:
            id = input("Enter the id of the entry you want to duplicate: ")

            try:
                int(id)
            except ValueError:
                logger.error("Please enter a valid integer.")
                continue

            row = self.base.get_single("entry", id, "world", table)

            if row is None:
                logger.error(f"Could not find entry with id: {id}")
                continue

            logger.info("Found entry:")
            for key, value in row.items():
                logger.info(f"{key}: {value}")

            confirm = input("Is this the entry you want to duplicate? (y/n): ")

            if confirm == "y":
                break
            elif confirm == "n":
                continue
            else:
                logger.error("Invalid input.")
                continue
        for key, value in row.items():
            logger.info(f"{key}: {value}")
            new_value = input(f"Enter the new value for {key}: ")
            if new_value == "":
                continue
            row[key] = new_value
        
        if split_line[0] == "item":
            self.base.add_entry("world", "item_template", row)
        elif split_line[0] == "mob":
            self.base.add_entry("world", "creature_template", row)
        elif split_line[0] == "quest":
            self.base.add_entry("world", "quest_template", row)
