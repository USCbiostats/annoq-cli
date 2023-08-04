import argparse
import shlex
import psutil
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit import PromptSession

from src.utils import load_json

VARIABLES = {}

def load(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True)
    parser.add_argument('--vcf', required=False)
    parser.add_argument('--rsid', required=False)
    parser.add_argument('--chr', required=False)

    try:
        parsed_args = parser.parse_args(shlex.split(' '.join(args)))
        print(f"Loading with config: {parsed_args.config}, vcf: {parsed_args.vcf}, rsid: {parsed_args.rsid}, chr: {parsed_args.chr}")
        config = load_json(parsed_args.config)
        VARIABLES['config'] = config
        print(f"You have the following config:\n {config}")
    except SystemExit:
        pass  # Ignore exit() call in argparse error handling


def search(*args):
    print(f"Searching with args: {args}")

def search_chr(*args):
    print(f"Searching chromosome with args: {args}")

def search_gp(*args):
    print(f"Searching gene product with args: {args}")

def search_rsid(*args):
    print(f"Searching rsid with args: {args}")

def reset(*args):
    print(f"Resetting with args: {args}")

def download(*args):
    print(f"Downloading with args: {args}")

def submit(*args):
    print(f"Submitting with args: {args}")

def set_var(args):
    name, value = args.split()
    VARIABLES[name] = value

def get_var(args):
    name = args.strip()
    if name in VARIABLES:
        print(f"{name} = {VARIABLES[name]}")
    else:
        print(f"No variable named {name}")
        
def print_memory_usage(*args):
    process = psutil.Process()
    mem_info = process.memory_info()
    print(f"Current memory usage: {mem_info.rss / 1024 / 1024} MB")
        
# Map command names to functions
COMMANDS = {
    "set": set_var,
    "get": get_var,
    "load": load,
    "search": search,
    "search_chr": search_chr,
    "search_gp": search_gp,
    "search_rsid": search_rsid,
    "reset": reset,
    "download": download,
    "submit": submit,
    "memory": print_memory_usage,
}

def main():
    session = PromptSession(auto_suggest=AutoSuggestFromHistory(), completer=PathCompleter())

    while True:
        try:
            text = session.prompt('YourApp> ', auto_suggest=AutoSuggestFromHistory(), completer=PathCompleter())
            if text.lower() == "exit":
                break
            else:
                cmd, *args = text.split()
                if cmd in COMMANDS:
                    try:
                        COMMANDS[cmd](*args)
                    except Exception as e:
                        print(f"Error executing command: {e}")                    
                else:
                    print(f"Unknown command: {cmd}")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

    print("Goodbye!")



def parse_arguments():
    parser = argparse.ArgumentParser(description='Loads pmids',
                                     epilog='It works!')

if __name__ == "__main__":
    main()


# python3 -m main
# load -c resources/sample_data/config.txt