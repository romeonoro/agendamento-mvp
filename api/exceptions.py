class ForaDoHorarioError(Exception):
    """Lançada quando a consulta está fora do turno de trabalho do médico."""
    pass

class ConflitoHorarioError(Exception):
    """Lançada quando já existe uma consulta no mesmo horário."""
    pass