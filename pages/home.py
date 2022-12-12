import dash
from dash import html
import base64

dash.register_page(__name__, path='/')

Introduction_text = [
    "Nous avions comme projet de réaliser des graphiques basés sur des fichiers json contenant différentes données correspondantes à des articles. ",
     html.Br(), 
     "Nous avons décidé de réaliser un Dashboard de plusieurs pages. Par ailleurs, nous l’avons rendu interactif afin de mieux visualiser les données ainsi qu’en visualiser le plus possible."
     ]

Countries_text = [
    "Ce tableau de bord est centré sur l'analyse des pays. En effet, nous plaçons sur une carte du monde, un marqueur représentant le nombre de fois où ce pays a été cité dans les articles du fichier sélectionné.", 
    html.Br(), 
    "Lorsque nous cliquons sur celui-ci, nous affichons un graphique en barres permettant de visualiser les 5 dates où ce pays a été cité le plus de fois pour un article ( 5 dates maximum). En cliquant sur une barre, nous allons afficher le titre ainsi que la description de l’article en question.", 
    html.Br(), 
    "Nous pouvons donc, à travers ce dashboard, émettre des hypothèses sur des évènements qui se sont passés. Par exemple, si un pays est cité beaucoup de fois dans un article, nous verrons la description de ce dernier.",
    html.Br(), 
    "A noter que ce dashboard peut prendre un certain temps avant de s’afficher dû au nombre important d’informations à traitées (15/20 secondes pour le plus petit fichier)."
    ]

Keywords_text = [
    "Ce tableau de bord est focalisé sur les mots clés. Abordons d’abord le graphique principal. Nous pouvons choisir une année pour cibler des périodes précises. Ce premier graphe est un graphique en barres représentant le nombre d’articles par jour.",
    html.Br(),
    "Lorsque l’on clique sur une barre, nous obtenons deux graphiques supplémentaires. Un premier qui est également un graphique en barres représentant les 5 mots clés les plus utilisés à cette date. Puis un deuxième graphique en lignes (line chart). Celui-ci représente le nombre de fois que les mots clés ont été utilisé lors de cette même année. Cela permet de se rendre compte si c’est un mot clé utilisé fréquemment ou non. Nous pouvons alors émettre des hypothèses quant aux évènements qui ont engendrés cela. Par exemple, pour le 8/10/2020 (avec le fichier 'mali de fdesouche' ), nous obtenons des mots clés tels que « Mali », « otage », « Sophie » et « libération » et en analysant le graphique en lignes, nous pouvons conclure que Sophie a été libéré ce jour là.",
    html.Br(),
    "En outre, nous pouvons isoler un mot clé sur le deuxième graphique en cliquant sur la barre correspondant à celui-ci, ce qui permet d’observer plus facilement son évolution au cours de l’année.",
    ]

Organizations_text = [
    "Ce tableau de bord porte sur l'analyse des différentes organisations citées dans les articles de chaque fichier. Le premier graphique est un graphique en barre animé permettant de visualiser pour les organisations les plus citées, le nombre de fois qu’une de ces organisations est présente. Ceci est effectué pour chaque mois de chaque année.",
    html.Br(),
    "Il est par ailleurs possible de cliquer sur une barre de ce graphique pour afficher de nouveaux résultats sur les deux autres. Un diagramme circulaire ainsi qu'un tableau s'affichent alors, le premier affiche les organisations les plus citées en même temps que l'organisation sélectionnée (10 organisations maximum). Ce graphique nous permet, par exemple d'observer que les groupes de l'état islamique sont la plupart du temps cités les uns avec les autres et représentent la plupart du temps à eux seul 50% des organisations présentent lorsque l'une d'elles est citée.",
    html.Br(),
    "Le tableau quant à lui, affiche une description de l'organisation afin de pouvoir se renseigner rapidement sur celle-ci."
]

Conclusion_text = [
    "A travers ce projet, nous avons appris à créer nos propres Dashboard. Cela est très important pour nous puisque nous serons menés à manipuler des données.",
    html.Br(),
    "Nous pouvons alors nous rendre compte de l'importance des graphiques pour visualiser les données.",
    html.Br(),
    "Enfin, voici un schéma de notre application avec les différentes pages ainsi que les callback.",
    ]

schema = './schema.png'
schema_base64 = base64.b64encode(open(schema, 'rb').read()).decode('ascii')

layout = html.Div(children=[

    html.Div(children=[
        
        html.H1(children='Introduction :'), 

        html.Div([
            i for i in Introduction_text
        ]),
        html.Br()
    ]),
    html.Div(children=[
        
        html.H1(children='Présentation de la page Countries-Analysis :'), 

        html.Div([
            i for i in Countries_text
        ]),
        html.Br()
    ]),
    html.Div(children=[
        
        html.H1(children='Présentation de la page Keywords-Analysis :'), 

        html.Div([
            i for i in Keywords_text
        ]),
        html.Br()
    ]),
     html.Div(children=[
        
        html.H1(children='Présentation de la page Organizations-Analysis :'), 

        html.Div([
            i for i in Organizations_text
        ]),
        html.Br()
    ]),
    html.Div(children=[
        
        html.H1(children='Conclusion :'), 

        html.Div([
            i for i in Conclusion_text
        ]),
        html.Br(),

        html.Img(src='data:image/png;base64,{}'.format(schema_base64)),
    ]),
])