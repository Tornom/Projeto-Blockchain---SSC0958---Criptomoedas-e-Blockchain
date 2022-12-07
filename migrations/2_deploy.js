// migrations/2_deploy.js
const Box = artifacts.require('Box');
const Lucas = artifacts.require('Lucas');
const Recomendacao = artifacts.require('Recomendacao');

module.exports = async function (deployer) {
  await deployer.deploy(Box);
  await deployer.deploy(Lucas);
  await deployer.deploy(Recomendacao);
};