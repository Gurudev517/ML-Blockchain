const hre = require("hardhat");

async function main() {
  // Get the contract factory
  const LoanContract = await hre.ethers.getContractFactory("LoanContract");

  // Deploy the contract (await ensures deployment is complete)
  const loan = await LoanContract.deploy();

  // In ethers v6, use `loan.target` instead of `loan.address`
  console.log(`LoanContract deployed to: ${loan.target}`);
}

// Run the script and handle errors
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
