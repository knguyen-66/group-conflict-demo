from group.group import RemoteGroup, GroupHandler

remote_groups: list[RemoteGroup] = [
    RemoteGroup(
        id=1,
        name="Group A",
        resources=[1, 2, 3, 4, 5],
    ),
    RemoteGroup(
        id=2,
        name="Group B",
        resources=[2, 4],
    ),
    RemoteGroup(
        id=3,
        name="Group C",
        resources=[5],
    ),
]

new_remote_groups: list[RemoteGroup] = [
    RemoteGroup(
        id=1,
        name="Group A",
        resources=[1, 2, 3, 4, 6],  # remove 5, add 6
    ),
    RemoteGroup(
        id=2,
        name="Group B",
        resources=[4],  # remove 2
    ),
    RemoteGroup(
        id=3,
        name="Group C",
        resources=[1, 5],  # add 1
    ),
    RemoteGroup(  # add group 4
        id=4,
        name="Group D",
        resources=[1, 6],
    ),
]


def main():
    handler = GroupHandler(local_groups=[])
    handler.show_data(help_text="init")
    handler.sync(remote_groups)
    handler.show_data(help_text="after first sync")
    handler.sync(remote_groups)
    handler.show_data(help_text="after unchanged sync")
    handler.sync(new_remote_groups)
    handler.show_data(help_text="after changed sync")
    # handler.add_local_resources(group_id=3, resource_ids=[6, 7])
    # handler.show_data(help_text="after add local resources")


if __name__ == "__main__":
    main()
