import pandas as pd

def load_data():
    entitlements = pd.read_excel(r"C:\Users\Aryanaman\Desktop\Secure Code Python\SOD_Ruleset.xlsx", sheet_name="ENTITLEMENT_MST")
    privileges = pd.read_excel(r"C:\Users\Aryanaman\Desktop\Secure Code Python\XX_7_PVLGS_MASTER_RPT.xlsx", sheet_name=None)

    if isinstance(privileges, dict):  
        privileges = next(iter(privileges.values()))

    privilege_roles = pd.read_excel(r"C:\Users\Aryanaman\Desktop\Secure Code Python\XX_6_PVLG_TO_ROLE_RELATION_RPT.xlsx")
    role_hierarchy = pd.read_excel(r"C:\Users\Aryanaman\Desktop\Secure Code Python\XX_5_ROLE_TO_ROLE_HIER_RPT.xlsx")
    user_roles = pd.read_excel(r"C:\Users\Aryanaman\Desktop\Secure Code Python\XX_3_USER_ROLE_MAPPING_RPT.xlsx")
    sod_rules = pd.read_excel(r"C:\Users\Aryanaman\Desktop\Secure Code Python\SOD_Ruleset.xlsx", sheet_name="SOD_MASTER")
    user_details = pd.read_excel(r"C:\Users\Aryanaman\Desktop\Secure Code Python\XX_2_USER_DETAILS_RPT.xlsx")
    role_details = pd.read_excel(r"C:\Users\Aryanaman\Desktop\Secure Code Python\XX_4_ROLE_MASTER_DETAILS_RPT.xlsx")

    return entitlements, privileges, privilege_roles, role_hierarchy, user_roles, sod_rules, user_details, role_details

def map_user_details(user_details):
    return dict(zip(user_details['USER_ID'], user_details['USER_DISPLAY_NAME']))

def map_role_details(role_details):
    return dict(zip(role_details['ROLE_ID'], role_details['ROLE_NAME']))

def map_entitlements_to_privileges(entitlements, privileges):
    entitlement_mapping = {}
    valid_privileges = set(privileges['CODE'].astype(str).str.strip().str.upper())

    for _, row in entitlements.iterrows():
        access_point = str(row['ACCESS_POINT_ID']).strip().upper()
        entitlement = row['ACCESS_ENTITLEMENT']
        if access_point and access_point != "NAN" and access_point in valid_privileges:
            entitlement_mapping[access_point] = entitlement

    return entitlement_mapping

def map_privileges_to_roles(privilege_roles):
    privilege_role_mapping = {}
    for _, row in privilege_roles.iterrows():
        privilege_id = str(row['PRIVILEGE_ID']).strip().upper()
        role_id = str(row['ROLE_ID']).strip().upper()
        if role_id not in privilege_role_mapping:
            privilege_role_mapping[role_id] = set()
        privilege_role_mapping[role_id].add(privilege_id)
    return privilege_role_mapping

def map_users_to_roles(user_roles):
    user_role_mapping = {}
    for _, row in user_roles.iterrows():
        user_id = str(row['USER_ID']).strip().upper()
        role_id = str(row['ROLE_ID']).strip().upper()
        if user_id not in user_role_mapping:
            user_role_mapping[user_id] = set()
        user_role_mapping[user_id].add(role_id)
    return user_role_mapping

def detect_conflicts(user_roles, privilege_roles, entitlement_mapping, sod_rules, user_map, role_map):
    conflicts = []
    sod_set = set(zip(sod_rules['ENT_LEG1'], sod_rules['ENT_LEG2']))

    for user, roles in user_roles.items():
        user_entitlements = set()
        for role in roles:
            if role in privilege_roles:
                for privilege in privilege_roles[role]:
                    if privilege in entitlement_mapping:
                        user_entitlements.add(entitlement_mapping[privilege])

        for ent1 in user_entitlements:
            for ent2 in user_entitlements:
                if (ent1, ent2) in sod_set or (ent2, ent1) in sod_set:
                    for role in user_roles[user]:
                        conflicts.append({
                            "User ID": user,
                            "User Name": user_map.get(user, "Unknown"),
                            "Role ID": role,
                            "Role Name": role_map.get(role, "Unknown"),
                            "Entitlement 1": ent1,
                            "Entitlement 2": ent2
                        })

    return conflicts

def generate_conflict_report(conflicts):
    df = pd.DataFrame(conflicts)
    df.to_excel("Conflict_Report.xlsx", index=False)
    print("✅ Conflict report generated: Conflict_Report.xlsx")

def main():
    entitlements, privileges, privilege_roles, role_hierarchy, user_roles, sod_rules, user_details, role_details = load_data()
    
    entitlement_mapping = map_entitlements_to_privileges(entitlements, privileges)
    privilege_role_mapping = map_privileges_to_roles(privilege_roles)
    user_role_mapping = map_users_to_roles(user_roles)

    user_map = map_user_details(user_details)
    role_map = map_role_details(role_details)

    conflicts = detect_conflicts(user_role_mapping, privilege_role_mapping, entitlement_mapping, sod_rules, user_map, role_map)
    generate_conflict_report(conflicts)

if __name__ == "__main__":
    main()