"""Short series "L'insulte du jour pour survivre en Espagne" — aimed at foreigners living in Spain.
Each episode: [hook, §spanish word, literal, meaning, context, cta]. '§' = spoken by the Spanish voice."""

EPISODES = {
    'fr': [
        dict(n=1, emo='🥛', lines=["Tu vis en Espagne ? Tu vas l'entendre :", "§¡Me cago en la leche!", "Littéralement : je chie dans le lait.",
                                    "En vrai : putain !", "Quand tu rates le dernier bus.", "La suite dans l'appli ¡Joder! : écris-moi."]),
        dict(n=2, emo='🐐', lines=["Tu vis en Espagne ? Tu vas l'entendre :", "§¡Estás como una cabra!", "Littéralement : t'es comme une chèvre.",
                                    "En vrai : t'es complètement fou !", "Ton coloc qui fait du karaoké à trois heures du matin.", "La suite dans l'appli ¡Joder! : écris-moi."]),
        dict(n=3, emo='🐐', lines=["Tu vis en Espagne ? Tu vas l'entendre :", "§¡Qué cabrón!", "Littéralement : quel bouc !",
                                    "En vrai : quel salaud… ou quel génie.", "Tout dépend du ton.", "La suite dans l'appli ¡Joder! : écris-moi."]),
    ],
    'en': [
        dict(n=1, emo='🥛', lines=["Living in Spain? You'll hear this:", "§¡Me cago en la leche!", "Literally: I crap in the milk.",
                                    "Meaning: damn it!", "When you miss the last bus.", "More in the ¡Joder! app: DM me."]),
        dict(n=2, emo='🐐', lines=["Living in Spain? You'll hear this:", "§¡Estás como una cabra!", "Literally: you're like a goat.",
                                    "Meaning: you're totally crazy!", "Your flatmate doing karaoke at 3 a.m.", "More in the ¡Joder! app: DM me."]),
        dict(n=3, emo='🐐', lines=["Living in Spain? You'll hear this:", "§¡Qué cabrón!", "Literally: what a billy goat!",
                                    "Meaning: what a bastard… or what a genius.", "It all depends on the tone.", "More in the ¡Joder! app: DM me."]),
    ],
}
SERIES = {'fr': "L'INSULTE DU JOUR", 'en': 'SPANISH INSULT OF THE DAY'}
SUB = {'fr': 'pour survivre en Espagne', 'en': 'to survive in Spain'}
LOCALE = {'fr': 'fr-FR', 'en': 'en-US'}
