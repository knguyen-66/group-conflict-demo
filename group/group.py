from copy import deepcopy
from typing import override, Literal


class GroupResource:
    id: int
    status: Literal[
        "up to date",
        "added locally",
        "removed locally",
        "added remotely",
        "removed remotely",
    ]

    def __init__(
        self,
        id: int,
        status: Literal[
            "up to date",
            "added locally",
            "removed locally",
            "added remotely",
            "removed remotely",
        ] = "up to date",
    ):
        self.id = id
        self.status = status


class Group:
    id: int
    name: str
    # resources: list[GroupResource]

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    # @override
    # def __str__(self) -> str:
    #     full_str = f"({self.id}) - {self.name}"
    #     for r in self.resources:
    #         full_str += f"\n\t{r.id} - {r.status}"
    #     return full_str


class RemoteGroup(Group):
    resources: list[int]

    def __init__(self, id: int, name: str, resources: list[int]) -> None:
        self.resources = resources
        self.resources.sort()
        super().__init__(id, name)

    @override
    def __str__(self) -> str:
        full_str = f"({self.id}) - {self.name} - {self.resources}"
        return full_str


class LocalGroup(Group):
    resources: dict[int, GroupResource]
    is_base_group: bool

    def __init__(self, id: int, name: str, resources: list[GroupResource], is_base_group: bool = False) -> None:
        self.is_base_group = is_base_group
        self.resources = {r.id: r for r in resources}
        super().__init__(id, name)

    @override
    def __str__(self) -> str:
        full_str = f"({self.id}) - {self.name}{' (base group)' if self.is_base_group else ''}"
        for r in self.resources.values():
            full_str += f"\n\t{r.id} - {r.status}"
        return full_str


class GroupHandler:
    remote_groups: dict[int, RemoteGroup]
    local_groups: dict[int, LocalGroup]

    def __init__(self, remote_groups: list[RemoteGroup], local_groups: list[LocalGroup]) -> None:
        self.remote_groups = {rg.id: rg for rg in remote_groups}
        self.local_groups = {lg.id: lg for lg in local_groups}

    def show_data(self, help_text: str = ""):
        print(f"\n------- Group data ({help_text}) -------")
        print("\nREMOTE:")
        for rg in self.remote_groups.values():
            print(rg)
        print("\nLOCAL:")
        for lg in self.local_groups.values():
            print(lg)

    def add_local_resources(self, group_id: int, resource_ids: list[int]):
        lg = self.local_groups.get(group_id)
        if not lg:
            raise ValueError(f"Local group {group_id} not found")
        for r_id in resource_ids:
            if r_id not in lg.resources:
                lg.resources[r_id] = GroupResource(id=r_id, status="added locally")
                print(f"add_local_resource: resource {r_id} added")
            else:
                print(f"add_local_resource: resource {r_id} already existed, skipping")

    # def fetch_remote(self, new_remote_groups: list[RemoteGroup]):
    #     self.remote_groups = new_remote_groups
    #
    # def fetch_local(self, new_local_groups: list[LocalGroup]):
    #     self.local_groups = new_local_groups

    def sync(self):
        for rg in self.remote_groups.values():
            if rg.id not in self.local_groups:  # group not imported to local
                local_resources = [GroupResource(id=id, status="up to date") for id in rg.resources]
                self.local_groups[rg.id] = LocalGroup(id=rg.id, name=rg.name, resources=local_resources)
            else:
                print("Sync not implemented")
