# Projet Universitaire

Créer un service permettant d'écouter en diffusion progressive (streaming) des fichiers musicaux. Le client pourra choisir ces morceaux grâce à moteur de recherche qui indexera les métadonnées contenues dans les fichiers musicaux.

----
## Etapes

- Installation sous Mac :

```
brew install exempi
brew install libxmp
sudo pip install python-xmp-toolkit
sudo pip install rdflib
```

- Lancer le projet :

```
cd streaming/
python server_web.py
```

puis dans un autre terminal lancer :

```
python server.py URL_VERS_CE_PROJET
```

Le site permettant d'effectuer la recherche est alors disponible [http://127.0.0.1:5000](http://127.0.0.1:5000)