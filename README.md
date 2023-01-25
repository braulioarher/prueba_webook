# Prueba weebook

En este API se puede cargar la informacion a partir del archivo CPdescargas.xl la cual incluye los codigos postales de todas las locaidad des dentro de la Republica Mexicana

## Intruciones para desplegar la aplicacion en un entorno virtual

    1.- Crear entorno virtual usando el comando: python3 -m venv venv
    2.- Activar entorno virtual usando el comando:  source venv/bin/activate
    3.- Instalar las dependeciad de las aplicacion con comando: pip install -r requirements.txt
    4.- Correr la aplicacion en nuestro entorno local usando el comando: flask run

Esta api incluye unicamente recursos de tipo GET donde las rustas se describen en seguida:

    -Ruta /estados:
        GET:
        (Regresesa todos los estados):
            Al usar este recurso nuestra API regresa un JSON con toda la informacion de los estados almacenada en nuestra DB ejemplo:
            http://127.0.0.1:5000/estados
            [
                {
                    "id": 1,
                    "name": "Aguascalientes"
                },
                {
                    "id": 2,
                    "name": "Baja California"
                }, ...
            ]

    -Ruta /estado/<estado_name>:
        GET:
        (Regresa solamente el estado solicitado)
            Al usar este recurso la API regresa detalles del estado almacenados en la DB con sus respectivos municipios ejemplo:
            http://127.0.0.1:5000/estado/Baja California Sur
            {
                "id": 3,
                "name": "Baja California Sur",
                "municipios": [
                    {
                        "id": 31,
                        "name": "Comondú"
                    },
                    {
                        "id": 32,
                        "name": "Mulegé"
                    }, ... ]}

    -Ruta /municipio/<municipio_name>:
        GET:
        (Regresa solamente el municipio solicitado)
            Al usar este recurso la API regresa detalles del municipio almacenado en la DB ejemplo:
            http://127.0.0.1:5000/municipio/Aguascalientes
            {
                "id": 11,
                "name": "Aguascalientes"
            }

    -Ruta /localidad/<municipio_name>:
        GET:
        (Regresa las localidad que coinciden con el nombre solicitado)
            Al usar este recurso la API regresa detalles de las localidades con el nombre solicitado almacenado en la DB ejemplo:
            http://127.0.0.1:5000/localidad/Aguascalientes Centro
            [
                {
                    "id": 1,
                    "name": "Aguascalientes Centro",
                    "cp": 20000,
                    "id_muni": 11
                }
            ]
    -Ruta /localidad/cp/<string:codigo_postal>:
        GET:
        (Regresa las localidades que cuente con el codigo postal solicitado)
            Al usar este recurso la API regresa detalles de las localidades que tengan el codigo postal solicitado ejemplo:
            http://127.0.0.1:5000/localidad/cp/20342
            [
                {
                    "id": 654,
                    "name": "San Francisco",
                    "cp": 20342,
                    "id_muni": 11
                },
                {
                    "id": 655,
                    "name": "San Gerardo",
                    "cp": 20342,
                    "id_muni": 11
                },
                {
                    "id": 656,
                    "name": "Santa Gertrudis",
                    "cp": 20342,
                    "id_muni": 11
                }
            ]

## Desplegar la aplicacion en docker

Para correr el proyecto en un contenedor de docker es necesario tener docker instalados

    1.- Nos posocionamos en la carpeta donde clonamos el repositorio
    2.- Crea una imagen Docker: docker build -t webook-test .
    3.- Crear y correr el contenedor usado docker run -d -p 5005:5000 -w /app -v "$(pwd):/app" weboo-test

La aplicacion correra en el servidor local en el puerto 5005

nota: al crear la imagen en docker se ejecuta el comando FLASK loaddata el cual carga toda la informacion del archivo CPdescargas.xls a la base de datos el resultado sera que tardara un tiempo considerable en cargar toda la informacion