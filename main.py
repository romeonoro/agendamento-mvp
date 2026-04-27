from datetime import datetime, time
from api.agendamento import Medico
from api.exceptions import ForaDoHorarioError, ConflitoHorarioError, IntervaloInvalidoError
from infra.repository import AgendamentoRepositorio

def simular_dia_na_clinica():
    print("=== INICIANDO SISTEMA DE AGENDAMENTOS (COM REPOSITÓRIO) ===\n")

    # 1. Instancia as dependências (Banco e Entidade)
    repo = AgendamentoRepositorio()
    dr_house = Medico(nome="Dr. House", inicio_turno=time(8, 0), fim_turno=time(12, 0), intervalo_atendimento=30)
    
    print(f"👨‍⚕️ Médico cadastrado: {dr_house._nome}")
    print(f"⏰ Turno: 08:00 às 12:00 (Consultas de 30 min)\n")

    # 2. Função Orquestradora (O nosso "Caso de Uso")
    def tentar_agendar(paciente_id: int, data_hora: datetime):
        print(f"Tentando agendar Paciente ID {paciente_id} para {data_hora.strftime('%H:%M')}...")
        try:
            # Passo A: Pega os dados atuais do banco
            agenda_atual = repo.buscar_todos()
            
            # Passo B: O Domínio executa as regras e devolve a consulta pronta
            nova_consulta = dr_house.agendar(paciente_id, data_hora, agenda_atual)
            
            # Passo C: O banco salva o dado validado
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

    # 3. Executando os Cenários (Testando os Contratos)
    
    # Cenário 1: Sucesso
    tentar_agendar(paciente_id=101, data_hora=datetime(2026, 4, 25, 9, 0))   
    
    # Cenário 2: Fora do Horário (RF02) - Tenta marcar 14h00
    tentar_agendar(paciente_id=102, data_hora=datetime(2026, 4, 25, 14, 0))  
    
    # Cenário 3: Horário Fragmentado (Nova Regra) - Tenta marcar 09h15
    tentar_agendar(paciente_id=103, data_hora=datetime(2026, 4, 25, 9, 15))  
    
    # Cenário 4: Conflito de Horário (RF03) - Tenta marcar 09h00 (Mesmo horário do ID 101)
    tentar_agendar(paciente_id=104, data_hora=datetime(2026, 4, 25, 9, 0))   

    # 4. Exibindo o estado final do Repositório
    print("=== AGENDA FINAL NO REPOSITÓRIO ===")
    consultas_salvas = repo.buscar_todos()
    
    if not consultas_salvas:
        print("Nenhuma consulta agendada.")
    else:
        for consulta in consultas_salvas:
            print(f"📅 Início: {consulta.inicio.strftime('%H:%M')} | Fim: {consulta.fim.strftime('%H:%M')} | Paciente: {consulta.paciente_id}")

if __name__ == "__main__":
    simular_dia_na_clinica()