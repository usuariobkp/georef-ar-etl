# Deploy Georef

## Dependencias

- [ElasticSearch >=5.5](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html)
- [Gedal](http://www.gdal.org/index.html)
- [PostgreSQL 9.6](https://www.postgresql.org/download/)
- [PostGis 2.3](http://postgis.net/install/)
- [Python >=3.5.x](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installing/)
- Unzip
- Wget

## Base de datos

Crear **dos** bases de datos en PostgreSQL, ambas con la extensión Postgis (no es requerido que se encuentren en el mismo clúster).

Ejemplo:

```plsql
  -- Creando una base de datos
  CREATE DATABASE indec;
  
  -- Agregando Postgis a la base de datos creada
  CREATE EXTENSION postgis;
```

```plsql
  -- Creando una base de datos
  CREATE DATABASE georef;
  
  -- Agregando Postgis a la base de datos creada
  CREATE EXTENSION postgis;
```

## Instalación

1. Clonar repositorio

    `$ git clone https://github.com/datosgobar/georef.git`

2. Crear entorno virtual e instalar dependencias con pip

    `$ python3.6 -m venv venv`
    
    `(venv)$ pip install -r requirements.txt`

3. Ejecutar el script `etl_indec_vias.sh` para descargar e importar los datos de INDEC:

    ```bash
      cd etl_scripts/
      sh etl_indec_vias.sh
    ```

4. Sincronizar la base de datos

    `$ ./manage.py migrate`

5. Cargar datos de entidades y vías

    `$ ./manage.py runscript load_entities`

    `$ ./manage.py runscript load_roads`


## ElasticSearch

1. Instalar dependencias JDK version 1.8.0_131

  `$ sudo apt install default-jre`
  
2. Instalar eleasticSearch

  `$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.0.0.deb`

  `# dpkg -i elasticsearch-6.0.0.deb`

3. Configuraciones

  `$ sudo vi /etc/elasticsearch/elasticsearch.yml`

  ```
  cluster.name: georef
  node.name: node-1
  network.host: 0.0.0.0
  http.max_content_length: 100mb
  ```
4. Probar el servicio

  `$ curl -X GET 'http://localhost:9200'`
  
5. Crear índices de entidades y vías
    
   `(venv)$ ./manage.py runscript index_entities`
    
   `(venv)$ ./manage.py runscript index_roads`

## Correr App

Agregar la configuración de los servicios `gunicorn` y `nginx`.

1. Configurar servicio y socket en `/etc/systemd/system/`. Completar y modificar los archivos `georef.service` y `georef.socket` de este repositorio.

2. Habilitar y levantar el socket:

    `# systemctl enable georef.socket`

    `# systemctl start georef.socket`

3. Levantar el servicio:

    `# systemctl start georef.service`

4. Para `nginx`, crear `/etc/nginx/sites-available/georef` tomando como base la configuración del archivo `georef.nginx`.

5. Generar un link simbólico a la configuración del sitio:

    `# ln -s /etc/nginx/sites-available/georef /etc/nginx/sites-enabled`,

6. Validar configuración:

    `# nginx -t`

7. Cargar la nueva configuración:

    `# nginx -s reload`

8. Correr Nginx:

    `# nginx`