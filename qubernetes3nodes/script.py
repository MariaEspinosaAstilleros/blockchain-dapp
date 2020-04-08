#!/usr/bin/python3
import os
import sys
import argparse

def añadir_nodo():
    nodes = 0

    with open('qubernetes.yaml') as file:
        data = file.readlines()

    linea = data[5]
    for char in linea:
        if char.isdigit():
            nodes = int(char) + 1
            break

    data[5] = '  number: {}\n'.format(nodes)
    
    with open('qubernetes.yaml', 'w') as file:
        file.writelines(data)


    with open('nodes.yaml', 'a') as file:
        print('\n', file=file)
        print('- member:', file=file)
        print('    NodeUserIdent: quorum-node{}'.format(nodes), file=file)
        print('    Key-Dir: key{}'.format(nodes), file=file)

    os.system('echo 2 | ./quorum-init')

    for i in range (1,nodes):
        os.system('cp -r ./out/deployments/0{}-quorum-single-deployment.yaml ./out_old'.format(i))
        os.system('rm -r ./out/deployments/0{}-quorum-single-deployment.yaml'.format(i))

    os.system('kubectl apply -f out -f out/deployments')


def quitar_nodo():
    nodes = 0
    
    with open('qubernetes.yaml') as file:
        data = file.readlines()

    linea = data[5]
    for char in linea:
        if char.isdigit():
            nodes = int(char) - 1
            break

    data[5] = '  number: {}\n'.format(nodes)

    with open('qubernetes.yaml', 'w') as file:
        file.writelines(data)
    
    with open('nodes.yaml') as file:
        data_nodes = file.readlines()

    with open('nodes.yaml', 'w') as file:
        file.writelines(data_nodes[0:-4])

    os.system('kubectl delete -n default deployment quorum-node{}-deployment'.format(nodes+1))
    os.system('rm out/deployments/0{}-quorum-single-deployment.yaml'.format(nodes+1))
    os.system('rm -r out/config/key{}'.format(nodes+1))

def iniciar_cluster():
    os.system('minikube start --memory 6144')
    os.system('echo 1 | ./quorum-init')
    os.system('kubectl apply -f out -f out/deployments')

def eliminar_cluster():
    os.system('minikube delete')    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script para añadir o quitar nodos de al red de Quorum')
    parser.add_argument('-a', '--add', action='store_true', help='añade nodo a la red')
    parser.add_argument('-r', '--remove', action='store_true', help='quita nodo de la red')
    parser.add_argument('-s', '--start', action='store_true', help='Inicia el cluster')
    parser.add_argument('-d', '--delete', action='store_true', help='Elimina el cluster')

    args = vars(parser.parse_args())

    if args['add']:
        añadir_nodo()
    elif args['remove']:
        quitar_nodo()
    elif args['start']:
        iniciar_cluster()
    elif args['delete']:
        eliminar_cluster()
    else:
        sys.exit(1)