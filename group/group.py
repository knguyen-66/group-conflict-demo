# from copy import deepcopy
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

    @override
    def __str__(self) -> str:
        return f"(R-{self.id}) - {self.status}"


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
        full_str = f"(RG-{self.id}) - {self.name} - {self.resources}"
        return full_str


class LocalGroup(Group):
    is_base_group: bool
    resources: dict[int, GroupResource]

    def __init__(self, id: int, name: str, resources: list[GroupResource], is_base_group: bool = False) -> None:
        self.is_base_group = is_base_group
        self.resources = {r.id: r for r in resources}
        super().__init__(id, name)

    @override
    def __str__(self) -> str:
        full_str = f"(LG-{self.id}) - {self.name}{' (base group)' if self.is_base_group else ''}"
        for r in self.resources.values():
            full_str += f"\n\t{r.id} - {r.status}"
        return full_str


class GroupHandler:
    # remote_groups: dict[int, RemoteGroup]
    local_groups: dict[int, LocalGroup]

    def __init__(self, local_groups: list[LocalGroup]) -> None:
        # self.remote_groups = {rg.id: rg for rg in remote_groups}
        self.local_groups = {lg.id: lg for lg in local_groups}

    def show_data(self, help_text: str = ""):
        print(f"\n------- Group data ({help_text}) -------")
        # for rg in self.remote_groups.values():
        #     print(rg)
        if self.local_groups == {}:
            print("EMPTY")
        else:
            for lg in self.local_groups.values():
                print(lg)
        print("\n------------------\n")

    def add_local_resources(self, group_id: int, resource_ids: list[int]):
        lg = self.local_groups.get(group_id)
        if not lg:
            raise ValueError(f"Local group {group_id} not found")
        for r_id in resource_ids:
            if r_id not in lg.resources:
                self.local_groups[lg.id].resources[r_id] = GroupResource(id=r_id, status="added locally")
                print(f"* add_local_resources: resource {r_id} in group {lg.id} added")
            else:
                print(f"* add_local_resources: resource {r_id} in group {lg.id} already existed, skipping")

    def remove_local_resources(self, group_id: int, resource_ids: list[int]):
        lg = self.local_groups.get(group_id)
        if not lg:
            raise ValueError(f"Local group {group_id} not found")
        for r_id in resource_ids:
            if r_id in lg.resources:
                self.local_groups[lg.id].resources[r_id].status = "removed locally"
                print(f"* remove_local_resources: resource {r_id} in group {lg.id} marked as removed locally")
            else:
                print(f"* remove_local_resources: resource {r_id} in group {lg.id} not existed, skipping")

    # def fetch_remote(self, new_remote_groups: list[RemoteGroup]):
    #     self.remote_groups = new_remote_groups
    #
    # def fetch_local(self, new_local_groups: list[LocalGroup]):
    #     self.local_groups = new_local_groups

    def apply_changes(self, processed_remote_groups: dict[int, RemoteGroup]):
        removed_locally_group_resources: dict[int, list[int]] = {}
        for lg in self.local_groups.values():
            removed_resource_ids: list[int] = []
            for lr in lg.resources.values():
                if lr.status == "up to date":
                    continue
                if lr.status == "added locally":
                    processed_remote_groups[lg.id].resources.append(lr.id)
                    print(f"* apply_changes: resource {lr.id} in group {lg.id} added from local")
                    self.local_groups[lg.id].resources[lr.id].status = "up to date"
                if lr.status == "removed locally":
                    processed_remote_groups[lg.id].resources.remove(lr.id)
                    print(f"* apply_changes: resource {lr.id} in group {lg.id} removed from local")
                    removed_resource_ids.append(lr.id)

            removed_locally_group_resources[lg.id] = removed_resource_ids

        for lg_id, removed_resource_ids in removed_locally_group_resources.items():
            for lr_id in removed_resource_ids:
                self.local_groups[lg_id].resources.pop(lr_id)
                print(f"* apply_changes: resource {lr_id} in group {lg_id} removed from local")

        print("* apply_changes: final remote group info:")
        for rg in processed_remote_groups.values():
            print(rg)

    def sync(self, fetched_remote_groups: list[RemoteGroup]):
        processed_remote_groups = {rg.id: rg for rg in fetched_remote_groups}

        for rg in processed_remote_groups.values():
            # remote-added groups
            if rg.id not in self.local_groups:
                # resources = [GroupResource(id=id, status="up to date") for id in rg.resources]
                self.local_groups[rg.id] = LocalGroup(id=rg.id, name=rg.name, resources=[])
                print(f"* sync: group {rg.id} added from remote")

            # remote-added resources
            for rr_id in rg.resources:
                if rr_id not in self.local_groups[rg.id].resources:
                    new_lr = GroupResource(id=rr_id, status="up to date")
                    self.local_groups[rg.id].resources[new_lr.id] = new_lr
                    print(f"* sync: resource {new_lr.id} in group {rg.id} added from remote")

        removed_remotely_group_resources: dict[int, list[int]] = {}
        for lg in self.local_groups.values():
            removed_resource_ids: list[int] = []
            for lr in lg.resources.values():
                if lr.id in processed_remote_groups[lg.id].resources and lr.status == "up to date":
                    continue
                if lr.id not in processed_remote_groups[lg.id].resources:
                    # remote-removed resources
                    if lr.status == "up to date":
                        removed_resource_ids.append(lr.id)
                        # --- handle "added locally" and "removed locally" on apply_changes

            removed_remotely_group_resources[lg.id] = removed_resource_ids

        for lg_id, removed_resource_ids in removed_remotely_group_resources.items():
            for rr_id in removed_resource_ids:
                self.local_groups[lg_id].resources.pop(rr_id)
                print(f"* sync: resource {rr_id} in group {lg_id} removed from remote")

        self.apply_changes(processed_remote_groups)
