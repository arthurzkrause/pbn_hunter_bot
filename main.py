import random, copy
from typing import Final
from typing import List
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from tokentoken.token_username import TOKEN,BOT_USERNAME
from vampire_random_generator.texts import perks_and_edges_text
from vampire_random_generator.eater_eggs import controle_updates, ambitions

TOKEN
BOT_USERNAME

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello and welcome to the World of Darkness!\n- This is a bot from POA by Night, an encyclopedia project where you can find out more about the RPG world created for the WoD system for Porto Alegre, Rio Grande do Sul, Brazil. For more information, visit our networks: https://linktr.ee/poabynight\n\n'
'What you can do:\n'
'- Play dice with the command /h5\n'
'- Make a random character with /character_generator.\n'
'- Get information about Creed, Drives, Edges and Perks by writing their names in the conversation.\n'
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'COMMANDS:\n'
        '- /h5 X Y (X = Total Dice Pool | Y = Total Desperation Dice)\n'
        '- /character_generator: Generates a random character with Skills, Attributes and Disciplines.\n'
        '- Get information about Creed, Drives, Edges and Perks by writing their names in the conversation.\n'
        '- /updates show what and when something was introduced\n'
	    '- You can type UPPER or lower case.\n\n'
         'Most of the content comes directly from the official Wiki!'
         'Do you want to send any update ideas?\n'
         'https://www.instagram.com/poabynight\n'
        )

async def character_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    import copy
    from vampire_random_generator.attributes import attributes_all, available_attributes_value, reset_attributes_values
    from vampire_random_generator.skills import skills_all, available_skill_value, reset_skill_values
    from vampire_random_generator.name_generator.surname import surname_list
    from vampire_random_generator.name_generator.own_name import name_list

    #OBS: Tentei fazer com que o bot fornecesse um personagem aleatório de um clã específico mudando só a variável "clan" ao ser digitado "/character_generator ventrue". Não consegui e deixo isso pro meu eu do futuro.

    # NAME GENERATOR
    def name_surname_age():
        age = random.randint(18, 60)

        name_generated = random.choice(name_list)

        first_surname_generated = random.choice(surname_list)
        second_surname_generated = random.choice(surname_list)

        return f"Name:\n{name_generated} {first_surname_generated} {second_surname_generated}\nAge: {age}\n"


    # ATTRIBUTES GENERATOR
    def attributes_generator():
        reset_attributes_values()
        result = "\nATTRIBUTES\n"
        for attribute in attributes_all:
            if available_attributes_value:
                assigned_value = random.choice(available_attributes_value)
                attributes_all[attribute] = assigned_value
                available_attributes_value.remove(assigned_value)
                result += f"{attribute}: {assigned_value}\n"
            else:
                result += f"{attribute}: No options available\n"

        return result

    # SKILLS GENERATOR - usa quase tudo que tá em vampir_random_generator.other_stats
    def skill_generator(category):
        reset_skill_values()
        result = f"\nSKILLS:\nType: {category}\n"
        values = available_skill_value.get(category, [])

        for atributo in skills_all:
            if values:
                assigned_value = random.choice(values)
                skills_all[atributo] = assigned_value
                values.remove(assigned_value)
                result += f"{atributo}: {assigned_value}\n"
            else:
                result += f"{atributo}: No options available\n"
        
        return result

    # Choose the desired category
    chosen_category = random.choice(list(available_skill_value.keys()))
    creed_choice = random.choice(["Entrepreneurial", "Faithful", "Inquisitive", "Martial", "Underground"])
    drive_choice = random.choice(["Curiousity", "Vengeance", "Oath", "Greed", "Pride", "Envy"])
    ambition = random.choice(ambitions)

    # RUN
    hunter_generated = f'{name_surname_age()}{attributes_generator()}{skill_generator(chosen_category)}\nCreed: {creed_choice}\nDrive: {drive_choice}\nAmbition: {ambition}'

    await update.message.reply_text(hunter_generated)

#DADOS
async def h5_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Divide o texto em partes usando espaços como delimitador
    args = text.split()

    # Verifica se há pelo menos dois argumentos
    if len(args) == 3 and args[1].isdigit() and args[2].isdigit():
        # Converte os argumentos para inteiros
        total_de_dados = int(args[1])
        dado_de_fome = int(args[2])

        # Verifica se os números são diferentes de zero -------------------------OK
        if total_de_dados > 20:
            await update.message.reply_text("Dice limit is 20 dice per roll.")
            return
        elif total_de_dados == 0 and dado_de_fome == 0:
            await update.message.reply_text("Why are you going to roll zero dice?")
            return
        elif total_de_dados == 0:
            await update.message.reply_text("What do you mean? The total number of dice is 0 and you still want to roll something?")
            return
        # Verifica se o dado de fome é zero ------------------------OK
        elif dado_de_fome == 0:
            # Se sim, rola o segundo número sem interferências
            result_dado_de_fome = 0
            result_total_de_dados = roll_dice(total_de_dados)
            sorted_total_de_dados = sort_dice_results(result_total_de_dados)
            ten_critic= double_ten_successes(sorted_total_de_dados)
            successes_dices = sum(1 for roll in result_total_de_dados if int(roll) >= 6)+ten_critic
            
            response_message = f"Dices: {', '.join(map(str, sorted_total_de_dados))}\nDesperation Dices: 0\n{successes_dices} successes\n"
        # Verifica se o DADO DE FOME é maior que o TOTAL DE DADOS  ------------------- ok
        elif dado_de_fome >= total_de_dados:
            # Se sim, rola o segundo número sem interferências
            result_total_de_dados = 0
            result_dado_de_fome = roll_dice(total_de_dados)
            sorted_dados_de_fome = sort_dice_results(result_dado_de_fome)
            ten_critic = double_ten_successes(sorted_dados_de_fome)
            successes_dices = sum(1 for roll in result_dado_de_fome if int(roll) >= 6)+ten_critic
            bestial = check_for_double_ten(sorted_dados_de_fome)

            response_message = f"Dices: 0\nDesperation Dices: {', '.join(map(str, sorted_dados_de_fome))}\n{successes_dices} successes\n{bestial}"
        else:
            # Se não, rola o primeiro número e pega os últimos num_dice2 resultados
            # TOTAL DE DADOS
            result_total_de_dados = roll_dice(total_de_dados)
            #COPIA total de dados e ORDENA para análise futura
            result_total_de_dados_copy = copy.deepcopy(result_total_de_dados)
            sorted_result_total_de_dados_copy = sorted(result_total_de_dados_copy, reverse=True)
            # DADOS DE FOME
            result_dado_de_fome = result_total_de_dados[-dado_de_fome:]
            sorted_dados_de_fome = sort_dice_results(result_dado_de_fome)
            # Atualiza a variável total_de_dados, removendo os dados de fome e ordena
            result_total_de_dados = result_total_de_dados[:-dado_de_fome]
            sorted_total_de_dados = sort_dice_results(result_total_de_dados)
            #Análise
            ten_critic = double_ten_successes(sorted_result_total_de_dados_copy)
            successes_dices = sum(1 for roll in sorted_result_total_de_dados_copy if int(roll) >= 6) + ten_critic
            
            # Verifica se há crítico bestial
            bestial = ""
            if 10 in sorted_total_de_dados and 10 in sorted_dados_de_fome:
                bestial = "Messy Critical!"
            elif 1 in sorted_total_de_dados and 1 in sorted_dados_de_fome:
                bestial = "Bestial Failure!"

            response_message = f"Dices: {', '.join(map(str, sorted_total_de_dados))}\nDesperation Dices: {', '.join(map(str, sorted_dados_de_fome))}\n{successes_dices} successes\n{bestial}"

            
        await update.message.reply_text(response_message)

    else:
        # Mensagem de erro se os argumentos não forem válidos
        response_message = f"Do you want to roll the dice?\nPlay in the format '/h5 4 1'!\n\nIn the example:\n4 is the Total Dices\n1 is the Total Desperation Dices!\n\nThe result will appear as:\nTotal dice pool: result.\nDesperation Dices: result."

        # Responde ao usuário com mensagem de erro
        await update.message.reply_text(response_message)

def double_ten_successes(how_many_tens):
    #confere dupla de 10 e soma no resultado, já que dois 10 são 4 pontos de sucesso.
    ten_successes = 0
    i = 0  # Inicializamos o índice fora do loop para evitar IndexError
    while i < len(how_many_tens) - 1:
        if int(how_many_tens[i]) == 10 and int(how_many_tens[i + 1]) == 10:
            ten_successes += 2
            i += 2  # Pular para a próxima possível dupla de 10
        else:
            i += 1  # Mover para o próximo elemento na lista
    return ten_successes

def check_for_double_ten(dados):
    #confere se há dois 10 ou 1 na rolagem e
    for i in range(len(dados) - 1):
        if int(dados[i]) == 10 and int(dados[i + 1]) == 10:
            return critico_falha_bestial(dados)
        elif int(dados[i]) == 1 and int(dados[i + 1]) == 1:
            return critico_falha_bestial(dados)
    return ''

def critico_falha_bestial(critic_list):
    #imprime mensagem de crítico
    if 10 in critic_list and 10 in critic_list:
        crit_message = "Messy Critical"
    elif 1 in critic_list and 1 in critic_list:
        crit_message = "Bestial Failure!\n"
    return crit_message
    
def roll_dice(num_dice):
    # Realiza a rolagem de dados de 10 lados
    results = [random.randint(1, 10) for _ in range(num_dice)]

    return results

def sort_dice_results(results_list):
    # Ordena a lista em ordem decrescente - Acho que isso não é necessário, mas é aquilo, já tá feito
    results_sorted = sorted(results_list, reverse=True)

    return results_sorted

async def desperation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Desperation represents the state of urgency and anxiety of a cell and dictates the amount of Desperation Dice that each Hunter can add to their pool by tapping into their Drive when performing actions related to their Edge. The higher a cell's Desperation is, the greater the strength of the Hunter's Drives. Desperation increases at the end of a major scene when things do not go in the cell's favor, and when the fate of the Hunters, their quarry, or innocents is on the line.\n\nExamples of Desperation increasing\n- One or more of the Hunters is seriously wounded or killed.\n- Even with the effort of the cell, the quarry has escaped or advanced its goals.\n- The quarry manages to kill innocents due to a misstep or failure to protect the cell.\n\nExamples of Desperation decreasing\n- The Hunters manage to gain crucial information about their quarry without any issue.\n- Innocents were protected by the cell while accomplishing another goal.\n- The quarry is seriously harmed or otherwise majorly impacted by the cell.\n\nDesperation Dice\n- Overreach: For each '1' on the Desperation Dice, increase Danger by 1. The Hunter has somehow revealed themselves and their cell to their quarry in a method related to their Drive. While the test is still a win, the long-term consequences could prove disastrous for the entire cell.\n- Despair: The test has failed, no matter the number of successes. The Hunter enters a state of Despair, which renders their Drive useless, and they are unable to call upon it to use Desperation Dice until they've redeemed themselves. Each Drive has a unique condition for redemption and can be treated as a group effort instead of being accomplished by an individual.")

#Dice rolls, inform the Narrator about some mechanics
async def dice_rolls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Automatic Wins\nPlayer's dice pool is double the challenge\n\nWinning at a cost\nRoll that includes successes, but fails. You may achieve your goal, but at some cost.\n\nTake Half\nDivide your total dice in half (round down). This will be your number of successes.\n\nMultiple opponents\nLose one die for each successive action in the same turn.\n\nExtended test\nCan be used between characters\nHigh difficulty test with cumulative rolls.\nE.g Getting your hands on a relic requires three wins for each task:\nInt + Larceny - overcome alarm \nDex + Stealth - Invade location through skylight\nComposure + Stealth - Extract relic from security laser\n\nSingle roll\nIf after 3 turns of combat and the question 'Will anything dramatically change with more interactions?' if not:\n- Difficulty 3 if the players won the last turn.\n- Difficulty 4 if they suffered the same as the npc\n- Difficulty 5 if the NPC won the last turn\n- Difficulty 6 if the players were lucky to be alive.\n\nManeuver\nThe character studies the opponent and moves to a place of advantage, or a critical point. Bonus of 1-3 dice.\n\nTotal Attack\n+1 damage, but cannot defend any attack. If it is a Ranged Weapon, discharge the weapon. (Even if the NPC has more successes, he will still take all the damage.)\n\nTotal Defense\nCharacter just wants to survive. Gains a bonus die on all defense rolls. If you are in good cover, if become immune to ranged attacks, as long as you are not flanked (maneuver). Can only perform minor actions.")

async def edges_and_perks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type the Edge to know more. Perks are listed with assets, just type the name:\n\nAssets:\n- Arsenal\n- Fleet\n- Ordnance\n- Library\n\nAptitudes:\n- Improvised Gear\n- Global Access\n- Drone Jockey\n- Beast Whisperer\n\nEndowments\n- Sense the Unnatural\n- Repel the Unnatural\n- Thwart the Unnatural\n- Artifact")

#Resonance, inform about the mecanic of resonances
async def creed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Creed is how Hunters approach their quarry - their modus operandi, tools they use during the Hunt, as well as their general outlook and social component. Hunters can find common ground with others of the same creed, although individual outlooks may still vary depending on their Drive and other factors. Most Hunters realize they have little choice but to work together, as it's them against the creatures of the night, other orgs, and a world unwilling to acknowledge the monsters.\n\nEntrepreneurial\n- Hunters take on their quarry through bold and experimental innovations.\n\nFaithful\n-Hunters operate with and through the belief in higher powers\n\nInquisitive\n- Hunters gather knowledge and use it against their quarries, using both modern cutting-edge and ancient methods to study the monsters and what they do\n\nMartial\n- Hunters devote themselves to arms and tactics to take down supernatural threats\n\nUnderground\n- Hunters use guile, subterfuge, and knowing the right people get them access to their quarry.")

#predator_type_roll inform the rolls to hunt
async def drives(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Drives motivate how Hunters act against the supernatural, and while they may complement their Creed, they don't have to. At character creation, each Hunter is given one Drive which has an influence on the character's outlook. It can suggest characterizations for the character, but it also decides certain consequences when using Desperation Dice.\n\nCuriousity\n- The Hunter is motivated to discover everything about the quarry; learning about their target motivates them to dig deeper for each new fact.\n- Redemption: The cell learns new information about their quarry.\n\nVengeance\n- The Hunter must balance the scale for the harm done to themselves or someone close to them by the supernatural.\n- Redemption: The cell must directly or indirectly harm their quarry (or a creature similar).\n\nOath\n- The Hunter's words are their bond, and they must fulfill the pledge they made against the creatures of the night, stopping at nothing to achieve this.\n- Redemption: The cell must aid the Hunter to either uphold their pledge or bring it closer to completion.\n\nGreed\n- The Hunter wants what the supernatural creatures have, believing it unfair that they profit from their monstrosities.\n- Redemption: Obtaining resources from the quarry or a creature like it.\n\nPride\n- The Hunter has a burning desire to prove themselves against supernatural creatures given powers that they've never deserved. Whether it represents the unbreakable human spirit or an overly competitive nature, the Hunter will take any chance to overcome their quarry.\n- Redemption: Directly or indirectly beating the quarry at some type of challenge.\n\nEnvy\n- The Hunter wants to join the supernatural or die trying.\n- Redemption: Either obtain samples of the source of the quarry's power or win their favor.\n\nAtonement\n- The Hunter helped a monster in the past, knowingly or unknowingly, and now seeks restitution. They are aware that their acts have injured innocent people and are willing to put themselves in danger to repay this debt.\n- Redemption: The cell must defend someone, directly or indirectly, from the quarry (or a similar creature) by putting themselves in danger and taking the hit for them. Alternately, the Hunter can atone for their transgression by helping a cellie.")

#Updates - controle de atualizações - vampire_random_generator / easter_eggs
async def updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultado_formatado = "\n".join(controle_updates) 
    await update.message.reply_text(resultado_formatado)

#Handle Responses - se o usuário digitar algo que não um comando,o bot devolve algo escrito
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if processed in perks_and_edges_text:
        return f'{processed.upper()}\n{perks_and_edges_text[processed]}'
    else:
        return "Type the name of the Perk or Edge you are interested in! There are some other surprises out there, don't give up!"    
  
#Handling Messages - Diferencia se é grupo ou não.
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str=update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response:str=handle_response(new_text)
        else:
            return
    else:
        response: str=handle_response(text)
    print('Bot', response)
    await update.message.reply_text(response)

#Errors - imprimir no terminal pra eu saber o que tá acontecendo
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}'),

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('h5',h5_command))
    app.add_handler(CommandHandler('character_generator',character_generator))
    app.add_handler(CommandHandler('updates',updates))
    app.add_handler(CommandHandler('dice_rolls',dice_rolls))
    app.add_handler(CommandHandler('edges_and_perks',edges_and_perks))
    app.add_handler(CommandHandler('desperation',desperation))
    app.add_handler(CommandHandler('creed',creed))
    app.add_handler(CommandHandler('drives',drives))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    #Errors
    app.add_error_handler(error)
    
    #Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)