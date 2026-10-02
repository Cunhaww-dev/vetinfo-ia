# no nível do arquivo só ficam definições (def, class, constantes); ação fica dentro de função.


def get_greeting(name: str, project: str) -> str:
    message = f"Olá, {name} o projeto é o {project}."
    return message


def main() -> None:
    dev_name = "Lucas Fabri"
    project_name = "vetinfo_ia"

    greeting = get_greeting(dev_name, project_name)
    print(greeting)
