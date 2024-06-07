# Inventario con QR

En este repositorio se encuentran los archivos relacionados con la construcción de un sistema de gestión de inventario de una bodega con QR. El sistema cuenta con una central desde la que se hacen las solicitudes de pedidos, el ingreso de nuevos productos, la extracción de estos de la bodega, así como el manejo de los tiempos de la línea de ensamblaje de los productos. Este sistema está dividido en tres partes principales: picking, estaciones/portales y centrales.

## Picking
El sistema de picking consiste en la recolección y ubicación de productos en las estanterías de las bodegas. Para esto, el sistema emplea un Arduino Nano RP 2040 Connect, el cual incluye un módulo WiFi, además de un sistema de tiras LEDs RGB ubicadas en cada posición de la estantería. En la carpeta `leds` del repositorio, se encuentra el código en Arduino (`leds.ino`) del sistema. Este código utiliza las librerías WiFiNINA y Adafruits_Neopixel para recibir la información del encendido de los LEDs de cada posición correspondiente para el ingreso y salida de productos, por medio de WiFi. También en esa carpeta, se encuentra un código de prueba en Python que utiliza la librería "socket" para el envío de datos usando el protocolo HTTPS.

Por otra parte, para la lectura de los QR en todo el sistema, se empleó una ArduCAM basada en un ESP32. En la carpeta `arduipistola` se encuentran dos archivos: `arduipistola.ino`, el cual usa las librerías ESP32CAM y WiFi para enviar imágenes capturadas por la ESPCAM por medio del protocolo HTTPS hacia el computador central; y el archivo `esp32pistola.py`, el cual trabaja con las librerías OpenCV, pyzbar, pysql y otras, de manera que establece una conexión entre la base de datos del sistema completo y el Arduino RP 2040 que controla los LEDs.

## Estaciones/Portales
Para esta parte, se utilizaban 7 estaciones de ensamblaje, las cuales tienen un computador propio y sobre la que se visualiza una página web para el registro de tiempos. En la carpeta `Pagina_estaciones` se encuentra todo el diseño y el funcionamiento de la página web de las estaciones. Esta página lee los QR de los kits de los productos, así como un manual de ensamblaje y el monitoreo de los tiempos de trabajo y de inactividad. La página web, además, establece una conexión con la base de datos central para modificar las tablas de los tiempos de ensamblaje totales del sistema.

## Centrales
La central cuenta con una página web desde la cual se controla el sistema completo. En la carpeta `Pagina_web` se encuentra todo el diseño de la página web del computador central. Desde esta, se puede hacer un inicio de sesión con los usuarios registrados, se puede hacer la solicitud de pedidos de productos, se puede solicitar el ingreso o la extracción de productos a la bodega y se puede observar la base de datos del inventario general y de los tiempos de logística. Toda la base de datos se construyó usando SQL.