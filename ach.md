# ACH

the automated clearing house (ACH) network is a "batch-oriented electronic funds transfer transfer system".
the network is governed by the nacha (national automated clearing house association) operating rules.

> NOTE
>
> apparently you have to pay $70 to access the nacha operating rules and guidelines...
> that does not make sense to me as it should be an open standard.

we note the following characteristics of ACH:

* batch-oriented
* store-and-forward

ACH can process both disbursements (credits) and collections (debits).
ACH is an alternative to paper checks and wire transfers.

we note the following consumer use cases of ACH:

* direct deposit (e.g. payroll)
* direct payment (e.g. bill/loan payments)

we note the following ACH participants:

* originator
* originating depository financial institution (ODFI)
* receiver
* receiving depository financial institution (RDFI)
* ACH operator (i.e. clearinghouse)

we have the following ACH operators:

* Federal Reserve Bank (i.e. FedACH)
* Electronic Payments Network (EPN)

the EPN is owned and operated by the clearing house payments company (PayCo).
PayCo is a child of the clearing house (association).
both PayCo and the clearing house association their own managing board.
members of the clearing house include large commercial banks such as JP Morgan Chase and Barclays.

> NOTE
>
> we need to determine how a ODFI chooses whether to submit ACH transactions via FedACH or EPN.

| ACH transaction | AKA    | example        | originator delta | receiver delta |
|-----------------|--------|----------------| -----------------|----------------|
| credit          | "push" | direct deposit | -                | +              |
| debit           | "pull" | bill payments  | +                | -              |

each ACH transaction must contain a standard entry class (SEC) code.
the SEC code specifies the nature of the ACH transaction.
example SEC codes include corporate credit or debit (CCD) and pre-arranged payment or deposit (PPD).
the ODFI must include the correct SEC code in the ACH transaction.

ACH flow:

* the originator obtains authorization from the receiver to transact against the receiver's account
  * the authorization method (e.g. written) depends on the SEC code for the ACH transaction
* the originator submits payment instructions to its ODFI
* the ODFI compiles the originator's payment instructions into an ACH entry
* the ODFI collects ACH entries from its originators and compiles those entries into one or more batches
* the ODFI compiles one or more batches into an ACH file
* the ODFI submits the ACH file to an ACH operator (FedACH or EPN)
* the ACH operator dispatches ACH entries to the corresponding RDFIs
* the RDFI receives ACH entries from the ACH operator and posts those entries to the accounts of the corresponding receivers

> TODO: verify accuracy of ACH flow above

ACH flow illustration:

![ACH flow](/assets/ach-flow-chart.png)

> source: [nacha (how ACH works)](https://achdevguide.nacha.org/how-ach-works)
