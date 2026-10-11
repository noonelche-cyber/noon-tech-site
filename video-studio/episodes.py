"""Short series "L'insulte du jour pour survivre en Espagne" — aimed at foreigners living in Spain.
Each episode: [hook, §spanish word, literal, meaning, context, cta]. '§' = spoken by the Spanish voice."""

EPISODES = {
    'fr': [
        dict(n=1, emo='🥛', lines=["Tu vis en Espagne ? Tu vas l'entendre :", "§¡Me cago en la leche!", "Littéralement : je chie dans le lait.",
                                    "En vrai : putain !", "Quand tu rates le dernier bus.", "Deviens bêta-testeur : l'appli ¡Joder! est gratuite pour les 30 premiers. Écris-moi !"]),
        dict(n=2, emo='🐐', lines=["Tu vis en Espagne ? Tu vas l'entendre :", "§¡Estás como una cabra!", "Littéralement : t'es comme une chèvre.",
                                    "En vrai : t'es complètement fou !", "Ton coloc qui fait du karaoké à trois heures du matin.", "Deviens bêta-testeur : l'appli ¡Joder! est gratuite pour les 30 premiers. Écris-moi !"]),
        dict(n=3, emo='🐐', lines=["Tu vis en Espagne ? Tu vas l'entendre :", "§¡Qué cabrón!", "Littéralement : quel bouc !",
                                    "En vrai : quel salaud… ou quel génie.", "Tout dépend du ton.", "Deviens bêta-testeur : l'appli ¡Joder! est gratuite pour les 30 premiers. Écris-moi !"]),
        dict(n=4, emo='🙄', lines=["Tu vis en Espagne ? Tu vas l'entendre :", '§¡Que te den!', "Littéralement : qu'on te donne !",
                                    'En vrai : va te faire voir !', 'Quand ton voisin se gare devant ton garage.', "Deviens bêta-testeur : l'appli ¡Joder! est gratuite pour les 30 premiers. Écris-moi !"]),
        dict(n=5, emo='😮', lines=["Tu vis en Espagne ? Tu vas l'entendre :", '§¡Hostia!', 'Littéralement : hostie !',
                                    'En vrai : putain… ou waouh !', 'Pour la colère, la surprise, et même la joie.', "Deviens bêta-testeur : l'appli ¡Joder! est gratuite pour les 30 premiers. Écris-moi !"]),
        dict(n=6, emo='🙄', lines=["Tu vis en Espagne ? Tu vas l'entendre :", '§¡Eres un tocapelotas!', "Littéralement : t'es un touche-couilles.",
                                    "En vrai : t'es un casse-pieds !", 'Le collègue qui envoie des mails le dimanche.', "Deviens bêta-testeur : l'appli ¡Joder! est gratuite pour les 30 premiers. Écris-moi !"]),
        dict(n=7, emo='🥛', lines=["Tu vis en Espagne ? Tu vas l'entendre :", '§¡Qué mala leche!', 'Littéralement : quel mauvais lait !',
                                    'En vrai : quel sale caractère !', 'Ton propriétaire qui garde la caution.', "Deviens bêta-testeur : l'appli ¡Joder! est gratuite pour les 30 premiers. Écris-moi !"]),
        dict(n=8, emo='😤', lines=["Tu vis en Espagne ? Tu vas l'entendre :", '§¡Qué cara tienes!', 'Littéralement : quel visage tu as !',
                                    "En vrai : t'es gonflé !", 'Celui qui double toute la file à la boulangerie.', "Deviens bêta-testeur : l'appli ¡Joder! est gratuite pour les 30 premiers. Écris-moi !"]),
        dict(n=9, emo='🥒', lines=["Tu vis en Espagne ? Tu vas l'entendre :", '§¡Me importa un pepino!', "Littéralement : ça m'importe un concombre.",
                                    "En vrai : je m'en fiche complètement.", 'Quand ton ex donne des nouvelles.', "Deviens bêta-testeur : l'appli ¡Joder! est gratuite pour les 30 premiers. Écris-moi !"]),
        dict(n=10, emo='🍺', lines=["Tu vis en Espagne ? Tu vas l'entendre :", '§¡Ni de coña!', 'Littéralement : même pas pour rire !',
                                    'En vrai : hors de question !', 'Payer huit euros une bière à Madrid ?', "Deviens bêta-testeur : l'appli ¡Joder! est gratuite pour les 30 premiers. Écris-moi !"]),
    ],
    'en': [
        dict(n=1, emo='🥛', lines=["Living in Spain? You'll hear this:", "§¡Me cago en la leche!", "Literally: I crap in the milk.",
                                    "Meaning: damn it!", "When you miss the last bus.", "Become a beta tester: the ¡Joder! app is free for the first 30. DM me!"]),
        dict(n=2, emo='🐐', lines=["Living in Spain? You'll hear this:", "§¡Estás como una cabra!", "Literally: you're like a goat.",
                                    "Meaning: you're totally crazy!", "Your flatmate doing karaoke at 3 a.m.", "Become a beta tester: the ¡Joder! app is free for the first 30. DM me!"]),
        dict(n=3, emo='🐐', lines=["Living in Spain? You'll hear this:", "§¡Qué cabrón!", "Literally: what a billy goat!",
                                    "Meaning: what a bastard… or what a genius.", "It all depends on the tone.", "Become a beta tester: the ¡Joder! app is free for the first 30. DM me!"]),
    ],
}
SERIES = {'fr': "L'INSULTE DU JOUR", 'en': 'SPANISH INSULT OF THE DAY'}
SUB = {'fr': 'pour survivre en Espagne', 'en': 'to survive in Spain'}
END = {'fr': ['DEVIENS BÊTA-TESTEUR', 'Appli complète gratuite · 30 places', 'Écris-moi en DM'],
       'en': ['BECOME A BETA TESTER', 'Full app free · 30 spots', 'DM me']}
LOCALE = {'fr': 'fr-FR', 'en': 'en-US'}
