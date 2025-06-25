This is an experiment to see if it's possible to run a banking core on a Stablecoin 

## Roadmap

- [ ] Connect with Solana blockchain 
- [ ] Figure out how to create a stablecoin 
- [ ] On-ramp 
- [ ] Off-ramp

## Developer Notes

### Mar 29th 2025

- ok let's do this

- today I'm going to experiment with Grok to see if it's able to help me code a blockchain project like this
    - then I need to try Claude because that's the default model I use for code 

- ok Grok is helping me scopre this out
    - we want to tokenize deposits so that we use Solana as the primary ledger
    - it says that we should connect to Solana's public RPCs
    - we want to create and manage tokens
    - our on/off ramp logic is likely off chain 
        - Solana transactions will be focused on token minting and burning
    - no Rust or self-hosted Node

- the options appear to be
    - web3.js which submits transactions to a public RPC
        - @solana/spl-token mints tokens for on-ramps, burn them off-ramps 
        - it handles all token operations (create mint, mint tokens, transfer, burn) via JavaScript.
    - python which doesn't make sense in this context
    - QuickNode or Alchemy SDK
        - apparently it's built on top of web3.js
        - Free tiers (e.g., QuickNode’s 1M requests/month)
        - QuickNode is apparently more reliable than public RPCs (fewer rate limits or downtime).
    - manual tokenization through the Solana CLI 
        - doesn't exactly scale for the banking core
    - solana-go uses RPC endpoints over HTTP/JSON-RPC
        - Connect to Solana clusters (devnet, testnet, mainnet).
        - Query account data, submit transactions, and interact with SPL tokens.
        - Supports token creation, minting, and transfers via the SPL Token program.

- we can use solana-go either by itself or with Quicknode
    - public RPC endpoints can be slow, rate-limited, or overloaded, especially on Mainnet during high traffic.
        - Spreading requests across multiple public RPCs reduces the burden on any single endpoint, potentially easing rate limits (e.g., if one RPC caps at 200 req/s, 70 RPCs could theoretically handle 14,000 req/s combined).
        - No single point of failure—if one RPC goes down, only that entity is affected, not all 70.
        - however, there aren’t 70 reliable, distinct public RPCs for Solana
        - Rate Limits: Public RPCs don’t scale with your usage—each still throttles, so 70 entities hitting limits simultaneously could clog the system.
        - Consistency: Different RPCs might lag or desync, causing ledger discrepancies (e.g., one entity sees a deposit before another).
    - QuickNode’s hosted nodes, which are optimized for speed and reliability.
        - QuickNode runs and maintains the nodes for you—still no self-hosting required.
        - QuickNode’s nodes are load-balanced, less prone to downtime, and rarely rate-limited on free tiers.
        - WebSocket support for real-time updates (e.g., deposit confirmations)
    - QuickNode’s RPC nodes are designed for high-throughput apps. 
        - Their free tier offers 1M requests/month
        - paid plans (e.g., “Discover” at $9/month) give 5M requests
        - higher tiers (e.g., “Scale” at $299/month) offer 100M requests/month with dedicated resources.

- however, any of these QuickNode fees are on top of the Solana fees
    - traditional cores often charge percentage-based fees for payments (e.g., 2%–3%), while Solana’s fixed fees favor larger transactions, enhancing cost-effectiveness.



