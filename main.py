from datetime import datetime, time

from api.agendamento import Medico
from api.exceptions import (
    ConflitoHorarioError,
    ForaDoHorarioError,
    IntervaloInvalidoError,
)
from infra.repository import AgendamentoRepositorio


def simular_dia_na_clinica():
    print("=== INICIANDO SISTEMA DE AGENDAMENTOS (COM REPOSITÓRIO) ===\n")

    # 1. Instancia as dependências
    repo = AgendamentoRepositorio()
    dr_house = Medico(
        nome="Dr. House",
        inicio_turno=time(8, 0),
        fim_turno=time(12, 0),
        intervalo_atendimento=30,
    )

    print(f"👨‍⚕️ Médico cadastrado: {dr_house._nome}")
    print("⏰ Turno: 08:00 às 12:00 (Consultas de 30 min)\n")

    # 2. Função Orquestradora
    def tentar_agendar(paciente_id: int, data_hora: datetime):
        hora_str = data_hora.strftime("%H:%M")
        print(f"Tentando agendar Paciente ID {paciente_id} para {hora_str}...")

        try:
            agenda_atual = repo.buscar_todos()
            nova_consulta = dr_house.agendar(paciente_id, data_hora, agenda_atual)
            repo.adicionar(nova_consulta)
            print("✅ Sucesso: Consulta agendada!\n")

        except ForaDoHorarioError as e:
            print(f"❌ Bloqueado (Fora do Horário): {e}\n")
        except IntervaloInvalidoError as e:
            print(f"❌ Bloqueado (Grade Inválida): {e}\n")
        except ConflitoHorarioError as e:
            print(f"❌ Bloqueado (Conflito): {e}\n")
        except Exception as e:
            print(f"❌ Erro Inesperado: {e}\n")

    # 3. Executando os Cenários
    tentar_agendar(paciente_id=101, data_hora=datetime(2026, 4, 25, 9, 0))
    tentar_agendar(paciente_id=102, data_hora=datetime(2026, 4, 25, 14, 0))
    tentar_agendar(paciente_id=103, data_hora=datetime(2026, 4, 25, 9, 15))
    tentar_agendar(paciente_id=104, data_hora=datetime(2026, 4, 25, 9, 0))

    # 4. Exibindo o estado final do Repositório
    print("=== AGENDA FINAL NO REPOSITÓRIO ===")
    consultas_salvas = repo.buscar_todos()

    if not consultas_salvas:
        print("Nenhuma consulta agendada.")
    else:
        for consulta in consultas_salvas:
            inicio = consulta.inicio.strftime("%H:%M")
            fim = consulta.fim.strftime("%H:%M")

            print(
                f"📅 Início: {inicio} | Fim: {fim} "
                f"| Paciente: {consulta.paciente_id}"
            )


if __name__ == "__main__":
    simular_dia_na_clinica()
