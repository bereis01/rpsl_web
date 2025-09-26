# Format of Objects in Buckets

## metadata

Various information about the data stored.

### as_nums

List of unique AS numbers in the database.
Extracted from the keys of 'aut_nums'.

### as_sets

List of unique AS set names in the database.
Extracted from the keys of 'as_sets'.

### addr_prefixes

List of unique prefixes in the database.
Extracted from the keys of 'as_routes'.

### route_sets

List of unique route set names in the database.
Extracted from the keys of 'route_sets'.

## asn

### attributes

Keys are AS numbers as strings. Returns the following object.

```json
{
    'as-name': Str,
    'descr': Str,
    ...
}
```

### imports and exports (RULE_OBJ)

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

#### PEERING_OBJ Format

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

#### FILTER_OBJ Format

```json
{
    'type': ['Any', 'PeerAS', 'AsNum', 'AsSet', 'RouteSet', 'FilterSet', 'AsPathRE', 'Unknown', 'AddrPrefixSet', 'And', 'Or', 'Not', 'Group', 'Community'],
    'value': [Str, Int, List or JSON(Dict)],
    ['left': FILTER_OBJ],
    ['right': FILTER_OBJ],
}
```

#### ACTIONS_OBJ Format

```json
{
    ['pref': Str], 
    ['med', Str],
    ['aspath': [{'method': Str, 'args': [Str]}]],
    ['community': [{'method': Str, 'args': [Str]}]],
}
```

### exchanged_objects

Keys are AS numbers as strings. Returns list of strings refering to the routes imported/exported by the given AS.

### relationships

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
## asset

### attributes

Keys are AS set names as strings. Returns the following object.

```json
{
    'descr': Str,
    ...
}
```

### members

Keys are AS set names as strings. Returns the following object.

```json
{
    'body': Str,
    'members': [Int],
    'set_members': [Str],
    'is_any': Bool,
}
```

## members_inverted

Keys are AS numbers as strings. Returns list of strings refering to AS sets in which the AS number is a member in 'as_sets'.

## membership

Keys are AS numbers as strings. Inside each, there are keys corresponding to AS set names of which the corresponding AS number is a member of. Inside each, there is the corresponding as_set object.

## rs

### attributes

Keys are route set names as strings. Returns the following object.

```json
{
    'descr': Str,
    ...
}
```

### members

Keys are route set names as strings. Returns the following object.

```json
{
    'body': Str,
    'members': [ROUTESET_OBJ],
}
```

#### ROUTESET_OBJ

```json
{
    'type': ['address', 'AS'],
    ['name': Str, 'op': Str],
    ['address_prefix': Str, 'range_operator': Str]
}
```

### members_inverted_as

Keys are AS names as strings. Returns list of strings referring to the route sets that contain the AS name.

### members_inverted_addr

Keys are address prefixes as strings. Returns list of strings referring to the route sets that contain the address prefix.

### members_inverted_rs

Keys are route set names as strings. Returns list of strings referring to the route sets that contain the route set.

## ps

### members

Keys are peering set names as strings. Returns the following object.

```json
{
    'body': Str,
    'peerings': [PEERING_OBJ],
}
```

## fs

### members

Keys are filter set names as strings. Returns the following object.

```json
{
    'body': Str,
    'filters': [FILTER_OBJ],
}
```

## addr

### announces

Keys are AS numbers as strings. Returns the following object.

```json
{
    'routes': [Str]
}
```

### announced_by

Keys are routes/prefixes as strings. Returns the following object.

```json
{
    'announced_by': [Str]
}
```

### announcement

Keys are AS numbers as strings. Inside each, there are keys corresponding to prefixes/routes that are announced by the corresponding AS number. Inside each, there is the corresponding as_routes_inverted object.