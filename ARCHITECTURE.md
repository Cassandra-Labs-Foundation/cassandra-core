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

### quality/performance

`TODO`

### engineering required

`TODO`
