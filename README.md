[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JhennerTigreros/zero_to_production/blob/master/00/model.ipynb)

# Configuración

Primeramente descargaremos la herramienta de linea de comandos para el manejo de recursos la manera más facil de instalar esta herramienta es seguir el tutorial oficial de Google Cloud [click aqui](https://cloud.google.com/sdk/docs/install)

## Creación de proyecto de GCP

Seguidamente debemos crear un proyecto en GCP para poder crear los recursos necesarios para desplegar nuestro modelo, para realizar esto debemos seguir la guia oficial de Google Cloud para crear proyectos [click aqui](https://cloud.google.com/resource-manager/docs/creating-managing-projects#gcloud). La manera más sencilla es con la herramienta de la linea de comandos ejecutando el comando:

    gcloud projects create tf_meetup_colombia

## Creación de bucket de almacenamiento

Para crear recursos de GCP mediante la interfaz de linea de comandos debemos instalar la herramienta gsutil, para esto es recomendable seguir el tutorial oficial de Google cloud [click aqui](https://cloud.google.com/storage/docs/gsutil_install). La manera de crear un bucket de almacenamiento debemos ejecutar el comando:

    gsutil mb gs://modelos

## Creación del modelo en AI Platform

Para desplegar nuestra versión de modelo entrenado, primero debemos crear un modelo en AI Platform, para esto tenemos dos opciones para la creación del modelo, una es la interfaz grafica y la otra es la interfaz de linea de comandos. Para crear un modelo nuevo debemos ejecutar el comando en la interfaz de linea de comandos, ejecutando el comando:

    gcloud ai-platform models create tf_meetup --regions=us-central1

Esto creara nuestro modelo en AI Platform.

# Despliegue

Para desplegar nuestra versión del modelo de DL entrenado y guardado en el formato SavedModel, y ya con el modelo creado en AI Platform, para esto debemos primeramente subir nuestor modelo a GCP en un bucket de almacenamiento, ejecutando el siguiente comando:

    gsutil cp -r flowers/1 gs://modelos

Con el modelo entrenado ya en GCS (Google Cloud Storage), procederemos a desplegar una versión dentro de nuestro modelo, esto para realizar las pruebas y poder utilizar nuestro modelo en diferentes formas, tanto API, librerías de lenguaje de programación o la interfaz de linea de comandos de GCP, para desplegar una nueva versión de nuestro modelo ejecutaremos el siguiente comando:

    gcloud ai-platform versions create v1 --model=tf_meetup --accelerator=type=nvidia-tesla-t4,count=1 --framework=tensorflow --machine-type=n1-standard-4 --origin=gs://modelos/flowers/1/ --python-version=3.7 --region=us-central1 --runtime-version=2.2

# Probar Modelo

Para probar el modelo entrenado y desplegado en AI platform utilizaremos el script en [main.py](https://github.com/JhennerTigreros/zero_to_production/blob/master/main.py), a este debemos proveerle de ciertos argumentos obligatorios los cuales son

-  project-id: Es el identificador de nuestro proyecto en GCP, lo podemos observar en la barra de selección de proyectos en GCP o el que le hayamos asignado en la sección de configuración.
-  img-path: Es la ruta del archivo de prueba que utilizaremos para probar nuestro modelo.
-  region: Es la region donde se encuentra desplegado nuestro modelo de Deep Learning en GCP.
-  model: Es el nombre del modelo desplegado en AI platform.
-  version: Es el nombre de la versión desplegada, por defecto se sirve la versión por defecto.
-  class-names: Los nombres de las clases de las cuales queremos realizar las predicciones.

Para ejecutar el script sería algo así:

    python main.py --project-id tf_meetup_colombia --img-path ./img/prueba.jpg --region us-central1 --model tf_meetup --version v1 --class-names daisy dandelion roses sunflowers tulips