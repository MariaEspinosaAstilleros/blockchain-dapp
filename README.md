# Introducción a blockchain

## Integrantes y roles
* Daniel Ballesteros Almazán - Red blockchain y backend
* María Espinosa Astilleros  - Backend y frontend 

## Objetivo
La práctica se divide en tres partes: diseño de la Dapp, diseño del backend e integración y despliegue de la Dapp en una red de blockchains (usando Quorum). La maqueta final consistirá inicialmente de una red con tres nodos que ejecutarán Quorum. Debe poder escalar fácilmente, de forma que debe incluirse un método para añadir nodos según sea necesario. La Dapp se desplegará como un Smart Contract dentro de la red. Finalmente, el backend se conectará a cualquier nodo de la red para operar con el sistema. 
Para implementar la Dapp se usará Solidity. 

## 3rd parties utilizadas
Las 3rd parties utilizadas son las siguientes:
- VirtualBox 6.0.14
- Minikube/Kubectl
- pyWeb3
- bootnode
- geth
- constellation
- truffle
- ganache-cli

## Instrucciones de despliegue
Para despelgar la red de blockchain, consultar el README.rd de la carpeta **qubernetes3nodes**. Una vez que ya tiene desplegada la red, hay que compilar el Smart Contract. Primero, nos movemos a la carpeta de **despliegue_dapp**, y después usamos el siguiente comando:
```bash
truffle compile
```
Después, en un terminal aparte, se deja ejecutando el siguiente comando:
```bash
geth --rpc
```
Mientras esta corriendo, en otro terminal se ejecuta:
```bash
truffle migrate
```
Para ejecutar el frontend, hay que ejecutar:
```bash
python3 Votaciones.py
```