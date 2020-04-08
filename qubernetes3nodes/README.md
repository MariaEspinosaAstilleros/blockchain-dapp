## Requisitos

- Funciona en equipos Mac y Linux.
- Paquetes necesarios: constellation, bootnode, geth, docker, kubectl y minikube.
- CPU de mas de 2 núcleos, más de 6 GB de RAM y más de 2 GB de espacio en el disco duro.

## Instrucciones

- Iniciar el cluster 

   python3 script.py -s
   
- Eliminar el cluster

   python3 script.py -d

- Scale in

   python3 script.py -a

- Scale out

   python3 script.py -r