const { ethers } = require("hardhat");

async function main() {
  const [owner, user] = await ethers.getSigners();

  // Attach to deployed contract
  const LoanContract = await ethers.getContractFactory("LoanContract");
  const contract = await LoanContract.attach(
    "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512" // deployed address from your console
  );

  console.log("👤 Owner Address:", owner.address);

  // Request a loan (amount=1000, approved=true)
  const tx = await contract.connect(user).requestLoan(1000, true);
  await tx.wait();

  console.log("✅ Loan requested by:", user.address);

  // Fetch loan details
  const loan = await contract.getLoan(1);
  console.log("📌 Loan Details:", loan);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
