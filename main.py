
import Filters as filters
import BassonFilter as bassonFilter

# Mettre les parametres boolean a True pour voir les graphiques,
# un a la fois, sinon le premier empeche la generation des graphiques du prochain

if __name__ == '__main__':
    # Extraction des parametres de la note de guitare et construction d'une chanson avec les sons synthetique
    filters.extractionParametres(False)

    # Filtrage de la note de basson
    bassonFilter.filtrageBasson(False)

    exit(1)
