from datetime import datetime, time, timedelta

class Agendamento:
    def __init__(self, paciente_id: int, inicio: datetime, duracao_minutos: int = 30):
        self._paciente_id = paciente_id
        self._inicio = inicio
        self._duracao = timedelta(minutes=duracao_minutos) 

    @property
    def inicio(self) -> datetime:
        return self._inicio
        
    @property
    def paciente_id(self) -> int:
        return self._paciente_id

class Medico:
    def __init__(self, nome: str, inicio_turno: time, fim_turno: time, intervalo_atendimento: int = 30):
        self._nome = nome
        self._inicio_turno = inicio_turno
        self._fim_turno = fim_turno
        self._intervalo_atendimento = intervalo_atendimento
        self._agendamentos = [] 
        
    @property
    def agendamentos(self) -> tuple:
        return tuple(self._agendamentos)

    def agendar(self, paciente_id: int, data_hora: datetime) -> None:
        novo_agendamento = Agendamento(
            paciente_id=paciente_id, 
            inicio=data_hora, 
            duracao_minutos=self._intervalo_atendimento
        )
        self._agendamentos.append(novo_agendamento)