const VotacionElecciones = artifacts.require ("VotacionElecciones");

module.exports = function(deployer) {
  deployer.deploy(VotacionElecciones, ["paco", "pepe"]);
}