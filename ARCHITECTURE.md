# architecture

## ledger

we consider the following options:

* [modern treasury](https://www.moderntreasury.com)
* [fragment](https://fragment.dev)
* [tigerbeetle](https://tigerbeetle.com)
* custom SQL database

below we analyze the options on several dimensions.

### hosting

both modern treasury and fragment would be hosted by the respective entity.
if a hosted service that we critically rely on experiences (non-negligible) downtime, then we are fucked.
given that tigerbeetle is open source, we have the option to self-host.
tigerbeetle mentions in their documentation that a hosted option could be available.
however, I think the ability to self-host is a strong advantage.
in the event that we build our own custom solution, then we would self-host.

### lindy (effect)

modern treasury seems to have been around for quite some time and also have some big customers.
fragment is quite new, so its survival is less certain.
between modern treasury and fragment, I don't think fragment makes sense on this dimension (at this time).
tigerbeetle is a young project, but it is open source.
even if the tigerbeetle project dies, we would still be able to maintain a fork and self-host.
no database technology (that I am aware of) is more lindy than SQL.
SQL is [boring technology](https://mcfunley.com/choose-boring-technology), and that is a virtue.

### capabilities

both modern treasury and fragment have a superset of the capabilities of tigerbeetle.
tigerbeetle only supports accounts and transfers.
each account exists within a particular ledger, where a ledger represents a logical grouping (e.g. a distinct asset).
you can create and manage transactions between accounts within the same ledger.
you can also perform "atomically linked transfers" to perform cross-ledger operations (e.g. currency exchange).
tigerbeetle is an account and transfer workhorse, but it would require that we build some other scaffolding around it.
for example, tigerbeetle accounts only have a 128-bit identifier.
to link a tigerbeetle account to a bank account, we would have to manage that in a separate database.
another example is reporting.
tigerbeetle does not have support for report generation out of the box, so we would have to build such a pipeline.

modern treasury and fragment have a richer data model...

### quality/performance

`TODO`

### engineering required

`TODO`

### pricing

general pricing info is unavailable for both modern treasury and fragment.
pricing is only available upon a discussion with the respective engineering/sales team.

we omit pricing for both tigerbeetle and the custom SQL solution, because we can self-host.
the cost of the managed tigerbeetle is not available in the documentation.
