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
