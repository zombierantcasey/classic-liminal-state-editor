import cmd, logging

logger = logging.getLogger(__name__)

class LiminalCLI(cmd.Cmd):
    intro = 'Welcome to the liminal-state-shell. Type help or ? to list commands.'
    prompt = '(wow-liminal-state) '

    def emptyline(self):
        pass  

    def do_exit(self):
        logger.info("Exiting the application.")
        return True 

    def do_edit(self, line: str):
        args = line.split()
        if len(args) == 0:
            logger.error("Please enter which entry you want to edit (item, mob)")
            return
        
        if args[0]  != "item" or args[0] != "mob":
            logger.error(f"Invalid entry type. Please enter either item or mob: {args[0]}")
            return
        
        id = input("Enter the database entry id you want to edit: ")

        try: 
            int(id)
        except ValueError:
            logger.error("Please enter a valid integer.")
            return
        
        match args[0]:
            case "item":
                raise NotImplementedError
            case "mob":
                raise NotImplementedError
        
    def do_duplicate(self, line: str): 
        raise NotImplementedError
        