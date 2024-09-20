# sandbox

we will provide a sandbox environment to enable high-fidelity simulation(s).
within the sandbox, you will have access to the entire API.
the state of the sandbox will persist until you choose to tear it down.

the sandbox will be available at a dedicated domain (TBD).

at the outset, we intend to offer an API similar to column.

> NOTE
>
> one exception is card issuance, since column does not offer a card API domain.
> for card issuance, the initial plan is to offer an issuing API similar to stripe.

you will be able to create entities, accounts, transfers, etc.
the default behavior of the API call will assume the "happy path" (e.g. AML/KYC approval).
other behavior will be available via simulation-only API endpoints and/or parameters.

certain API domains may be subject to time-restricted processing to simulate realistic conditions.
for example, ACH and wire transfers are subject to particular processing time windows.
time restriction overrides will be available via simulation-only API endpoints and/or parameters.
