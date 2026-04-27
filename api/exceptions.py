class ForaDoHorarioError(Exception):
    def __init__(self, message="Médico não está disponível neste horário."):
        super().__init__(message)


class ConflitoHorarioError(Exception):
    def __init__(self, message="Conflito de Horário."):
        super().__init__(message)


class IntervaloInvalidoError(Exception):
    def __init__(self, message="O horário deve respeitar a grade de intervalos."):
        super().__init__(message)


class AgendamentoNaoEncontradoError(Exception):
    def __init__(self, paciente_id: int):
        mensagem = f"Nenhuma consulta encontrada para o Paciente {paciente_id}."
        super().__init__(mensagem)
