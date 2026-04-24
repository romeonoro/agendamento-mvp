from datetime import datetime, time
from api.agendamento import Medico, ForaDoHorarioError, ConflitoHorarioError

def simular_dia_na_clinica():
    print("=== INICIANDO SISTEMA DE AGENDAMENTOS ===\n")

    dr_house = Medico(nome="Dr. House", inicio_turno=time(8, 0), fim_turno=time(12, 0), intervalo_atendimento=30)
    print(f"👨‍⚕️ Médico cadastrado: {dr_house._nome}")
    print(f"⏰ Turno: 08:00 às 12:00 (Consultas de 30 min)\n")

    try:
        print("Tentando agendar Paciente ID 101 para 09:00...")
        dr_house.agendar(paciente_id=101, data_hora=datetime(2026, 4, 25, 9, 0))
        print("✅ Sucesso: Consulta agendada!\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")

    try:
        print("Tentando agendar Paciente ID 102 para 14:00...")
        dr_house.agendar(paciente_id=102, data_hora=datetime(2026, 4, 25, 14, 0))
        print("✅ Sucesso: Consulta agendada!\n")
    except ForaDoHorarioError as e:
        print(f"❌ Bloqueado (Fora do Horário): {e}\n")

    try:
        print("Tentando agendar Paciente ID 103 para 09:15...")
        dr_house.agendar(paciente_id=103, data_hora=datetime(2026, 4, 25, 9, 15))
        print("✅ Sucesso: Consulta agendada!\n")
    except ConflitoHorarioError as e:
        print(f"❌ Bloqueado (Conflito): {e}\n")

    print("=== AGENDA FINAL DO DR. HOUSE ===")
    for consulta in dr_house.agendamentos:
        print(f"📅 Início: {consulta.inicio.strftime('%H:%M')} | Fim: {consulta.fim.strftime('%H:%M')} | Paciente: {consulta.paciente_id}")

if __name__ == "__main__":
    simular_dia_na_clinica()