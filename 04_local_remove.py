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


def main():
    handler = GroupHandler(local_groups=[])
    handler.show_data(help_text="init")
    handler.sync(remote_groups)
    handler.show_data(help_text="after first sync")
    handler.remove_local_resources(group_id=1, resource_ids=[1, 2])
    handler.remove_local_resources(group_id=3, resource_ids=[6, 5])  # remove unknown 6
    handler.show_data(help_text="after add local resources")
    handler.sync(remote_groups)
    handler.show_data(help_text="after add sync")


if __name__ == "__main__":
    main()
