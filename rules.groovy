{
    "rules": {
        "Users": {
            ".read": "auth != null",
            ".indexOn":["Data/Handle", "Data/ID"],

            "$user_id": {
                "Belongings": {
                    "Dataframes": {
                        "Collaborations": {
                                "$df_id": {
                                    ".write": "$user_id === auth.uid || root.child('Dataframes/' + $df_id + '/Belongings/Owner').val() === auth.uid"
                                }
                        },
                        "Owned": {
                            ".write": "$user_id === auth.uid"
                        }
                    }
                },
                "Data": {
                        ".write": "$user_id === auth.uid"
                }
            }
        },
        "Dataframes": {
            ".indexOn": ["Owner", "Collaborators"],

            "$df_id": {
                ".read": "auth != null &&
                (
                    root.child('Users/' + auth.uid + '/Belongings/Dataframes/Owned/' + $df_id).val() === true ||
                    root.child('Users/' + auth.uid + '/Belongings/Dataframes/Collaborations/' + $df_id).val() === true
                )",
              	".write": "!data.exists() ||
                (
                    auth != null &&
										(
                        (data.exists() && newData.exists() && root.child('Users/' + auth.uid + '/Belongings/Dataframes/Collaborations/' + $df_id).val() === true) ||
                        root.child('Users/' + auth.uid + '/Belongings/Dataframes/Owned/' + $df_id).val() === true
                    )
                )"
            }
        }
    }
}
