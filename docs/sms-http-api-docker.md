# Guide Docker de l'API HTTP SMS

Ce guide explique comment construire l'image Docker pour l'exemple d'API HTTP SMS, lancer le conteneur et envoyer votre premier SMS.

## Construire l'image

```bash
docker build -t sms-api .
```

Cette commande crée une image contenant le serveur API issu de `examples/sms_http_api.py`.

## Exécuter le conteneur

Définissez les variables d'environnement pour la connexion au modem et démarrez le conteneur :

```bash
docker run -d --network host \
  -e MODEM_URL="http://192.168.8.1/" \
  -e USERNAME=admin \
  -e PASSWORD=YOUR_PASSWORD \
  -e SMS_API_DB=/data/sms_api.db \
  sms-api
```

`MODEM_URL` est obligatoire et doit pointer vers votre modem Huawei. `USERNAME` et `PASSWORD` fournissent les identifiants de connexion. L'option `--network host` permet au conteneur d'accéder au modem à `192.168.8.1`. Vous pouvez éventuellement définir `HOST` et `PORT` pour changer l'adresse d'écoute (par défaut `0.0.0.0:80`).
`SMS_API_DB` définit le chemin de la base SQLite utilisée pour stocker les journaux des requêtes.

Le serveur API est alors accessible sur l'hôte au port choisi.

L'API propose également un endpoint `/health` pour vérifier l'état du modem et
afficher plusieurs informations issues des exemples `device_info.py` et
`device_signal.py` :

```bash
curl http://localhost:80/health
```


## Envoyer votre premier SMS

Préparez la charge JSON (destinataire, expéditeur et message) puis utilisez `curl` pour appeler l'API :

```bash
curl -X POST http://localhost:80/sms \
  -H "Content-Type: application/json" \
  -d '{"to": ["+420123456789"], "from": "+420987654321", "text": "Hello from the API!"}'
```

Si la requête réussit, le serveur répond `OK`.

## Utilisation alternative

Vous pouvez aussi exécuter l'API directement hors de Docker avec :

```bash
python examples/sms_http_api.py http://192.168.8.1/ --username admin --password YOUR_PASSWORD
```

Consultez la docstring du script pour les options supplémentaires.
