def convert_computers(input_data):
    data = {
        'data': [],
        'meta': {
            'type': 'computers',
            'count': 0,
            'version': 4,
            'methods': 0
        }
    }

    for computer in input_data['computers']:
        obj = {
            'PrimaryGroupSID': computer['PrimaryGroupSid'],
            'AllowedToDelegate': computer['AllowedToDelegate'],
            'AllowedToAct': [{'ObjectIdentifier': entry['MemberId'], 'ObjectType': entry['MemberType']} for entry in computer['AllowedToAct']],
            'HasSIDHistory': [],
            'Sessions': {
                'Collected': True,
                'FailureReason': None,
                'Results': computer['Sessions']
            },
            # This doesn't exist in the v3 data source
            'PrivilegedSessions': {
                'Collected': True,
                'FailureReason': None,
                'Results': []
            },
            # This doesn't exist in the v3 data source
            'RegistrySessions': {
                'Collected': True,
                'FailureReason': None,
                'Results': []
            },
            'LocalAdmins': {
                'Collected': True,
                'FailureReason': None,
                'Results': [{'ObjectIdentifier': entry['MemberId'], 'ObjectType': entry['MemberType']} for entry in computer['LocalAdmins']]
            },
            'RemoteDesktopUsers': {
                'Collected': True,
                'FailureReason': None,
                'Results': computer['RemoteDesktopUsers']
            },
            'DcomUsers': {
                'Collected': True,
                'FailureReason': None,
                'Results': computer['DcomUsers']
            },
            'PSRemoteUsers': {
                'Collected': True,
                'FailureReason': None,
                'Results': computer['PSRemoteUsers']
            },
            'Status': None,
            'Aces': computer['Aces'],
            'ObjectIdentifier': computer['ObjectIdentifier'],
            'IsDeleted': False,
            'IsACLProtected': False,
            'Properties': computer['Properties']
        }

        obj['Properties']['lastlogon'] = obj['Properties']['lastlogontimestamp']
        obj['Properties']['whencreated'] = 0
        obj['Properties']['sidhistory'] = []

        data['data'].append(obj)

    data['meta']['count'] = len(data['data'])
    return data


trust_types = {
    0: 'ParentChild',
    1: 'CrossLink',
    2: 'Forest',
    3: 'External',
    4: 'Unknown'
}

trust_directions = {
    0: 'Disabled',
    1: 'Inbound',
    2: 'Outbound',
    3: 'Bidirectional'
}


def convert_domains(input_data):
    data = {
        'data': [],
        'meta': {
            'type': 'domains',
            'count': 0,
            'version': 4,
            'methods': 0
        }
    }

    for domain in input_data['domains']:
        obj = {
            'ChildObjects': [],
            'Trusts': [],
            'Links': [{'IsEnforced': link['IsEnforced'], 'GUID': link['Guid']} for link in domain['Links']],
            'Aces': domain['Aces'],
            'ObjectIdentifier': domain['ObjectIdentifier'],
            'IsDeleted': False,
            'IsACLProtected': False,
            'GPOChanges': {
                'LocalAdmins': [],
                'RemoteDesktopUsers': [],
                'DcomUsers': [],
                'PSRemoteUsers': [],
                'AffectedComputers': []
            },
            'Properties': domain['Properties']
        }

        for ou in domain['ChildOus']:
            obj['ChildObjects'].append({
                'ObjectIdentifier': ou,
                'ObjectType': 'OU'
            })

        for trust in domain['Trusts']:
            obj['Trusts'].append({
                'TargetDomainSid': trust['TargetDomainSid'],
                'TargetDomainName': trust['TargetDomainName'],
                'IsTransitive': trust['IsTransitive'],
                'SidFilteringEnabled': trust['SidFilteringEnabled'],
                'TrustDirection': trust_directions[trust['TrustDirection']],
                'TrustType': trust_types[trust['TrustType']]
            })

        data['data'].append(obj)

    data['meta']['count'] = len(data['data'])

    return data


def convert_gpos(input_data):
    data = {
        'data': [],
        'meta': {
            'type': 'gpos',
            'count': 0,
            'version': 4,
            'methods': 0
        }
    }

    for gpo in input_data['gpos']:
        obj = {
            'Aces': gpo['Aces'],
            'ObjectIdentifier': gpo['ObjectIdentifier'],
            'IsDeleted': False,
            'IsACLProtected': True,
            'Properties': gpo['Properties']
        }

        obj['Properties']['whencreated'] = 0

        data['data'].append(obj)

    data['meta']['count'] = len(data['data'])

    return data


def convert_groups(input_data):
    data = {
        'data': [],
        'meta': {
            'type': 'groups',
            'count': 0,
            'version': 4,
            'methods': 0
        }
    }

    for group in input_data['groups']:
        obj = {
            'Members': [{'ObjectIdentifier': member['MemberId'], 'ObjectType': member['MemberType']} for member in group['Members']],
            'Aces': group['Aces'],
            'ObjectIdentifier': group['ObjectIdentifier'],
            'IsDeleted': False,
            'IsACLProtected': True,
            'Properties': group['Properties']
        }

        data['data'].append(obj)

    data['meta']['count'] = len(data['data'])

    return data


def convert_ous(input_data):
    data = {
        'data': [],
        'meta': {
            'type': 'ous',
            'count': 0,
            'version': 4,
            'methods': 0
        }
    }

    for ou in input_data['ous']:
        obj = {
            'Links': [{'IsEnforced': link['IsEnforced'], 'GUID': link['Guid']} for link in ou['Links']],
            'ChildObjects': [],
            'Aces': ou['Aces'],
            'ObjectIdentifier': ou['ObjectIdentifier'],
            'IsDeleted': False,
            'IsACLProtected': ou['ACLProtected'],
            'GPOChanges': {
                'LocalAdmins': [],
                'RemoteDesktopUsers': [],
                'DcomUsers': [],
                'PSRemoteUsers': [],
                'AffectedComputers': []
            },
            'Properties': ou['Properties']
        }

        obj['Properties']['whencreated'] = 0

        for user in ou['Users']:
            obj['ChildObjects'].append({
                'ObjectIdentifier': user,
                'ObjectType': 'Users'
            })

        for computer in ou['Computers']:
            obj['ChildObjects'].append({
                'ObjectIdentifier': computer,
                'ObjectType': 'Computer'
            })

        for cou in ou['ChildOus']:
            obj['ChildObjects'].append({
                'ObjectIdentifier': cou,
                'ObjectType': 'OU'
            })

        data['data'].append(obj)

    data['meta']['count'] = len(data['data'])

    return data


def convert_users(input_data):
    data = {
        'data': [],
        'meta': {
            'type': 'users',
            'count': 0,
            'version': 4,
            'methods': 0
        }
    }

    for user in input_data['users']:
        obj = {
            'AllowedToDelegate': user['AllowedToDelegate'],
            'PrimaryGroupSID': user['PrimaryGroupSid'],
            'HasSIDHistory': user['HasSIDHistory'],
            'SPNTargets': user['SPNTargets'],
            'Aces': user['Aces'],
            'ObjectIdentifier': user['ObjectIdentifier'],
            'IsDeleted': False,
            'IsACLProtected': True,
            'Properties': user['Properties']
        }

        obj['Properties']['whencreated'] = 0

        data['data'].append(obj)

    data['meta']['count'] = len(data['data'])

    return data


converters = {
    'computers': convert_computers,
    'domains': convert_domains,
    'gpos': convert_gpos,
    'groups': convert_groups,
    'ous': convert_ous,
    'users': convert_users,
}
