from create_db import PlannerModel

# Function to get a list of the excel planner ids
def get_excel_ids(session):
    results = session.query(PlannerModel).all()
    ids = []
    for row in results:
        if row.planner_id_excel not in ids:
            ids.append(row.planner_id_excel)
    return ids

# Function to get a list of all the staff members
def get_staff(session):
    results = session.query(PlannerModel).all()
    staff = []
    for row in results:
        if row.staff_code not in staff:
            staff.append(row.staff_code)
    return staff

# Function to get a list of all the classes that a staff member teaches
def get_classes_for_staff(session, staff_code):
    results = session.query(PlannerModel).filter(PlannerModel.staff_code == staff_code).all()
    classes = []
    for row in results:
        if row.class_code not in classes:
            classes.append(row.class_code)
    return classes

# Function to get a list of all the staff members that teach a class
def get_staff_for_class(session, class_code):
    results = session.query(PlannerModel).filter(PlannerModel.class_code == class_code).all()
    staff = []
    for row in results:
        if row.staff_code not in staff:
            staff.append(row.staff_code)
    return staff

# Function to filter and sort data
def filter_and_sort_data(session, staff_code=None, date_range=None, class_code=None, sort_by=None):
    query = session.query(PlannerModel)
    if staff_code:
        query = query.filter(PlannerModel.staff_code == staff_code)
    if date_range:
        query = query.filter(PlannerModel.period_date.between(*date_range))
    if class_code:
        query = query.filter(PlannerModel.class_code == class_code)
    if sort_by:
        query = query.order_by(sort_by)
    return query.all()