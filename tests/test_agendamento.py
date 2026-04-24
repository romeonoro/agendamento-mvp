import unittest
from datetime import datetime, time 
from api.agendamento import Medico

class TestAgendamento(unittest.TestCase):

    def test_agendamento_com_sucesso(self):
        medico = Medico(nome = "Dr. House", inicio_turno = time(8, 0), fim_turno = time(12, 0), intervalo_atendimento = 30)
        
        self.assertEqual(len(medico.agendamentos),0)

        horario_desejado = datetime(2026, 4, 24, 9, 0)
        paciente_id = 123

        medico.agendar(paciente_id=paciente_id, data_hora=horario_desejado)

        self.assertEqual(len(medico.agendamentos),1)
        
        agendamento_criado = medico.agendamentos[0]
        self.assertEqual(agendamento_criado.inicio, horario_desejado)
        self.assertEqual(agendamento_criado.paciente_id, paciente_id)
