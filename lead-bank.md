graph LR
    A[Increase_BaaS_API]
    A --> CB[Core_Banking_Functions]
    A --> UN[Underlying_Networks]
    A --> DT[Developer_Tools]
    A --> CP[Compliance_and_Protection]
    A --> TL[Transfer_Lifecycle]
    A --> CUST[Customization]
    A --> CON[Concepts]

    subgraph CB[Core_Banking_Functions]
        ACC[Accounts]
        ACC --> ACC_OP[OP_POST_/accounts]
        ACC --> ACC_DATA[DATA_GET_/accounts_id]

        ACH[ACH_Transfers]
        ACH --> ACH_OP[OP_POST_/ach_transfers]
        ACH --> ACH_DATA[DATA_GET_/ach_transfers_id]

        WIRE[Wires]
        WIRE --> WIRE_OP[OP_POST_/wires]
        WIRE --> WIRE_DATA[DATA_GET_/wires_id]

        CHECKS[Checks]
        CHECKS --> CHECKS_OP[OP_POST_/checks]
        CHECKS --> CHECKS_DATA[DATA_GET_/checks_id]

        RTP[Real-Time_Payments]
        RTP --> RTP_OP[OP_POST_/rtp_payments]
        RTP --> RTP_DATA[DATA_GET_/rtp_payments_id]

        CARDS[Cards]
        CARDS --> CARDS_OP[OP_POST_/cards]
        CARDS --> CARDS_DATA[DATA_GET_/cards_id]
    end

    subgraph UN[Underlying_Networks]
        UN_ACH[ACH_FedACH]
        UN_FEDWIRE[Fedwire]
        UN_CHECK21[Check_21]
        UN_RTP[Real-Time_Payments_Network]
        UN_VISA[Visa]
    end

    subgraph DT[Developer_Tools]
        API_REF[API_Reference]
        SDK[SDKs]
        OAUTH[OAuth]
        OAUTH --> OAUTH_OP[OP_POST_/oauth_token]
        OAUTH --> OAUTH_DATA[DATA_GET_/oauth_info]
        IDEMPOT[Idempotency_Keys]
        WEBHOOK[Webhooks_and_Events]
        WEBHOOK --> WEBHOOK_DATA[DATA_GET_/events]
        DATA_DICT[Data_Dictionary]
        RELIABILITY[Reliability]
    end

    subgraph CP[Compliance_and_Protection]
        BOOK[Bookkeeping]
        INFOSEC[Information_Security]
        EXT_DEP[Extended_Deposit_Insurance]
        ONBOARD[Platform_Onboarding]
        OVERSIGHT[Ongoing_Oversight]
    end

    subgraph TL[Transfer_Lifecycle]
        INB[Inbound_ACH_Transfers]
        INB --> INB_DATA[DATA_GET_/inbound_ach_transfers_id]
        OUTB[Outbound_ACH_Transfers]
        OUTB --> OUTB_DATA[DATA_GET_/outbound_ach_transfers_id]
    end

    subgraph CUST[Customization]
        CARD_ART[Custom_Card_Artwork]
        PHYS_CARDS[Physical_Cards]
        DIGI_WALLET[Digital_Wallets]
    end

    subgraph CON[Concepts]
        ROLES[Roles_and_Permissions]
        TRANS[Transactions_and_Transfers]
        APPROVALS[Transfer_Approvals]
    end

    %% Relationship Arrows Across Clusters
    ACC_OP --> ONBOARD
    ACH_OP --> TL
    RTP_OP --> TL
    CARDS_OP --> CP
    ACH_DATA --> TRANS
    CARDS_DATA --> TRANS
    OAUTH --> API_REF
    WEBHOOK --> CP
    INB_DATA --> BOOK
    OUTB_DATA --> BOOK
