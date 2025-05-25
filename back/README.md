# Format of Objects in Buckets

## as_nums

List of unique AS numbers in the database.
Extracted from the keys of 'aut_nums'.

## aut_nums

Keys are AS numbers as strings. Returns the following object.

```json
{
    'body': Str,
    'n_import': Int
    'n_export': Int
}
```

## imports and exports (RULE_OBJ)

Keys are AS numbers as strings. Returns list of the following object.

```json
{
    'version': ['ipv4', 'ipv6', 'any'],
    'cast': ['unicast', 'multicast', 'any']
    'peering': PEERING_OBJ,
    'actions': ACTIONS_OBJ
    'filter': FILTER_OBJ
}
```

### PEERING_OBJ Format

```json
{
    'remote_as': {
                    'field': ['Single', 'Group', 'Operation', 'PeeringSet'], 
                    'type': [['Num', 'Set', 'Invalid'], ['And', 'Or', 'Except'], ['And', 'Or', 'Except'], ['PeeringSet']], 
                    'value': [Int, Str or JSON(Dict)],
                    ['left': REMOTE_AS_OBJ,]
                    ['right': REMOTE_AS_OBJ,]
                },

    'remote_router': {
                        'field': ['Ip', 'InetRtrOrRtrSet', 'And', 'Or', 'Except'], 
                        'value': [Str],
                        ['left': ROUTER_OBJ,]
                        ['right': ROUTER_OBJ,]
                    }

    'local_router': {
                        'field': ['Ip', 'InetRtrOrRtrSet', 'And', 'Or', 'Except'], 
                        'value': [Str],
                        ['left': ROUTER_OBJ,]
                        ['right': ROUTER_OBJ,]
                    }
}
```

### FILTER_OBJ Format

```json
{
    'type': ['Any', 'PeerAS', 'AsNum', 'AsSet', 'RouteSet', 'FilterSet', 'AsPathRE', 'Unknown', 'AddrPrefixSet', 'And', 'Or', 'Not', 'Group', 'Community'],
    'value': [Str, Int, List or JSON(Dict)],
    ['left': FILTER_OBJ],
    ['right': FILTER_OBJ],
}
```

### ACTIONS_OBJ Format

```json
{
    ['pref': Str], 
    ['med', Str],
    ['aspath': [{'method': Str, 'args': [Str]}]],
    ['community': [{'method': Str, 'args': [Str]}]],
}
```

## as_sets

Keys are AS set names as strings. Returns the following object.

```json
{
    'body': Str,
    'members': [Int],
    'set_members': [Str],
    'is_any': Bool,
}
```

## as_sets_inverted

Keys are AS numbers as strings. Returns list of strings refering to AS sets in which the AS number is a member in 'as_sets'.

## route_sets

Keys are route set names as strings. Returns the following object.

```json
{
    'body': Str,
    'members': [ROUTESET_OBJ],
}
```

## peering_sets

Keys are peering set names as strings. Returns the following object.

```json
{
    'body': Str,
    'peerings': [PEERING_OBJ],
}
```

## filter_sets

Keys are filter set names as strings. Returns the following object.

```json
{
    'body': Str,
    'filters': [FILTER_OBJ],
}
```

## as_routes

Keys are AS numbers as strings. Returns the following object.

```json
{
    'routes': [Str]
}
```

## relationships

Keys are AS numbers as strings. Returns a list of the following object.

```json
{
    'asn': Str,
    'peer': PEERING_OBJ,
    'tor': ["Provider", "Customer", "Peer"],
    'import': RULE_OBJ,
    'export': RULE_OBJ,
}
```