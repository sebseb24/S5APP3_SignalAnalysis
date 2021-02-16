
import Filters as filters
import BassonFilter as bassonFilter

# En mettant les parametres boolean a true, on active l'affichage des graphiques
# L'affichage des graphique est bloquant, donc si la premiere fonction affiche ses graphiques,
# la deuxieme fonction ne s'execute pas

if __name__ == '__main__':
    # Extraction des parametres de la note de guitare et construction d'une chanson avec les sons synthetique
    filters.extractionParametres(False)

    # Filtrage de la note de basson
    bassonFilter.filtrageBasson(False)

    exit(1)
