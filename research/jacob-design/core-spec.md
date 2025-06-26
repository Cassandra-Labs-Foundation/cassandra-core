# core spec

## data model

> NOTE
>
> some data types referenced within another type remain undefined.
> some data types are more or less informative aliases.
> types are a concise form of documentation.

### entity

> NOTE
>
> we could use a common data structure for both persons and businesses and differentiate with an enum field, but we separate them for now.

#### `PersonEntity`

> NOTE
>
> for a person entity, it's unclear whether we should support separate (optional) ID parameters, or whether we should have some enum.
> for example, we could have an enum with variants for e.g. driver's license, passport, SSN, etc.
> each variant of the enum would have a country code or other identifier along with the identifier corresponding to the document.

```
struct PersonEntity {
  id: EntityId,
  name: string,
  dob: timestamp,
  address: Address,
  ssn?: Ssn,
  passport?: Passport,
  license?: DriverLicense,
  email?: EmailAddress,
}
```

#### `BusinessEntity`

```
enum BusinessType {
  SoleProprietor,
  Llc,
  NonProfit,
  ...
}
```

```
struct Incorporation {
  type: BusinessType,
  state: State,
  incorporated: timestamp,
}
```

```
struct BusinessEntity {
  id: EntityId,
  name: string,
  ein: Ein,
  incorporation: Incorporation,
  address: Address,
  owners: PersonEntity[],
}
```

### account

> NOTE
>
> we may want to further distinguish between different savings accounts (e.g. CD, money market, etc).
> additionally, we may want separate types for personal account types and business account types.
> more domain research is necessary.
> the following set is likely non-exhaustive.

```
enum AccountType {
  /// demand deposit account
  Dda,
  /// savings deposit account
  Sda,
  Ira,
  Hsa,
  Joint,
  Custodial,
  MerchantServices,
  Sweep,
  Escrow,
}
```

```
struct Account {
  id: AccountId,
  num: AccountNumber,
  type: AccountType,
  routing: RoutingNumber,
  /// swift BIC code (international wire)
  bic: SwiftBic,
  currency: CurrencyCode,
  name: string,
  owners: EntityId[],
  balance: Balance,
}
```

> NOTE
>
> we need to determine how to represent external accounts (i.e. accounts at other banking institutions).
> column bank denotes an external account as a "counterparty".

> NOTE
>
> I imagine that a user would like some method to retrieve all transfers w.r.t. a particular account.
> however, there are many different transfer types, and it's unclear what the overlap among those types are.
> the obvious overlap is that it represents some movement of some asset into or out of some account(s).
> we may just want to offer one API endpoint under `transfers` to retrieve all transfers w.r.t. some account.
> and then, we can have API endpoints under e.g. `ach` or `wire` to initiate those particular transfer mechanisms.

### transfer

```
enum TransferType {
  Ach,
  Check,
  Swift,
  Wire,
  ...
}
```

```
struct Transfer {
  id: TransferId,
  status: TransferStatus,
  type: TransferType,
  /// e.g. incoming/outgoing
  direction: TransferDirection,
  amount: u64,
  currency: CurrencyCode,
  created: timestamp,
  ...
}
```

...
