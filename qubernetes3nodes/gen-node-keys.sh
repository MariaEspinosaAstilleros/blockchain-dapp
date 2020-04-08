#!/bin/bash







NODE_DIRS=key1,key2,key3,key4,key5,key6,key7


BASE_DIR=$(pwd)/out/config


mkdir -p $BASE_DIR
IFS=', ' read -r -a array <<< "$NODE_DIRS"

for node_key_dir in "${array[@]}"; do
  KEY_DIR=$BASE_DIR/$node_key_dir
  echo "KEY DIR IS $KEY_DIR"
  ## If key dir exists, skip it.
  if [ ! -d $KEY_DIR ]; then
    pushd .
    mkdir -p $KEY_DIR
    cd $KEY_DIR
    echo | constellation-node --generatekeys=tm
    touch password.txt
    geth --keystore $KEY_DIR  account new --password password.txt
    bootnode -genkey nodekey
    bootnode  -nodekeyhex $(cat nodekey) -writeaddress > enode
    popd
  else
    echo "Key Dir exists! Skipping creating new key in $KEY_DIR"
  fi
done
