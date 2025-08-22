from group.group import GroupResource, RemoteGroup, LocalGroup, GroupHandler

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
    handler = GroupHandler(remote_groups=remote_groups, local_groups=[])
    handler.show_data(help_text="init")
    handler.sync()
    handler.show_data(help_text="after sync")
    handler.add_local_resources(group_id=3, resource_ids=[6, 7])
    handler.show_data(help_text="after add local resources")


if __name__ == "__main__":
    main()
