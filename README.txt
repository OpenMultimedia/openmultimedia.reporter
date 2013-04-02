.. -*- coding: utf-8 -*-

.. contents:: Tabla de Contenidos

Introducción
============
Este producto provee la funcionalidad de `Soy reportero`_.


Características
===============
- Se proveen 2 tipos de contenido:

    - Sección soy reportero
    - Reporte anónimo


Requisitos previos
==================
TBD


Información de desarrollador
============================
`Soy reportero`_ funciona íntimamente relacionado con una aplicación multimedia externa con la que debe poder comunicarse para su correcto funcionamiento.
La comunicación se realiza por medio del paquete ``openmultimedia.api``, en donde se configura la ubicación del servidor externo y los parametros necesarios para la comunicación. Algunos parametros adicionales, se configuran desde el panel de control de `Soy reportero`_
La explicación a continuación, asume lo siguiente::

  La dirección base del servidor es: http://multimedia.tlsur.net/api/
  La dirección para subir contenido es: http://multimedia.tlsur.net/api/upload
  La dirección para notificar la subida de un video es: http://multimedia.tlsur.net/api/clip
  La dirección para notificar la subida de una imagen es: http://multimedia.tlsur.net/api/imagen
  Se tiene, además, 2 llaves de seguridad, una para subir el archivo y otra para la notificacion que finalizó su procesamiento.

En este caso, la dirección base es lo único que se configura desde ``openmultimedia.api``, el resto es configurado desde el panel de control de `Soy reportero`_

El proceso de carga de un reporte se inicia al subir un archivo a http://multimedia.tlsur.net/api/upload.
Al finalizar la carga, el sistema remoto retorna en el campo 'id' de la respuesta, un identificador unico que va a utilizar para ese archivo subido, el cual es almacenado localmente, al guardarse el reporte.


Es en este momento (al guardarse el reporte), en que el sistema remoto es notificado para que se cree la estructura.
En el caso de ser un video, se hara a http://multimedia.tlsur.net/api/clip y en el caso de una imagen, a http://multimedia.tlsur.net/api/imagen.
Como parametros del request, se incluyen el titulo con el que se creo el reporte, el id (retornado previamente al haberse subido el archivo), y un url de 'callback', que sera utilizado por el sistema remoto para notificar que el procesamiento del archivo multimedia, ha finalizado.

En la respuesta a este request, se incluye el slug del archivo en el sistema remoto.


Para que el reporte sea visible, se necesita avanzar a un estado "pendiente de revisión", el sistema remoto debe realizar un request a esta "callback" url, agregando un parametro 'key' y otro 'type'. El parámetro 'type' puede ser o bien 'error', o bien 'success', en base a si el procesamiento finalizo en algun error, o con exito.
El parametro 'key', es un hash MD5 que se forma con la llave secreta de notificacion y id del archivo. El algoritmo en python sería:: 

  >>> m = hashlib.md5()
  >>> m.update(secret_key+file_id)
  >>> hash = m.hexdigest()

Al recibir el request con un 'type' y un 'key' válidos, el reporte pasa al estado "pendiente de revisión", y se pide el contenido remoto a: http://multimedia.tlsur.net/api/clip/file_slug en caso de un video o a: http://multimedia.tlsur.net/api/imagen/file_slug en caso de una imagen, cargando asi el contenido local al reporte, si es que el reporte se encuentra publicado en el sistema remoto. Es a partir de este momento, que el reporte es visible para el adminsitrador de los reportes, en el listado de reportes no publicados, desde donde, el administrador accede a algún reporte en particular y lo publica, para que sea visible por cualquier visitante del sitio.

Instalación
===========
Usted puede leer el archivo ``INSTALL.txt`` dentro del directorio ``docs`` de este paquete.


Descargas
=========
Usted puede encontrar la versión de desarrollo del paquete ``openmultimedia.reporter`` en el `repositorio OpenMultimedia`_ en Github.com.


Autor(es) Original(es)
======================

* Franco Pellegrini aka frapell

Para una lista actualizada de todo los colaboradores visite: https://github.com/teleSUR/telesur.reportero/contributors

.. _Soy reportero: http://exwebserv.telesurtv.net/secciones/psoy_reportero/
.. _repositorio OpenMultimedia: https://github.com/OpenMultimedia/openmultimedia.reporter


