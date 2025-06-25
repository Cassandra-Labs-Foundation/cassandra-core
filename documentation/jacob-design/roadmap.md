# roadmap

## routing transit number (RTN)

we outline the following steps to obtain a RTN from the american bankers association (ABA):

1. obtain charter
1. (optional) establish correspondent bank relationships
1. submit application to ABA (includes fee)
1. obtain RTN assignment from ABA

to the extent that we can, we need to pipeline obtaining the charter and obtaining the RTN.

while we await an official RTN, we can easily go with a placeholder for system simulation/testing.

## payment systems

### FedLine direct

FedLine direct is the computer-to-computer interface to federal reserve financial services.
it will enable us to achieve the highest level of automation possible.
communications are encrypted end-to-end.

FedLine direct provides access to the following services:

* FedACH
* FedWire funds
* FedWire securities
* FedWire statements
* accounting/billing
* reporting

other technical requirements include the following:

* WebSphere MQ (FedLine direct message)
* Connect:Direct (FedLine direct file)

we need to determine whether we can gain access to FedLine direct specifications while we await our charter/RTN.

### ach

the two ACH operators are the federal reserve (i.e. FedACH) and the clearing house (TCH) electronic payments network (EPN).
we can choose to integrate with FedACH or EPN or both.
if we have to choose one, then I assume it would be better to start with FedACH.
the two operators have facilities to inter-operate with each other.
if we integrate with FedLine direct for FedWire, then we will have done some of the legwork for FedACH.
I suspect that if we can satisfy the regulatory requirements for FedACH, then we can satisfy the regulatory requirements for EPN.
AFAICT the federal reserve has more public documentation.
TCH gatekeeps essentially all documentation behind a subscription.
AFAICT we won't be able to get around the $70-105 to obtain the NACHA operating rules.

assuming we have a RTN (see above), we outline the following steps to onboard with FedACH:

1. (optional) establish membership at a regional payments association (RPA)
1. submit application to the federal reserve bank that serves our district
1. establish a master account with the federal reserve
1. integrate ACH system(s) with FedACH
1. ensure ACH system(s) pass FedACH tests and comply with NACHA operating rules
1. establish settlement agreement for master account at federal reserve bank
1. submit participation/authorization agreement(s) to the federal reserve
1. coordinate launch with FedACH

AFAICT we cannot submit an application to FedACH until we have a charter.
I'm not sure how much of a balance we would need to maintain in the master account at the federal reserve.
in addition to the technical requirements, we will also have to maintain operational procedures to manage ACH transactions.

### wire

[FedWire funds services forms](https://www.frbservices.org/forms/wires)

### RTP/FedNow

### checks

## reporting

we will be required to generate various reports for regulatory/compliance purposes.

those reports include the following (among others):

* financials (e.g. capital adequacy)
* lending (e.g. fair lending practices)
* monitoring (e.g. suspicious activity)
* taxes (e.g. interest paid)

we need to enumerate all of the various reports that we must generate and develop automated processes for generation.
