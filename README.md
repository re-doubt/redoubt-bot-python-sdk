# re:doubt Threat Detection Python SDK

The re:doubt monitors TON on-chain activity in real-time, detecting threats and other security-related events. 
The network is made up of numerous detection bots developed by a community of Web3 developers and security experts. 
Each bot acts like a little security camera monitoring something specific on-chain. What the re:doubt detects is a 
direct result of the bots being run. Some bots monitor generic threats, and others monitor protocol-specific activity.

See the developer documentation at [docs.redoubt.online](https://docs.redoubt.online)

## Bot examples

* [New pools detector](./new_pools.py)

## API keys

To use SDK one need to request API key from @RedoubtAPIBot and pass it either directly to 
``RedoubtEventsStream`` instance or using REDOUBT_API_KEY env variable.

## Examples

### New pools bot

It is monitoring for new pools and just prints info

### Jetton transfers bot

More complicated example. It listens for all Jetton transfers and after receiving info 
about the transfer it requests additional info over GraphQL API. In this case it
uses additional GraphQL request to get Jetton metadata (symbol and decimals).

As a result you will get such a message:
```
EQ...EJ => EQ...7f 22.033882202 SCALE
```
