from typing import List, Optional, Tuple
from app.models.group import Group

# Заглушечная БД
_groups_db = {
    1: Group(id=1, name="МАТ-101", faculty="Математический факультет"),
    2: Group(id=2, name="ИНФ-202", faculty="Факультет информатики"),
}
_next_group_id = 3

def create_group(name: str, faculty: str) -> Group:
    global _next_group_id
    group = Group(id=_next_group_id, name=name, faculty=faculty)
    _groups_db[group.id] = group
    _next_group_id += 1
    return group

def get_all_groups(page: int = 1, limit: int = 20) -> Tuple[List[Group], int]:
    groups = list(_groups_db.values())
    total = len(groups)

    start = (page - 1) * limit
    end = start + limit
    paginated = groups[start:end]

    return paginated, total

def get_group_by_id(group_id: int) -> Optional[Group]:
    return _groups_db.get(group_id)