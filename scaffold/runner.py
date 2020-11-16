from prompt_toolkit import PromptSession

from scaffold.scaffold import Scaffold
from scaffold.utils import prompt_parse


def main():
    session = PromptSession()
    while True:
        try:
            text = session.prompt('> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        scaffold = Scaffold(*prompt_parse(text))
        scaffold.execute()
        #print(f'app={scaffold.app}', f'model={scaffold.model}', f'fields={scaffold.fields}')

if __name__ == '__main__':
    main()
