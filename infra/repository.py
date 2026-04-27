from api.agendamento import Agendamento


class AgendamentoRepositorio:
    def __init__(self):
        self._agendamentos: list[Agendamento] = []

    def adicionar(self, agendamento: Agendamento) -> None:
        self._agendamentos.append(agendamento)

    def buscar_todos(self) -> list[Agendamento]:
        return list(self._agendamentos)
