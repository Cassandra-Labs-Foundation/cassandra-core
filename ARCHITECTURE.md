# architecture

## ledger

we will use tigerbeetle for the ledger.
given that tigerbeetle is open source, we have the option to self-host.
tigerbeetle mentions in their documentation that a hosted option could be available.
however, I think the ability to self-host is a strong advantage.
compliance requirements may dictate that we self-host.
tigerbeetle is a young project, but it is open source.
even if the tigerbeetle project dies, we would still be able to maintain a fork and self-host.

> TigerBeetle has a "zero dependencies" policy, apart from the Zig toolchain.

a minimal number of dependencies is a huge advantage.
each additional dependency introduces risk (e.g. supply chain attack).

tigerbeetle only supports accounts and transfers.
each account exists within a particular ledger, where a ledger represents a logical grouping (e.g. a distinct asset).
you can create and manage transactions between accounts within the same ledger.
you can also perform "atomically linked transfers" to perform cross-ledger operations (e.g. currency exchange).

### quality/performance

`TODO`

### engineering required

tigerbeetle is an account and transfer workhorse, but it would require that we build some other scaffolding around it.
we accept the specialization of tigerbeetle, and it is line with our philosophy of modularity/composition.
for example, tigerbeetle accounts only have a 128-bit identifier.
to link a tigerbeetle account to a bank account, we would have to manage that in a separate database.
another example is lack of support for report generation out of the box, so we would have to build such a pipeline.

### pricing

we omit pricing for both tigerbeetle, because we can self-host.
the cost of the managed tigerbeetle is not available in the documentation.
