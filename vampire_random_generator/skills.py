skills_all = {
    'Athletics': 0,
    'Brawl': 0,
    'Craft': 0,
    'Driving': 0,
    'Firearms': 0,
    'Larceny': 0,
    'Meleee': 0,
    'Stealth': 0,
    'Survival': 0,
    'Animal Ken': 0,
    'Etiquette': 0,
    'Insight': 0,
    'Intimidation': 0,
    'Leadership': 0,
    'Performance': 0,
    'Persuasion': 0,
    'Streetwise': 0,
    'Subterfuge': 0,
    'Academics': 0,
    'Awareness': 0,
    'Finance': 0,
    'Investigation': 0,
    'Medicine': 0,
    'Occult': 0,
    'Politics': 0,
    'Science': 0,
    'Technology': 0,
}

def initialize_skill_values():
    return {
        "Jack of All Trades": [3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,0],
        "Balanced": [3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0],
        "Specialist": [4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0],
    }

available_skill_value = initialize_skill_values()

# Função para reinicializar a lista de valores de atributos
def reset_skill_values():
    global available_skill_value
    available_skill_value = initialize_skill_values()