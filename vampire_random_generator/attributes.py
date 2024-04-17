import copy
attributes_all = {
    'Strength': 0,
    'Dexterity': 0,
    'Stamina': 0,
    'Charisma': 0,
    'Manipulation': 0,
    'Composure': 0,
    'Intelligence': 0, 
    'Wits': 0,
    'Resolve': 0,
}

def initialize_attributes_values():
    return [4, 3, 3, 3, 2, 2, 2, 2, 1]

available_attributes_value = initialize_attributes_values()

# Função para reinicializar a lista de valores de atributos
def reset_attributes_values():
    global available_attributes_value
    available_attributes_value = initialize_attributes_values()