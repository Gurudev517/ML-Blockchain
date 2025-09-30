// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title LoanContract
 * @dev Stores loan applications and their ML-based approval/rejection results on the blockchain.
 */
contract LoanContract {

    // Define loan structure
    struct Loan {
        address borrower;   // who applied
        uint amount;        // loan amount
        uint duration;      // duration in months
        string decision;    // ML model decision (Approved / Rejected)
    }

    // Mapping of loanId => Loan details
    mapping(uint => Loan) public loans;
    uint public loanCount;  // total loans stored

    // Event to track new loan storage
    event LoanStored(
        uint loanId,
        address borrower,
        uint amount,
        uint duration,
        string decision
    );

    /**
     * @dev Store loan decision from ML model
     * @param _amount Loan amount
     * @param _duration Loan duration
     * @param _decision ML model decision (Approved/Rejected)
     */
    function storeLoan(uint _amount, uint _duration, string memory _decision) public {
        loans[loanCount] = Loan(msg.sender, _amount, _duration, _decision);

        emit LoanStored(loanCount, msg.sender, _amount, _duration, _decision);

        loanCount++;
    }

    /**
     * @dev Fetch loan details by ID
     * @param _loanId Loan identifier
     * @return borrower Address of applicant
     * @return amount Loan amount
     * @return duration Duration in months
     * @return decision ML model decision
     */
    function getLoan(uint _loanId) public view returns (address borrower, uint amount, uint duration, string memory decision) {
        Loan memory l = loans[_loanId];
        return (l.borrower, l.amount, l.duration, l.decision);
    }
}
