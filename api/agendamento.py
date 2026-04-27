from datetime import datetime, time, timedelta
from api.exceptions import ForaDoHorarioError, ConflitoHorarioError, IntervaloInvalidoError

class Agendamento:
    def __init__(self, paciente_id: int, inicio: datetime, duracao_minutos: int = 30):
        self._paciente_id = paciente_id
        self._inicio = inicio
        self._duracao = timedelta(minutes=duracao_minutos) 

    @property
    def inicio(self) -> datetime:
        return self._inicio
    @property
    def fim(self) -> datetime:
        return self._inicio + self._duracao

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

    def _esta_no_horario_de_trabalho(self, agendamento: Agendamento) -> bool:
        return (self._inicio_turno <= agendamento.inicio.time() and 
                agendamento.fim.time() <= self._fim_turno)

    def _existe_conflito(self, novo_agendamento: Agendamento) -> bool:
        for agendamento_existente in self._agendamentos:
            if (novo_agendamento.inicio < agendamento_existente.fim and 
                novo_agendamento.fim > agendamento_existente.inicio):
                return True
        return False

    def _respeita_grade_de_intervalo(self, data_hora: datetime) -> bool:
        return data_hora.minute % self._intervalo_atendimento == 0

    def agendar(self, paciente_id: int, data_hora: datetime) -> None:
        novo_agendamento = Agendamento(
            paciente_id=paciente_id, 
            inicio=data_hora, 
            duracao_minutos=self._intervalo_atendimento
        )
        
        if not self._esta_no_horario_de_trabalho(novo_agendamento):
            raise ForaDoHorarioError("Médico não está disponível neste horário.")
            
        if self._existe_conflito(novo_agendamento):
            raise ConflitoHorarioError("Conflito de Horário.")

        if not self._respeita_grade_de_intervalo(data_hora):
            raise IntervaloInvalidoError(f"O horário deve ser em blocos de {self._intervalo_atendimento} minutos.")
            
        self._agendamentos.append(novo_agendamento)

    