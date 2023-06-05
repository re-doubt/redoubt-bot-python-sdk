# re:doubt Bot Python SDK

[![PyPI](https://img.shields.io/pypi/v/redoubt-agent?color=blue)](https://pypi.org/project/redoubt-agent/)

The re:doubt monitors TON on-chain activity in real-time, detecting threats and other security-related events. 
The network is made up of numerous detection bots developed by a community of Web3 developers and security experts. 
Each bot acts like a little security camera monitoring something specific on-chain. What the re:doubt detects is a 
direct result of the bots being run. Some bots monitor generic threats, and others monitor protocol-specific activity.

See the developer documentation at [re:doubt documentation](https://docs.redoubt.online)

## Installation

Install Python 3 package: `pip3 install redoubt-agent`

## API Keys

To use SDK one need to request API key from [@RedoubtAPIBot](https://t.me/RedoubtAPIBot) and pass it either directly 
to `RedoubtEventsStream` instance or using `REDOUBT_API_KEY` environment variable.

## Examples

### New pools bot

* [New pools detector](https://github.com/re-doubt/redoubt-bot-python-sdk/blob/main/examples/new_pools.py)

It is monitoring for new pools and just prints info.

### Jetton transfers bot

* [Jetton transfers bot](https://github.com/re-doubt/redoubt-bot-python-sdk/blob/main/examples/jetton_transfer.py)

More complicated example. It listens for all Jetton transfers and after receiving info 
about the transfer it requests additional info over GraphQL API. In this case it
uses additional GraphQL request to get Jetton metadata (symbol and decimals).

As a result you will get such a message:
```
EQ...EJ => EQ...7f 22.033882202 SCALE
```
