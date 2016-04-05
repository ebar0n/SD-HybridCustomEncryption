# Criptografía simétrica y asimétrica
Se usaron algoritmos personalizados de encriptación, basados en operaciones matemáticas, para encriptar y desencriptar la data circulante entre un cliente y un servidor, dependiendo del tipo de llave.

### Funcionamiento 
Proceso ejecutado en la apps conectadas por protocolo TCP
- Se instancia un servidor para tener disponibilidad en un puerto `x`
- Se  instancia un cliente, y se indica la información de ubicación del servidor.
- El cliente decide si quiere establecer una comunicación segura o no.
- Si la comunicación es segura el servidor genera un par de llaves publicas y privadas, enviándole la publica al cliente.
- El cliente al recibir la llave, genera su par de llaves y envía la publica al cliente.
- Una vez el servidor recibe la lave publica del cliente, genera un key único para ser usado en el método asimétrico, y lo envía encriptandolo con la llave publica del cliente.
- EL cliente recibe este único key y lo desencripta de forma asimétrica con su llave privada.
- La comunicación continua encriptando la información de forma simétrica, con el key ya compartido de forma segura.
- El servidor (Si no hubo comunicación segura llega a este paso) envía una lista de archivos disponibles, al cliente.
- El cliente solicitad uno de los archivos al servidor e inicia su descarga.
- Una vez finaliza la descarga el cliente se desconecta, y el servidor queda activo esperando mas solicitudes de descarga.
