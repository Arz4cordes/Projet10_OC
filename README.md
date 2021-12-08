# PROJET10_OC
API construite avec Django Rest Framework, permettant le suivi de problèmes
rencontrés lors de projets sur trois plateformes (site web, application iOS, application Android)

1) Pour télécharger l'application, voici le lien GitHub:
    https://github.com/Arz4cordes/Projet10_OC
2) Pour utiliser les programmes, installer un environnement virtuel Python,
    par exemple avec la commande python -m venv envp10 sous windows.
3) Le fichier requirements.txt contient les bibliothèques à installer:
    utiliser par exemple la commande python -m pip install -r requirements.txt
    pour installer les bibliothèques utilisées dans l'application.
3) Une fois Django installé, vous pouvez faire les migrations avec les    
    commandes suivantes depuis le dossier source Project10:
    python manage.py makemigrations
    python manage.py migrate
    Cela mettra en place les tables de la base de donnée SQLLite.
5) Depuis le dossier source Project10, écrire la commande
    python manage.py runserver pour lancer le serveur
6) L'API peut être utilisée avec le logiciel Postman.
    La documentation concernant l'application et les différents endpoints
    est publiée à cette adresse: https://documenter.getpostman.com/view/14708629/UVC6j7Tw
7) Pour utiliser l'application, un utilisateur doit d'abord aller sur l'endpoint
    http://127.0.0.1:8000/signup/ afin de créer un compte utilisateur
8) Une fois qu'un compte utilisateur est crée, l'utilisateur peut se connecter
    à l'application en allant sur l'endpoint http://127.0.0.1:8000/login/
    En réponse, l'utilisateur qui s'est authentifié recevra un Token d'accès.
    Ce Token est valable 5 minutes et il doit être recopié dans la partie "Authorization"
    pour chacune des requètes effectuées par la suite.
9) Quand le Token d'accès n'est plus valide, l'utilisateur doit à nouveau se connecter
    en allant sur l'endpoint  http://127.0.0.1:8000/login/ pour récupérer un nouveau Token d'accès,
    qu'il faudra copier pour l'utiliser par la suite dans les nouvelles requètes.
10) Tout utilisateur authentifié peut créer un nouveau projet en allant sur l'endpoint
    http://127.0.0.1:8000/projects/ (en POST)
    Il pourra ajouter des contributeurs au projet via l'endpoint http://127.0.0.1:8000/projects/ID/users/
    où ID est le numéro du projet.
    Seul l'auteur d'un projet peut le mettre à jour ou le supprimer.
    Les projets dont un utilisateur est contributeur sont visibles via l'endpoint
    http://127.0.0.1:8000/projects/ (en GET)
11) Les autres endpoints sont détaillés dans la documentation visible à l'adresse
    https://documenter.getpostman.com/view/14708629/UVC6j7Tw
12) Rappel: seuls les auteurs d'une issue peuvent la mettre à jour ou la supprimer.
    De même seuls les auteurs d'un comment peuvent le mettre à jour ou le supprimer.
