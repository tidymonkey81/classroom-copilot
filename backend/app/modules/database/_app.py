# %% [markdown]
# # Classroom Copilot

# %% [markdown]
# An AI copilot for learners and educators.

# %% [markdown]
# ## Setup the local environment

# %%
# Install the necessary libraries
#!pip install -r ./requirements.txt

# %%
# Setup the environment
import sys
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
sys.path.append(os.getenv("PY_MODULES_PATH"))

import logger_tool as logger

log_file = 'classroomcopilot-init'
# logger_name = os.path.basename(__file__)
logger_name = 'logger_tool'
log_level = os.getenv('LOG_LEVEL')

logging = logger.get_logger(name=logger_name, log_level=log_level, log_file=log_file)
logging.app(f"Logger {logger_name} has been instantiated with log level {log_level}. Log file: {log_file}.log")

# Setup tools
import setup_app as app
app.setup_tools()
app.setup_tools('neo')
app.setup_tools('planner')

# Setup the environment directories
data_path = os.getenv('DATA_PATH')
dbfs_path = os.getenv('DBFS_PATH')

# %%
# Import packages
import driver_tools as neo
from datetime import datetime, date, time, timedelta

import pandas as pd
import json
import shutil

import get_planner as planner

# %%
def str_to_bool(s):
    return s.lower() == 'true'

# %% [markdown]
# ## Setup the app environment

# %% [markdown]
# ### Options

# %%
class OptionsAccessor:
    def __init__(self, options):
        self.options = options

    def get(self, category, *keys):
        # Traverse the options dictionary using the category and keys
        value = self.options.get(category, {})
        for key in keys:
            if isinstance(value, dict):  # Ensure we can continue traversing
                value = value.get(key, {})
            else:  # Stop if we reach a non-dict type before finding all keys
                return None
        return value

class AccessOptionsAccessor:
    def __init__(self, options_accessor):
        self.options_accessor = options_accessor

    def get(self, key):
        return self.options_accessor.get('access_options', key)


class RunOptionsAccessor:
    def __init__(self, options_accessor):
        self.options_accessor = options_accessor

    def get(self, key):
        return self.options_accessor.get('default_run_options', key)


class InitOptionsAccessor:
    def __init__(self, options_accessor):
        self.options_accessor = options_accessor

    def get(self, key):
        return self.options_accessor.get('init_options', key)


class LocalCalendarOptionsAccessor:
    def __init__(self, init_options_accessor):
        self.init_options_accessor = init_options_accessor

    def get(self, *keys):
        return self.init_options_accessor.get('local_calendar_options', *keys)


class LocalPlannerOptionsAccessor:
    def __init__(self, init_options_accessor):
        self.init_options_accessor = init_options_accessor

    def get(self, *keys):
        return self.init_options_accessor.get('local_planner_options', *keys)
    
class LocalCurriculumOptionsAccessor:
    def __init__(self, init_options_accessor):
        self.init_options_accessor = init_options_accessor

    def get(self, *keys):
        return self.init_options_accessor.get('local_curriculum_options', *keys)


# %%
def load_options_from_file(filepath):
    with open(filepath, 'r') as file:
        options = json.load(file)
    return options

# Call the accessor classes for options
def get_options_accessor(options):
    options_accessor = OptionsAccessor(options)
    access_options_accessor = AccessOptionsAccessor(options_accessor)
    run_options_accessor = RunOptionsAccessor(options_accessor)
    init_options_accessor = InitOptionsAccessor(options_accessor)
    local_calendar_options_accessor = LocalCalendarOptionsAccessor(init_options_accessor)
    local_planner_options_accessor = LocalPlannerOptionsAccessor(init_options_accessor)
    local_curriculum_options_accessor = LocalCurriculumOptionsAccessor(init_options_accessor)
    return (options_accessor, access_options_accessor, run_options_accessor,
            init_options_accessor, local_calendar_options_accessor, local_planner_options_accessor, local_curriculum_options_accessor)

# %% [markdown]
# ### Labels

# %%
class LabelsAccessor:
    def __init__(self, labels, type='calendar'):  # Default type is 'calendar'
        self.labels = labels
        self.type = type  # 'calendar', 'planner' or 'curriculum'

    def get(self, category, key):
        # Construct the full key based on the type
        full_key = f'local_{self.type}_{category}'
        return self.labels.get(full_key, {}).get(key, None)

class NodeLabelsAccessor(LabelsAccessor):
    def __init__(self, labels_accessor):
        super().__init__(labels_accessor.labels, labels_accessor.type)  # Pass the type to the parent class

    def get(self, key):
        return super().get('node_labels', key)  # Use 'node_labels' as the category

class NodePropertiesAccessor(LabelsAccessor):
    def __init__(self, labels_accessor):
        super().__init__(labels_accessor.labels, labels_accessor.type)

    def get(self, key):
        return super().get('node_properties', key)

class HierarchyLabelsAccessor(LabelsAccessor):
    def __init__(self, labels_accessor):
        super().__init__(labels_accessor.labels, labels_accessor.type)

    def get(self, key):
        return super().get('hierarchy_labels', key)

class HierarchyPropertiesAccessor(LabelsAccessor):
    def __init__(self, labels_accessor):
        super().__init__(labels_accessor.labels, labels_accessor.type)

    def get(self, key):
        return super().get('hierarchy_properties', key)

# %%
# Function to load labels from a JSON file
def load_labels_from_file(filepath):
    with open(filepath, 'r') as file:
        labels = json.load(file)
    return labels

# Call the accessor classes
def get_planner_labels_accessor(labels):
    planner_labels_accessor = LabelsAccessor(labels, type='planner')
    node_labels_accessor = NodeLabelsAccessor(planner_labels_accessor)
    node_properties_accessor = NodePropertiesAccessor(planner_labels_accessor)
    hierarchy_labels_accessor = HierarchyLabelsAccessor(planner_labels_accessor)
    hierarchy_properties_accessor = HierarchyPropertiesAccessor(planner_labels_accessor)
    return (planner_labels_accessor, node_labels_accessor, node_properties_accessor, hierarchy_labels_accessor, hierarchy_properties_accessor)

def get_calendar_labels_accessor(labels): # TODO: Autogenerated
    calendar_labels_accessor = LabelsAccessor(labels, type='calendar')
    node_labels_accessor = NodeLabelsAccessor(calendar_labels_accessor)
    node_properties_accessor = NodePropertiesAccessor(calendar_labels_accessor)
    hierarchy_labels_accessor = HierarchyLabelsAccessor(calendar_labels_accessor)
    hierarchy_properties_accessor = HierarchyPropertiesAccessor(calendar_labels_accessor)
    return (calendar_labels_accessor, node_labels_accessor, node_properties_accessor, hierarchy_labels_accessor, hierarchy_properties_accessor)

def get_curriculum_labels_accessor(labels): # TODO: Autogenerated
    curriculum_labels_accessor = LabelsAccessor(labels, type='curriculum')
    node_labels_accessor = NodeLabelsAccessor(curriculum_labels_accessor)
    node_properties_accessor = NodePropertiesAccessor(curriculum_labels_accessor)
    hierarchy_labels_accessor = HierarchyLabelsAccessor(curriculum_labels_accessor)
    hierarchy_properties_accessor = HierarchyPropertiesAccessor(curriculum_labels_accessor)
    return (curriculum_labels_accessor, node_labels_accessor, node_properties_accessor, hierarchy_labels_accessor, hierarchy_properties_accessor)

# %% [markdown]
# ## Build graphs

# %% [markdown]
# ### Graph helper functions

# %% [markdown]
# #### Sequencing

# %%
def create_single_sequence_relationship(session, start_node, end_node):
    sequence_rel = neo.create_relationship(session, start_node=start_node, end_node=end_node, label='HAS_NEXT', returns=True)
    return sequence_rel

def sequence_list_of_nodes(session, nodes):
    logging.prod("Creating sequenced relationships between total number of nodes: " + str(len(nodes)))
    sequenced_rels = []
    for i in range(len(nodes)-1):
        sequence_rel = create_single_sequence_relationship(session, nodes[i], nodes[i+1])
        sequenced_rels.append(sequence_rel)
    return sequenced_rels

# %% [markdown]
# #### Temporal

# %%
# We will hard code properties but get labels
def create_now_node(session, state_labels_accessor):
    now_node_dict = {}
    properties = {
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'minute': datetime.now().minute,
        'hour': datetime.now().hour,
        'day': datetime.now().day,
        'month': datetime.now().month,
        'year': datetime.now().year
    }
    now_node = neo.create_node(session, state_labels_accessor.get('now_node'), properties, returns=True) # probably not right
    now_node_dict['node'] = now_node
    now_node_dict['properties'] = properties
    return now_node_dict

def create_current_state(local_calendar_session, local_calendar_dict, local_calendar_labels, local_calendar_properties, local_state_labels, local_state_properties):
    # Create the now node
    now_node_dict = create_now_node(local_calendar_session, local_state_labels)
    local_calendar_dict['now_node'] = now_node_dict
    logging.prod("Created now node")

    # Create the relationship between now and local calendar nodes for the current time_chunk, the current day, the current month, and the current year
    # Get the current time_chunk
    current_time_chunk = local_calendar_dict['time_chunks']['current'] # TODO: This is a placeholder

    return local_calendar_dict

# %% [markdown]
# ### Local calendar

# %% [markdown]
# #### Setup the local calendar

# %%
# Functions to prepare properties
def prepare_local_calendar_node(label, start, end, data_dir=None):
    logging.app("Preparing local calendar node properties for type: " + label)
    if label == 'Year':
        logging.pedantic("Preparing local calendar node properties for year: " + str(start))
        properties = {
            'start_date': start.isoformat(),
            'end_date': end.isoformat()
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'Month':
        logging.pedantic("Preparing local calendar node properties for month: " + str(start.isoformat()))
        properties = {
            'start_month': '{}-{}'.format(start.isoformat().year, start.isoformat().month),
            'end_month': '{}-{}'.format(end.isoformat().year, end.isoformat().month)
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'Week':
        logging.pedantic("Preparing local calendar node properties for week: " + str(start.isoformat()))
        properties = {
            'start_week': '{}-{}'.format(start.isoformat().year, start.isoformat().isocalendar()[1]),
            'end_week': '{}-{}'.format(end.isoformat().year, end.isoformat().isocalendar()[1])
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'Date':
        logging.pedantic("Preparing local calendar node properties for date: " + str(start.isoformat()))
        properties = {
            'start_date': start.isoformat(),
            'end_date': end.isoformat()
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'TimeChunk':
        logging.pedantic("Preparing local calendar node properties for time chunk: " + str(start.isoformat()))
        properties = {
            'start_time_chunk': start.isoformat(),
            'end_time_chunk': end.isoformat()
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    else:
        return ValueError("Invalid type of local calendar node")

def prepare_local_year_node(year, year_of_calendar, data_dir=None):
    logging.pedantic("Preparing local year node properties for year: " + str(year))
    properties = {
        'year': year,
        'year_of_calendar': year_of_calendar,
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_month_node(year, month, month_of_calendar, data_dir=None):
    logging.pedantic("Preparing local month node properties for year: " + str(year) + " and month: " + str(month))
    properties = {
        'year_month': '{}-{}'.format(year, month),
        'month_of_calendar': month_of_calendar,
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_week_node(start_date, week_of_calendar, data_dir=None):
    logging.pedantic("Preparing week node properties for year: " + str(start_date.year) + " and week: " + str(start_date.isocalendar()[1]))
    properties = {
        'year_iso_week': '{}-{}'.format(start_date.year, start_date.isocalendar()[1]),
        'week_of_calendar': week_of_calendar,
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_date_node(date, d, data_dir=None):
    logging.pedantic("Preparing local date node properties for date: " + date.isoformat())
    properties = {
        'date': date,
        'day_of_calendar': d,
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_time_chunk_node(time_chunk_start, time_chunk_minutes, time_chunk_for_calendar, data_dir=None):
    logging.pedantic("Preparing local time chunk node properties for start time chunk: " + time_chunk_start.isoformat())
    properties = {
        'time_chunk_start': time_chunk_start,
        'time_chunk_duration_minutes': time_chunk_minutes,
        'time_chunk_of_calendar': time_chunk_for_calendar
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties


# %%
# Create the constraints
def create_local_calendar_node_constraints(session, labels): # TODO: by file
    local_calendar_node_labels_accessor = get_calendar_labels_accessor(labels)[1]
    local_year_node_label = local_calendar_node_labels_accessor.get('local_year_node_label')
    local_month_node_label = local_calendar_node_labels_accessor.get('local_month_node_label')
    week_node_label = local_calendar_node_labels_accessor.get('week_node_label')
    local_date_node_label = local_calendar_node_labels_accessor.get('local_date_node_label')
    local_time_chunk_node_label = local_calendar_node_labels_accessor.get('local_time_chunk_node_label')
    with session.begin_transaction() as tx:
        local_year_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (y:{local_year_node_label}) REQUIRE y.year IS NOT NULL",
            f"CREATE CONSTRAINT FOR (y:{local_year_node_label}) REQUIRE y.year IS UNIQUE"
        ]
        local_month_constraint_queries = [
            f"CREATE CONSTRAINT FOR (m:{local_month_node_label}) REQUIRE m.year_month IS NOT NULL",
            f"CREATE CONSTRAINT FOR (m:{local_month_node_label}) REQUIRE m.year_month IS UNIQUE"
        ]
        week_constraint_queries = [
            f"CREATE CONSTRAINT FOR (w:{week_node_label}) REQUIRE w.year_iso_week IS NOT NULL",
            f"CREATE CONSTRAINT FOR (w:{week_node_label}) REQUIRE w.year_iso_week IS UNIQUE"
        ]
        local_date_constraint_queries = [
            f"CREATE CONSTRAINT FOR (d:{local_date_node_label}) REQUIRE d.date IS NOT NULL",
            f"CREATE CONSTRAINT FOR (d:{local_date_node_label}) REQUIRE d.date IS UNIQUE"
        ]
        local_time_chunk_constraint_queries = [
            f"CREATE CONSTRAINT FOR (t:{local_time_chunk_node_label}) REQUIRE t.time_chunk_start IS NOT NULL",
            f"CREATE CONSTRAINT FOR (t:{local_time_chunk_node_label}) REQUIRE t.time_chunk_start IS UNIQUE"
        ]
        joined_queries = local_year_constraint_queries + local_month_constraint_queries + week_constraint_queries + local_date_constraint_queries + local_time_chunk_constraint_queries
        for query in  joined_queries:
            logging.query('Running calendar node constraint query: ' + query)
            tx.run(query)
    return True

# %% [markdown]
# #### Functions to create local calendar nodes and relationships

# %%
# Create a local calendar
def create_local_calendar_node(session, labels, label, properties, data_dir=None):
    node_labels_accessor = get_labels_accessor(labels)[1]
    local_calendar_label = node_labels_accessor.get('local_calendar_node_label')
    local_year_label = node_labels_accessor.get('local_year_node_label')
    local_month_label = node_labels_accessor.get('local_month_node_label')
    local_week_label = node_labels_accessor.get('local_week_node_label')
    local_date_label = node_labels_accessor.get('local_date_node_label')
    local_time_chunk_label = node_labels_accessor.get('local_time_chunk_node_label')
    if label == local_calendar_label:
        logging.app(f"Creating local calendar node with label: {label}")
        logging.app(f"Properties: {str(properties)}")
        prepared_properties = prepare_local_calendar_node(properties[0], properties[1], properties[2], properties[3], data_dir)
        node = neo.create_node(session, label, prepared_properties, returns=True)
    elif label == local_year_label:
        prepared_properties = prepare_local_year_node(properties[0], properties[1], properties[2], data_dir)
        node = neo.create_node(session, label, prepared_properties, returns=True)
    elif label == local_month_label:
        prepared_properties = prepare_local_month_node(properties[0], properties[1], properties[2], properties[3], data_dir)
        node = neo.create_node(session, label, prepared_properties, returns=True)
    elif label == local_week_label:
        prepared_properties = prepare_local_week_node(properties[0], properties[1], properties[2], data_dir)
        node = neo.create_node(session, label, prepared_properties, returns=True)
    elif label == local_date_label:
        prepared_properties = prepare_local_date_node(properties[0], properties[1], properties[2], data_dir)
        node = neo.create_node(session, label, prepared_properties, returns=True)
    elif label == local_time_chunk_label:
        prepared_properties = prepare_local_time_chunk_node(properties[0], properties[1], properties[2], properties[3], data_dir)
        node = neo.create_node(session, label, prepared_properties, returns=True)
    else:
        logging.error(f'Cannot create node with label {label} because label not found in local calendar labels.')
        return ValueError("Create node error.")
    return node

# Create relationships
def create_local_calendar_relationship(session, start_node, end_node, label, local_calendar_labels, constraints=True, properties=None):
    try:
        start_label = next(iter(start_node.labels), None)
        end_label = next(iter(end_node.labels), None)
    except:
        logging.error(f"start_node and end_node must be nodes. Got {start_node} and {end_node} instead.")
        return ValueError("Create relationship error.")
    if constraints:
        allowed_calendar_relationship_constraints = create_allowed_calendar_relationship_constraints(local_calendar_labels)
        allowed = any(
            start == start_label
            and end == end_label
            and label in relationships
            for (
                start,
                end,
            ), relationships in allowed_calendar_relationship_constraints.items()
        )
        if allowed:
            logging.info(f"Creating local calendar relationship with constraints: {label} between {start_label} and {end_label}")
            return neo.create_relationship(
                session, start_node, end_node, label, properties, returns=True
            )
        else:
            logging.error(f"Attempted to create disallowed relationship '{label}' between '{start_label}' and '{end_label}'")
            return ValueError("Create relationship error.")
    else:
        logging.warning("Creating local calendar relationship without constraints")
        return neo.create_relationship(
            session, start_node, end_node, label, properties, returns=True
        )

def get_local_calendar_labels(local_calendar_labels):
    node_labels_accessor = get_calendar_labels_accessor(local_calendar_labels)[1]
    hierarchy_labels_accessor = get_calendar_labels_accessor(local_calendar_labels)[3]
    sequence_label_accessor = get_calendar_labels_accessor(local_calendar_labels)[4] # Not implemented yet
    # Node labels
    local_calendar_node_label = node_labels_accessor.get('local_calendar_node_label')
    local_year_node_label = node_labels_accessor.get('local_year_node_label')
    local_month_node_label = node_labels_accessor.get('local_month_node_label')
    local_week_node_label = node_labels_accessor.get('local_week_node_label')
    local_date_node_label = node_labels_accessor.get('local_date_node_label')
    local_time_chunk_node_label = node_labels_accessor.get('local_time_chunk_node_label')
    # Hierarchy labels
    contains_many_hierarchy_label = hierarchy_labels_accessor.get('contains_many_hierarchy_label')
    contains_set_hierarchy_label = hierarchy_labels_accessor.get('contains_set_hierarchy_label')
    contains_single_hierarchy_label = hierarchy_labels_accessor.get('contains_single') # Not implemented yet
    return local_calendar_node_label, local_year_node_label, local_month_node_label, local_week_node_label, local_date_node_label, local_time_chunk_node_label, contains_many_hierarchy_label, contains_set_hierarchy_label, contains_single_hierarchy_label

def get_local_calendar_init_options(init_options):
    local_calendar_options = init_options['local_calendar_options']
    local_calendar_name = local_calendar_options.get('local_calendar_name', 'LocalCalendar')
    create_years = local_calendar_options.get('create_year_nodes', True).lower() in ['true', 't', 'yes', 'y']
    create_months = local_calendar_options.get('create_month_nodes', True).lower() in ['true', 't', 'yes', 'y']
    create_weeks = local_calendar_options.get('create_week_nodes', False).lower() in ['true', 't', 'yes', 'y']
    create_dates = local_calendar_options.get('create_date_nodes', True).lower() in ['true', 't', 'yes', 'y']
    create_time_chunks = local_calendar_options.get('create_time_chunk_nodes', False).lower() in ['true', 't', 'yes', 'y']
    create_data_directories = local_calendar_options.get('create_data_directories', False).lower() in ['true', 't', 'yes', 'y']
    create_sequenced_relationships = local_calendar_options.get('create_sequenced_relationships', False).lower() in ['true', 't', 'yes', 'y']
    sequenced_relationships_options = local_calendar_options.get('sequenced_relationships', {})
    if sequenced_relationships_options:
        sequenced_relationships_options = local_calendar_options.get('sequenced_relationships', {})
        create_sequenced_years = sequenced_relationships_options.get('create_sequenced_years', False).lower() in ['true', 't', 'yes', 'y']
        create_sequenced_months = sequenced_relationships_options.get('create_sequenced_months', False).lower() in ['true', 't', 'yes', 'y']
        create_sequenced_dates = sequenced_relationships_options.get('create_sequenced_dates', False).lower() in ['true', 't', 'yes', 'y']
        create_sequenced_weeks = sequenced_relationships_options.get('create_sequenced_weeks', False).lower() in ['true', 't', 'yes', 'y']
        create_sequenced_time_chunks = sequenced_relationships_options.get('create_sequenced_time_chunks', False).lower() in ['true', 't', 'yes', 'y']
    return local_calendar_name, local_calendar_options, create_years, create_months, create_weeks, create_dates, create_time_chunks, create_data_directories, create_sequenced_relationships, create_sequenced_years, create_sequenced_months, create_sequenced_dates, create_sequenced_weeks, create_sequenced_time_chunks

def create_allowed_calendar_relationship_constraints(local_calendar_labels):
    node_labels_accessor = get_calendar_labels_accessor(local_calendar_labels)[1]
    hierarchy_labels_accessor = get_calendar_labels_accessor(local_calendar_labels)[3]
    local_calendar_node_label = node_labels_accessor.get('local_calendar_node_label')
    local_year_node_label = node_labels_accessor.get('local_year_node_label')
    local_month_node_label = node_labels_accessor.get('local_month_node_label')
    local_week_node_label = node_labels_accessor.get('local_week_node_label')
    local_date_node_label = node_labels_accessor.get('local_date_node_label')
    local_time_chunk_node_label = node_labels_accessor.get('local_time_chunk_node_label')
    contains_many_hierarchy_label = hierarchy_labels_accessor.get('contains_many_hierarchy_label')
    contains_set_hierarchy_label = hierarchy_labels_accessor.get('contains_set_hierarchy_label')
    allowed_calendar_relationship_constraints = {
        (local_calendar_node_label, local_year_node_label): contains_set_hierarchy_label,
        (local_calendar_node_label, local_week_node_label): contains_set_hierarchy_label,
        (local_year_node_label, local_month_node_label): contains_set_hierarchy_label,
        (local_month_node_label, local_date_node_label): contains_set_hierarchy_label,
        (local_week_node_label, local_date_node_label): contains_set_hierarchy_label,
        (local_date_node_label, local_time_chunk_node_label): contains_set_hierarchy_label,
    }
    return allowed_calendar_relationship_constraints

# %% [markdown]
# #### Initialise the local calendar

# %%
# Function to create a local calendar
def initialise_local_calendar(session, local_calendar_labels, data, init_options, path=None, local_node=None):
    # Options
    local_calendar_name, local_calendar_options, create_years, create_months, create_weeks, create_dates, create_time_chunks, create_data_directories, create_sequenced_relationships, create_sequenced_years, create_sequenced_months, create_sequenced_dates, create_sequenced_weeks, create_sequenced_time_chunks = get_local_calendar_init_options(init_options)
    # Get labels and properties
    local_calendar_node_label, local_year_node_label, local_month_node_label, local_week_node_label, local_date_node_label, local_time_chunk_node_label, contains_many_hierarchy_label, contains_set_hierarchy_label, contains_single_hierarchy_label = get_calendar_labels_accessor(local_calendar_labels)
    # Verify initialisation options
    if create_data_directories and not path:
        logging.error("Path must be provided to create data directories.")
        return ValueError("Initialisation error.")
    # Verify data
    calendar_start_date = data[0]
    calendar_end_date = data[1]
    if calendar_end_date < calendar_start_date:
        logging.error("End date must be after start date")
        return ValueError("Initialisation error.")
    # Create useful variables
    first_year_in_calendar = calendar_start_date.year
    last_year_in_calendar = calendar_end_date.year
    first_month_in_calendar = calendar_start_date.month
    last_month_in_calendar = calendar_end_date.month
    total_years_in_calendar = (calendar_end_date.year - calendar_start_date.year) + 1
    total_months_in_calendar = (calendar_end_date.year - calendar_start_date.year) * 12 + (calendar_end_date.month - calendar_start_date.month) + 1
    total_days_in_calendar = (calendar_end_date - calendar_start_date).days + 1
    if create_time_chunks:
        time_chunk_minutes = int(local_calendar_options.get('time_chunk_minutes', 60))
        time_chunks_in_day = 24*60 / time_chunk_minutes
        normalised_time_chunk_minutes = 24*60 / time_chunks_in_day
        total_time_chunks_in_calendar = total_days_in_calendar * time_chunks_in_day
    if create_data_directories:
        db_path = path
    # Create the local calendar
    local_calendar = {
        'local_calendar_node': None,
        'local_year_nodes': [],
        'local_month_nodes': [],
        'local_date_nodes': [],
        'local_week_nodes': [],
        'local_time_chunk_nodes': [],
        'hierarchy_local_calendar': [], # The highest order nodes in the hierarchy store the relationships between themselves and the next highest order nodes
        'hierarchy_local_year': [],
        'hierarchy_local_month': [],
        'hierarchy_local_week': [],
        'hierarchy_local_date': [],
        'sequenced_local_year_relationships': [],
        'sequenced_local_month_relationships': [],
        'sequenced_local_week_relationships': [],
        'sequenced_local_date_relationships': [],
        'sequenced_local_time_chunk_relationships': [],
    }
    local_calendar_node_properties = [calendar_start_date, calendar_end_date]
    if create_data_directories:
        local_calendar_path = os.path.join(db_path, local_calendar_name)
        os.makedirs(local_calendar_path, exist_ok=True)
        local_calendar_node_properties.append(local_calendar_path)
    local_calendar_node = create_local_calendar_node(session, local_calendar_labels, local_calendar_node_label, local_calendar_node_properties)
    local_calendar['local_calendar_node'] = local_calendar_node
    logging.prod(f"Created local calendar node for {local_calendar_name} with start date {calendar_start_date} and end date {calendar_end_date}")
    # Connect the local calendar to a local node if one is provided
    if local_node: # Not tested yet
        local_calendar_rel = create_local_calendar_relationship(session, local_node, local_calendar_node, contains_single_hierarchy_label, local_calendar_labels)
        logging.prod(f"Connected local calendar to local node: {local_node}")
    # Logic to create years, months, dates, weeks, and time chunks (and periods for planner)
    y = 1
    m = 1
    w = 1
    d = 1
    t = 1
    # Create a year node for every year in the calendar, and a month node for every month in the year, and a date node for every date in the month if initialisation options are set
    for year in range(first_year_in_calendar, last_year_in_calendar + 1):
        if create_years:
            year_properties = [year, y]
            if create_data_directories:
                year_path = os.path.join(local_calendar_path, "cal", str(year))
                logging.app(f"Creating data directory for year {y} at {year_path}")
                os.makedirs(year_path, exist_ok=True)
                year_properties.append(year_path)
            year_node = create_local_calendar_node(session, local_calendar_labels, local_year_node_label, year_properties)
            year_rel = create_local_calendar_relationship(session, local_calendar_node, year_node, contains_many_hierarchy_label, local_calendar_labels)
            local_calendar['local_year_nodes'].append(year_node)
            local_calendar['hierarchy_local_calendar'].append(year_rel)
            logging.prod(f"Created node and relationship for year {y} at {year_path} within local calendar")
        # Create a month node for every month in the calendar
        if year == first_year_in_calendar:
            first_month = first_month_in_calendar
        else:
            first_month = 1
        if year == last_year_in_calendar:
            last_month = last_month_in_calendar
        else:
            last_month = 12
        for month in range(first_month, last_month + 1):
            if create_months:
                month_properties = [year, month, m]
                if create_data_directories:
                    month_path = os.path.join(local_calendar_path, str(year), str(month))
                    logging.app(f"Creating data directory for month {m} at {month_path}")
                    os.makedirs(month_path, exist_ok=True)
                    month_properties.append(month_path)
                month_node = create_local_calendar_node(session, local_calendar_labels, local_month_node_label, month_properties)
                if create_years:
                    month_rel = create_local_calendar_relationship(session, year_node, month_node, contains_set_hierarchy_label, local_calendar_labels)
                else:
                    month_rel = create_local_calendar_relationship(session, local_calendar_node, month_node, contains_many_hierarchy_label, local_calendar_labels)
                local_calendar['local_month_nodes'].append(month_node)
                local_calendar['hierarchy_local_year'].append(month_rel)
                logging.prod(f"Created node and relationship for month {m} at {month_path} within year {y} in local calendar")
            # Create a date node for every date in the month
            if year == first_year_in_calendar and month == first_month_in_calendar:
                first_day = calendar_start_date.day
            else:
                first_day = 1
            if year == last_year_in_calendar and month == last_month_in_calendar:
                last_day = calendar_end_date.day
            else:
                last_day = 31
                if month in [4, 6, 9, 11]:
                    last_day = 30
                if month == 2:
                    if year % 4 == 0:
                        last_day = 29
                    else:
                        last_day = 28
            for day in range(first_day, last_day + 1):
                date = datetime.date(year, month, day)
                if create_dates:
                    date_properties = [date, d]
                    if create_data_directories:
                        date_path = os.path.join(local_calendar_path, str(year), str(month), str(day))
                        logging.app(f"Creating data directory for date {d} at {date_path}")
                        os.makedirs(date_path, exist_ok=True)
                        date_properties.append(date_path)
                    date_node = create_local_calendar_node(session, local_calendar_labels, local_date_node_label, date_properties)
                    if create_months:
                        date_rel = create_local_calendar_relationship(session, month_node, date_node, contains_set_hierarchy_label, local_calendar_labels)
                        local_calendar['local_date_nodes'].append(date_node)
                        local_calendar['hierarchy_local_month'].append(date_rel)
                    else:
                        local_calendar['local_date_nodes'].append(date_node)
                    logging.prod(f"Created node and relationship for date {d} at {date_path} within month {m} in local calendar")
                # Create a time chunk node for every time chunk in the date
                if create_time_chunks:
                    for t_day in range(int(time_chunks_in_day)):
                        time_chunk_start = datetime.datetime.combine(date, time(hour=int(t_day * normalised_time_chunk_minutes / 60), minute=int((t_day * normalised_time_chunk_minutes) % 60)))
                        time_chunk_properties = [time_chunk_start, normalised_time_chunk_minutes, t]
                        if create_data_directories:
                            time_chunk_path = os.path.join(local_calendar_path, str(year), str(month), str(day), str(t_day))
                            logging.app(f"Creating data directory for time chunk {t} at {time_chunk_path}")
                            os.makedirs(time_chunk_path, exist_ok=True)
                            time_chunk_properties.append(time_chunk_path)
                        time_chunk_node = create_local_calendar_node(session, local_calendar_labels, local_time_chunk_node_label, time_chunk_properties)
                        time_chunk_rel = create_local_calendar_relationship(session, date_node, time_chunk_node, contains_set_hierarchy_label, local_calendar_labels)
                        local_calendar['local_time_chunk_nodes'].append(time_chunk_node)
                        local_calendar['hierarchy_local_date'].append(time_chunk_rel)
                        logging.prod(f"Created node and relationship for time chunk {t} at {time_chunk_path} within date {d} in local calendar")
                        t_day += 1
                        t += 1
                d += 1
            m += 1
        y += 1
    # Create week nodes and relationships if create_weeks is set to True
    if create_weeks:
        number_of_days_in_first_week = 7 - calendar_start_date.weekday()
        number_of_days_in_last_week = calendar_end_date.weekday() + 1
        number_of_weeks_in_calendar = (total_days_in_calendar - number_of_days_in_first_week - number_of_days_in_last_week) / 7
        for i in range(int(number_of_weeks_in_calendar) + 2):
            if i == 0:
                week_start_date = calendar_start_date
            elif i == int(number_of_weeks_in_calendar) + 1:
                week_start_date = calendar_end_date - timedelta(days=number_of_days_in_last_week - 1)
            else:
                week_start_date = calendar_start_date + timedelta(days=number_of_days_in_first_week + (i-1)*7)
            week_properties = [week_start_date, w]
            if create_data_directories:
                week_path = os.path.join(local_calendar_path, 'weeks', str(week_start_date.year), str(week_start_date.isocalendar()[1]))
                os.makedirs(week_path, exist_ok=True)
                week_properties.append(week_path)
            week_node = create_local_calendar_node(session, local_calendar_labels, local_week_node_label, week_properties)
            week_rel = create_local_calendar_relationship(session, local_calendar_node, week_node, contains_many_hierarchy_label, local_calendar_labels)
            local_calendar['local_week_nodes'].append(week_node)
            local_calendar['hierarchy_local_calendar'].append(week_rel)
            logging.prod(f"Created week node {w} for week beginning {week_start_date}")
            w += 1
        for date in local_calendar['local_date_nodes']:
            date_iso_week = '{}-{}'.format(date['date'].year, date['date'].isocalendar()[1])
            week_node = [week for week in local_calendar['local_date_nodes'] if week['year_iso_week'] == date_iso_week][0]
            week_rel = create_local_calendar_relationship(session, week_node, date, contains_set_hierarchy_label, local_calendar_labels)
            local_calendar['hierarchy_local_week'].append(week_rel)
            logging.prod(f"Connected date {date['date']} to week {week_node['year_iso_week']}")
    # Create sequenced relationships
    if create_sequenced_relationships:
        if create_sequenced_years:
            sequence_local_year_relationships = sequence_list_of_nodes(session, local_calendar['local_year_nodes'])
            local_calendar['sequenced_local_year_relationships'].append(sequence_local_year_relationships)
            logging.prod("Created sequenced year relationships")
        if create_sequenced_months:
            sequence_local_month_relationships = sequence_list_of_nodes(session, local_calendar['local_month_nodes'])
            local_calendar['sequenced_local_month_relationships'].append(sequence_local_month_relationships)
            logging.prod("Created sequenced month relationships")
        if create_sequenced_weeks:
            sequence_local_week_relationships = sequence_list_of_nodes(session, local_calendar['local_week_nodes'])
            local_calendar['sequenced_local_week_relationships'].append(sequence_local_week_relationships)
            logging.prod("Created sequenced week relationships")
        if create_sequenced_dates:
            sequence_local_date_relationships = sequence_list_of_nodes(session, local_calendar['local_date_nodes'])
            local_calendar['sequenced_local_date_relationships'].append(sequence_local_date_relationships)
            logging.prod("Created sequenced date relationships")
        if create_sequenced_time_chunks:
            sequence_local_time_chunk_relationships = sequence_list_of_nodes(session, local_calendar['local_time_chunk_nodes'])
            local_calendar['sequenced_local_time_chunk_relationships'].append(sequence_local_time_chunk_relationships)
            logging.prod("Created sequenced time chunk relationships")
    # Return the local calendar
    return local_calendar

# %% [markdown]
# ### Local planner

# %% [markdown]
# #### Local planner KevlarAI enhanced node and relationships preparations

# %%
# Functions to prepare properties
def prepare_local_planner_node(label, data, data_dir=None): # TODO: Implement AI planner node properties (needs to match to code below for now)
    if label == 'LocalPlanner':
        properties = {
            'planner_name': data
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'AcademicYear':
        properties = {
            'first_day_of_academic_year': data[0],
            'last_day_of_academic_year': data[1]
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'AcademicTerm':
        properties = {
            'term_name': data[0],
            'start_date': data[1],
            'end_date': data[2]
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'TermBreak':
        properties = {
            'break_name': data[0],
            'start_date': data[1],
            'end_date': data[2]
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'AcademicWeek':
        properties = {
            'week': data[0],
            'type': data[1]
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'HolidayWeek':
        properties = {
            'week': data[0]
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'AcademicDate':
        properties = {
            'date': data[0],
            'type': data[1],
            'notes': data[2]
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'HolidayDay':
        properties = {
            'date': data[0]
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'AcademicPeriod':
        properties = {
            'start': data[0],
            'type': data[1],
            'duration_minutes': data[2]
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'AcademicTimeChunk':
        properties = {
            'start': data[0],
            'duration_minutes': data[1]
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    else:
        return ValueError("Invalid type of local calendar node")

def prepare_local_academic_year_node(start, end, data_dir=None): # TODO: Implement AI planner year node properties (needs to match to code below for now)
    properties = {
        'academic_year': f'{start}-{end}'
        }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_academic_term_node(term_name, start_date, end_date, data_dir=None): # TODO: Implement AI planner term node properties (needs to match to code below for now)
    properties = {
        'term_name': term_name,
        'start_date': start_date,
        'end_date': end_date
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_term_break_node(break_name, start_date, end_date, data_dir=None): # TODO: Implement AI planner term break node properties (needs to match to code below for now)
    properties = {
        'break_name': break_name,
        'start_date': start_date,
        'end_date': end_date
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_academic_week_node(academic_week, start_date, end_date, notes, week_type, data_dir=None): # TODO: Implement AI planner week node properties (needs to match to code below for now)
    properties = {
        'academic_week': academic_week,
        'start_date': start_date,
        'end_date': end_date,
        'type': week_type,
        'notes': notes
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_holiday_week_node(week, data_dir=None): # TODO: Implement AI planner holiday week node properties (needs to match to code below for now)
    properties = {
        'holiday_week': week
    }
    return properties

def prepare_local_academic_date_node(date, day_type, week_type=None, data_dir=None): # TODO: Implement AI planner date node properties (needs to match to code below for now)
    properties = {
        'date': date,
        'type': day_type
    }
    if week_type:
        properties['week_type'] = week_type
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_academic_day_node(date, data_dir=None): # TODO: Implement AI planner day node properties (needs to match to code below for now)
    properties = {
        'day': date
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_holiday_day_node(date, data_dir=None): # TODO: Implement AI planner holiday day node properties (needs to match to code below for now)
    properties = {
        'holiday_day': date
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_academic_staff_day_node(date, data_dir=None): # TODO: Implement AI planner staff day node properties (needs to match to code below for now)
    properties = {
        'staff_day': date
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_academic_off_timetable_node(date, data_dir=None): # TODO: Implement AI planner off timetable node properties (needs to match to code below for now)
    properties = {
        'off_timetable': date
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_academic_period_node(start, minutes, period, period_type, week_type, data_dir=None): # TODO: Implement AI planner period node properties (needs to match to code below for now)
    properties = {
        'start': start,
        'duration_minutes': minutes,
        'period': period,
        'type': period_type,
        'week_type': week_type
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

# TODO: Add granular period node labels and properties

def prepare_local_academic_time_chunk_node(start, minutes, data_dir=None): # TODO: Implement AI planner time chunk node properties (needs to match to code below for now)
    properties = {
        'time_chunk_start': start,
        'time_chunk_duration_minutes': minutes
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties


# %% [markdown]
# #### Get planner labels, properties, relationships and initialisation options

# %%
def get_local_planner_node_and_relationship_labels_using_accessor(local_planner_labels_file):
    planner_node_labels_accessor, hierarchy_labels_accessor = [get_planner_labels_accessor(local_planner_labels_file)[i] for i in [1, 3]] # TODO: Add more labels
    local_planner_node_and_relationship_labels = {
        'local_planner_node_label': planner_node_labels_accessor.get('local_planner_node_label'),
        'local_academic_year_node_label': planner_node_labels_accessor.get('local_academic_year_node_label'),
        'local_academic_term_node_label': planner_node_labels_accessor.get('local_academic_term_node_label'),
        'local_academic_term_break_node_label': planner_node_labels_accessor.get('local_academic_term_break_node_label'),
        'local_academic_week_node_label': planner_node_labels_accessor.get('local_academic_week_node_label'),
        'local_academic_week_holiday_node_label': planner_node_labels_accessor.get('local_academic_week_holiday_node_label'),
        'local_academic_date_node_label': planner_node_labels_accessor.get('local_academic_date_node_label'),
        'local_academic_day_node_label': planner_node_labels_accessor.get('local_academic_day_node_label'),
        'local_academic_holiday_day_node_label': planner_node_labels_accessor.get('local_academic_holiday_day_node_label'),
        'local_academic_staff_day_node_label': planner_node_labels_accessor.get('local_academic_staff_day_node_label'),
        'local_academic_off_timetable_node_label': planner_node_labels_accessor.get('local_academic_off_timetable_node_label'),
        'local_academic_period_timetabled_lesson_node_label': planner_node_labels_accessor.get('local_academic_period_timetabled_lesson_node_label'),
        'local_academic_period_registration_node_label': planner_node_labels_accessor.get('local_academic_period_registration_node_label'),
        'local_academic_period_break_node_label': planner_node_labels_accessor.get('local_academic_period_break_node_label'),
        'local_academic_period_meeting_node_label': planner_node_labels_accessor.get('local_academic_period_meeting_node_label'),
        'local_academic_period_task_node_label': planner_node_labels_accessor.get('local_academic_period_task_node_label'),
        'local_academic_period_node_label': planner_node_labels_accessor.get('local_academic_period_node_label'),
        'local_academic_time_chunk_node_label': planner_node_labels_accessor.get('local_academic_time_chunk_node_label'),
        'contains_many_hierarchy_label': planner_node_labels_accessor.get('contains_many_hierarchy_label'),
        'contains_set_hierarchy_label': planner_node_labels_accessor.get('contains_set_hierarchy_label'),
        'contains_single_label': planner_node_labels_accessor.get('contains_single')
    }
    return local_planner_node_and_relationship_labels

def get_local_planner_init_options(init_options):
    local_planner_options = init_options['local_planner_options'] # TODO: Check if this is correct
    local_planner_name = local_planner_options.get('local_planner_name', 'LocalPlanner')
    def str_to_bool(s, default=False):
        return s.lower() in ['true', 't', 'yes', 'y'] if s is not None else default
    options_keys = [
        'create_academic_year_nodes', 'create_academic_term_nodes', 'create_academic_term_break_nodes',
        'create_academic_week_nodes', 'create_academic_week_holiday_nodes', 'create_academic_day_nodes',
        'create_academic_holiday_day_nodes', 'create_academic_staff_day_nodes', 'create_academic_off_timetable_nodes',
        'create_academic_period_timetabled_lesson_nodes', 'create_academic_period_registration_nodes',
        'create_academic_period_break_nodes', 'create_academic_period_meeting_nodes', 'create_academic_period_task_nodes',
        'create_academic_time_chunk_nodes', 'create_sequenced_relationships', 'create_data_directories'
    ]
    options = {k: str_to_bool(local_planner_options.get(k), k not in ['create_academic_term_break_nodes', 'create_academic_week_nodes', 'create_academic_time_chunk_nodes', 'create_data_directories', 'create_sequenced_relationships']) for k in options_keys}
    sequenced_relationships_options = local_planner_options.get('sequenced_relationships', {})
    if sequenced_relationships_options:
        sequenced_options_keys = [
            'create_sequenced_academic_years', 'create_sequenced_academic_terms_with_breaks',
            'create_sequenced_academic_terms_without_breaks', 'create_sequenced_academic_weeks_with_holidays',
            'create_sequenced_academic_weeks_without_holidays', 'create_sequenced_academic_dates_with_holidays',
            'create_sequenced_academic_dates_without_holidays', 'create_sequenced_academic_periods_for_year',
            'create_sequenced_academic_periods_for_day', 'create_sequenced_academic_time_chunks_for_year',
            'create_sequenced_academic_time_chunks_for_day'
        ]
        sequenced_options = {k: str_to_bool(sequenced_relationships_options.get(k)) for k in sequenced_options_keys}
        local_planner_init_options = {**options, **sequenced_options, 'local_planner_name': local_planner_name, 'local_planner_options': local_planner_options}
    else:
        local_planner_init_options = {**options, 'local_planner_name': local_planner_name, 'local_planner_options': local_planner_options}
    return local_planner_init_options


# %% [markdown]
# #### Create planner constraints

# %%
# Create the constraints
def create_local_planner_node_constraints_using_file(session, local_planner_labels_file):
    local_planner_node_and_relationship_labels = get_local_planner_node_and_relationship_labels_using_accessor(local_planner_labels_file)
    local_planner_node_label = local_planner_node_and_relationship_labels.get('local_planner_node_label')
    local_academic_year_node_label = local_planner_node_and_relationship_labels.get('local_academic_year_node_label')
    local_academic_term_node_label = local_planner_node_and_relationship_labels.get('local_academic_term_node_label')
    local_academic_term_break_node_label = local_planner_node_and_relationship_labels.get('local_academic_term_break_node_label')
    local_academic_week_node_label = local_planner_node_and_relationship_labels.get('local_academic_week_node_label')
    local_academic_week_holiday_node_label = local_planner_node_and_relationship_labels.get('local_academic_week_holiday_node_label')
    local_academic_date_node_label = local_planner_node_and_relationship_labels.get('local_academic_date_node_label')
    local_academic_day_node_label = local_planner_node_and_relationship_labels.get('local_academic_day_node_label')
    local_academic_holiday_day_node_label = local_planner_node_and_relationship_labels.get('local_academic_holiday_day_node_label')
    local_academic_staff_day_node_label = local_planner_node_and_relationship_labels.get('local_academic_staff_day_node_label')
    local_academic_off_timetable_node_label = local_planner_node_and_relationship_labels.get('local_academic_off_timetable_node_label')
    local_academic_period_timetabled_lesson_node_label = local_planner_node_and_relationship_labels.get('local_academic_period_timetabled_lesson_node_label')
    local_academic_period_registration_node_label = local_planner_node_and_relationship_labels.get('local_academic_period_registration_node_label')
    local_academic_period_break_node_label = local_planner_node_and_relationship_labels.get('local_academic_period_break_node_label')
    local_academic_period_meeting_node_label = local_planner_node_and_relationship_labels.get('local_academic_period_meeting_node_label')
    local_academic_period_task_node_label = local_planner_node_and_relationship_labels.get('local_academic_period_task_node_label')
    local_academic_period_node_label = local_planner_node_and_relationship_labels.get('local_academic_period_node_label')
    local_academic_time_chunk_node_label = local_planner_node_and_relationship_labels.get('local_academic_time_chunk_node_label')
    with session.begin_transaction() as tx:
        local_planner_constraint_queries = None
        local_academic_year_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (y:{local_academic_year_node_label}) REQUIRE y.academic_year IS NOT NULL",
            f"CREATE CONSTRAINT FOR (y:{local_academic_year_node_label}) REQUIRE y.academic_year IS UNIQUE"
        ]
        local_academic_term_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (t:{local_academic_term_node_label}) REQUIRE t.term_name IS NOT NULL",
            f"CREATE CONSTRAINT FOR (t:{local_academic_term_node_label}) REQUIRE t.start_date IS NOT NULL",
            f"CREATE CONSTRAINT FOR (t:{local_academic_term_node_label}) REQUIRE t.end_date IS NOT NULL",
            f"CREATE CONSTRAINT FOR (t:{local_academic_term_node_label}) REQUIRE t.term_name IS UNIQUE"
        ]
        local_academic_term_break_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (b:{local_academic_term_break_node_label}) REQUIRE b.break_name IS NOT NULL",
            f"CREATE CONSTRAINT FOR (b:{local_academic_term_break_node_label}) REQUIRE b.start_date IS NOT NULL",
            f"CREATE CONSTRAINT FOR (b:{local_academic_term_break_node_label}) REQUIRE b.end_date IS NOT NULL",
            f"CREATE CONSTRAINT FOR (b:{local_academic_term_break_node_label}) REQUIRE b.break_name IS UNIQUE"
        ]
        local_academic_week_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (w:{local_academic_week_node_label}) REQUIRE w.academic_week IS NOT NULL",
            f"CREATE CONSTRAINT FOR (w:{local_academic_week_node_label}) REQUIRE w.type IS NOT NULL",
            f"CREATE CONSTRAINT FOR (w:{local_academic_week_node_label}) REQUIRE w.week IS UNIQUE"
        ]
        local_academic_week_holiday_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (h:{local_academic_week_holiday_node_label}) REQUIRE h.holiday_week IS NOT NULL",
            f"CREATE CONSTRAINT FOR (h:{local_academic_week_holiday_node_label}) REQUIRE h.holiday_week IS UNIQUE"
        ]
        local_academic_date_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (d:{local_academic_date_node_label}) REQUIRE d.date IS NOT NULL",
            f"CREATE CONSTRAINT FOR (d:{local_academic_date_node_label}) REQUIRE d.type IS NOT NULL",
            f"CREATE CONSTRAINT FOR (d:{local_academic_date_node_label}) REQUIRE d.date IS UNIQUE"
        ]
        local_academic_day_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (dy:{local_academic_day_node_label}) REQUIRE dy.date IS NOT NULL",
            f"CREATE CONSTRAINT FOR (dy:{local_academic_day_node_label}) REQUIRE dy.date IS UNIQUE"
        ]
        local_academic_holiday_day_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (h:{local_academic_holiday_day_node_label}) REQUIRE h.date IS NOT NULL",
            f"CREATE CONSTRAINT FOR (h:{local_academic_holiday_day_node_label}) REQUIRE h.date IS UNIQUE"
        ]
        local_academic_staff_day_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (s:{local_academic_staff_day_node_label}) REQUIRE s.date IS NOT NULL",
            f"CREATE CONSTRAINT FOR (s:{local_academic_staff_day_node_label}) REQUIRE s.date IS UNIQUE"
        ]
        local_academic_off_timetable_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (o:{local_academic_off_timetable_node_label}) REQUIRE o.date IS NOT NULL",
            f"CREATE CONSTRAINT FOR (o:{local_academic_off_timetable_node_label}) REQUIRE o.date IS UNIQUE"
        ]
        local_academic_period_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (p:{local_academic_period_node_label}) REQUIRE p.start IS NOT NULL",
            f"CREATE CONSTRAINT FOR (p:{local_academic_period_node_label}) REQUIRE p.duration_minutes IS NOT NULL",
            f"CREATE CONSTRAINT FOR (p:{local_academic_period_node_label}) REQUIRE p.type IS NOT NULL",
            f"CREATE CONSTRAINT FOR (p:{local_academic_period_node_label}) REQUIRE p.start IS UNIQUE"
        ]
        local_academic_period_timetabled_lesson_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (l:{local_academic_period_timetabled_lesson_node_label}) REQUIRE l.timetabled_lesson IS NOT NULL",
            f"CREATE CONSTRAINT FOR (l:{local_academic_period_timetabled_lesson_node_label}) REQUIRE l.timetabled_lesson IS UNIQUE"
        ]
        local_academic_period_registration_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (r:{local_academic_period_registration_node_label}) REQUIRE r.registration IS NOT NULL",
            f"CREATE CONSTRAINT FOR (r:{local_academic_period_registration_node_label}) REQUIRE r.registration IS UNIQUE"
        ]
        local_academic_period_break_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (b:{local_academic_period_break_node_label}) REQUIRE b.period_break IS NOT NULL",
            f"CREATE CONSTRAINT FOR (b:{local_academic_period_break_node_label}) REQUIRE b.period_break IS UNIQUE"
        ]
        local_academic_period_meeting_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (m:{local_academic_period_meeting_node_label}) REQUIRE m.meeting IS NOT NULL",
            f"CREATE CONSTRAINT FOR (m:{local_academic_period_meeting_node_label}) REQUIRE m.meeting IS UNIQUE"
        ]
        local_academic_period_task_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (t:{local_academic_period_task_node_label}) REQUIRE t.task IS NOT NULL",
            f"CREATE CONSTRAINT FOR (t:{local_academic_period_task_node_label}) REQUIRE t.task IS UNIQUE"
        ]
        local_academic_time_chunk_constraint_queries  = [
            f"CREATE CONSTRAINT FOR (t:{local_academic_time_chunk_node_label}) REQUIRE t.time_chunk_start IS NOT NULL",
            f"CREATE CONSTRAINT FOR (t:{local_academic_time_chunk_node_label}) REQUIRE t.time_chunk_duration_minutes IS NOT NULL",
            f"CREATE CONSTRAINT FOR (t:{local_academic_time_chunk_node_label}) REQUIRE t.time_chunk_start IS UNIQUE"
        ]
        joined_queries = local_academic_year_constraint_queries + local_academic_term_constraint_queries + local_academic_term_break_constraint_queries + local_academic_week_constraint_queries + local_academic_week_holiday_constraint_queries + local_academic_date_constraint_queries + local_academic_day_constraint_queries + local_academic_holiday_day_constraint_queries + local_academic_staff_day_constraint_queries + local_academic_off_timetable_constraint_queries + local_academic_period_timetabled_lesson_constraint_queries + local_academic_period_registration_constraint_queries + local_academic_period_break_constraint_queries + local_academic_period_meeting_constraint_queries + local_academic_period_task_constraint_queries + local_academic_period_constraint_queries + local_academic_time_chunk_constraint_queries
        for query in joined_queries:
            logging.query(f'Running planner node constraint query: {query}')
            tx.run(query)
    return True

def create_allowed_planner_relationship_constraints_using_labels(local_planner_node_and_relationship_labels):
    packed_labels = local_planner_node_and_relationship_labels
    label_keys = ['local_planner_node_label', 'local_academic_year_node_label', 'local_academic_term_node_label', 'local_academic_term_break_node_label', 'local_academic_week_node_label', 'local_academic_week_holiday_node_label', 'local_academic_date_node_label', 'local_academic_day_node_label', 'local_academic_holiday_day_node_label', 'local_academic_staff_day_node_label', 'local_academic_off_timetable_node_label', 'local_academic_period_node_label','local_academic_period_timetabled_lesson_node_label', 'local_academic_period_registration_node_label','local_academic_period_break_node_label', 'local_academic_period_meeting_node_label', 'local_academic_period_task_node_label', 'local_academic_time_chunk_node_label', 'contains_many_hierarchy_label', 'contains_set_hierarchy_label', 'contains_single_hierarchy_label']
    labels = {key: packed_labels.get(key) for key in label_keys}
    allowed_planner_relationship_constraints_dict_from_labels = {
    (labels['local_planner_node_label'], labels['local_academic_year_node_label']): labels['contains_many_hierarchy_label'],
    (labels['local_academic_year_node_label'], labels['local_academic_term_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_year_node_label'], labels['local_academic_term_break_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_year_node_label'], labels['local_academic_week_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_year_node_label'], labels['local_academic_week_holiday_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_year_node_label'], labels['local_academic_date_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_term_node_label'], labels['local_academic_week_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_term_break_node_label'], labels['local_academic_week_node_label']): labels['contains_set_hierarchy_label'],    
    (labels['local_academic_term_break_node_label'], labels['local_academic_week_holiday_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_week_node_label'], labels['local_academic_date_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_week_node_label'], labels['local_academic_day_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_week_node_label'], labels['local_academic_staff_day_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_week_node_label'], labels['local_academic_off_timetable_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_week_holiday_node_label'], labels['local_academic_date_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_week_holiday_node_label'], labels['local_academic_holiday_day_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_date_node_label'], labels['local_academic_period_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_date_node_label'], labels['local_academic_period_timetabled_lesson_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_date_node_label'], labels['local_academic_period_registration_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_date_node_label'], labels['local_academic_period_break_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_date_node_label'], labels['local_academic_period_meeting_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_date_node_label'], labels['local_academic_period_task_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_academic_period_node_label'], labels['local_academic_time_chunk_node_label']): labels['contains_set_hierarchy_label']
    }
    return allowed_planner_relationship_constraints_dict_from_labels

# %% [markdown]
# #### Functions to create local planner nodes and relationships

# %%
# Create a local planner
def create_local_planner_node_using_labels(session, local_planner_node_and_relationship_labels, label, properties, path=None):
    labels = local_planner_node_and_relationship_labels
    if label == labels.get('local_planner_node_label'): # Handle local planner node at initialisation
        logging.debug(f"Creating local planner node with properties: {properties}")
        prepared_properties = prepare_local_planner_node(label, properties, path) # name (start-end)
        
    elif label == labels.get('local_academic_year_node_label'):
        prepared_properties = prepare_local_academic_year_node(properties[0], properties[1]) # start, end
        if properties[2]:
            prepared_properties['data_dir'] = properties[2]
            
    elif label == labels.get('local_academic_term_node_label'):
        prepared_properties = prepare_local_academic_term_node(properties['term_name'], properties['start_date'], properties['end_date'])
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_term_break_node_label'):
        prepared_properties = prepare_local_term_break_node(properties['term_break_name'], properties['start_date'], properties['end_date'])
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_week_node_label'):
        prepared_properties = prepare_local_academic_week_node(properties['week'], properties['start_date'], properties['end_date'], properties['notes'], properties['type'])
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_week_holiday_node_label'):
        prepared_properties = prepare_local_holiday_week_node(properties[0]) # date
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_date_node_label'):
        prepared_properties = prepare_local_academic_date_node(properties['date'], properties['type'], properties['notes'])
        if properties.get('week_type'):
            prepared_properties['week_type'] = properties['week_type']
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_day_node_label'):
        prepared_properties = prepare_local_academic_day_node(properties[0]) # date
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_holiday_day_node_label'):
        prepared_properties = prepare_local_holiday_day_node(properties[0]) # date
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_staff_day_node_label'):
        prepared_properties = prepare_local_academic_staff_day_node(properties[0]) # date
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_off_timetable_node_label'): # TODO: Implement days off timetable and periods off timetable, possibly alternate labels for periods, days, weeks, even time chunks (for ultra granular control over actions and events)
        prepared_properties = prepare_local_academic_off_timetable_node(properties[0]) # date
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_period_node_label'):
        prepared_properties = prepare_local_academic_period_node(properties['start'], properties['minutes'], properties['period'], properties['type'], properties['week_type'])
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_period_timetabled_lesson_node_label'):
        prepared_properties = prepare_local_academic_timetabled_lesson_node(properties[0], properties[1]) # start, minutes
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
            
    elif label == labels.get('local_academic_period_registration_node_label'): # TODO: Implement
        prepared_properties = prepare_local_academic_registration_node(properties[0], properties[1]) # start, minutes
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
    elif label == labels.get('local_academic_period_break_node_label'): # TODO: Implement
        prepared_properties = prepare_local_academic_break_node(properties[0], properties[1], properties[2]) # start, minutes, break_type
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
    elif label == labels.get('local_academic_period_meeting_node_label'): # TODO: Implement
        prepared_properties = prepare_local_academic_meeting_node(properties[0], properties[1]) # start, minutes
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
    elif label == labels.get('local_academic_period_task_node_label'): # TODO: Implement
        prepared_properties = prepare_local_academic_period_task_node(properties[0], properties[1], properties[2]) # start, minutes, task_type
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
    elif label == labels.get('local_academic_time_chunk_node_label'):
        prepared_properties = prepare_local_academic_time_chunk_node(properties['start'], properties['minutes'])
        if properties.get('data_dir'):
            prepared_properties['data_dir'] = properties['data_dir']
    else:
        logging.error(f'Cannot create node with label {label} because label not found in local planner labels.')
        return ValueError("Create node error.")
    node = neo.create_node(session, label, prepared_properties, returns=True)
    return node

# Create relationships
def create_local_planner_relationship(session, start_node, end_node, label, local_planner_labels, constraints=True, properties=None):
    try:
        start_label = next(iter(start_node.labels), None)
        end_label = next(iter(end_node.labels), None)
    except Exception:
        logging.error(f"start_node and end_node must be nodes. Got {start_node} and {end_node} instead.")
        return ValueError("Create relationship error.")
    if constraints:
        allowed_planner_relationship_constraints = create_allowed_planner_relationship_constraints_using_labels(local_planner_labels)
        allowed = any(
            start == start_label
            and end == end_label
            and label in relationships
            for (
                start,
                end,
            ), relationships in allowed_planner_relationship_constraints.items()
        )
        if allowed:
            logging.info(f"Creating local planner relationship with constraints: {label} between {start_label} and {end_label}")
            return neo.create_relationship(
                session, start_node, end_node, label, properties, returns=True
            )
        else:
            logging.error(f"Attempted to create disallowed relationship '{label}' between '{start_label}' and '{end_label}'")
            return ValueError("Create relationship error.")
    else:
        logging.warning("Creating local planner relationship without constraints")
        return neo.create_relationship(
            session, start_node, end_node, label, properties, returns=True
        )

# %% [markdown]
# #### Create intermediate property dictionaries for weeks and days from external data

# %%
def create_weeks_days_dicts(start_year, excel_days_list_of_dicts, excel_weeks_list_of_dicts): # TODO: THIS IS BEING REPEATED BELOW! FIX IT OR REMOVE IT (Update: This may be useful)
    start_date = date(start_year, 1, 1)
    end_date = date(start_year + 1, 12, 31)
    weeks_dict = {}
    days_dict = {}
    # Convert days_data and weeks_data into dictionaries for easy lookup (is this necessary?)
    days_data_dict = {pd.to_datetime(d['date']).date(): d for d in excel_days_list_of_dicts}
    weeks_data_dict = {pd.to_datetime(w['start_date']).date(): w for w in excel_weeks_list_of_dicts}
    current_date = start_date
    while current_date <= end_date:
        week_start = current_date - timedelta(days=current_date.weekday())
        week_id = week_start.strftime('%Y-W%W')
        if week_id not in weeks_dict:
            week_data = weeks_data_dict.get(week_start) # Get week data if it exists
            week_type = week_data['type'] if week_data and 'type' in week_data and pd.notna(week_data['type']) else 'undefined'
            week_calendar_agenda = week_data['calendar_agenda'] if week_data and 'calendar_agenda' in week_data and pd.notna(week_data['calendar_agenda']) else ''
            week_agenda_heading = week_data['agenda_heading'] if week_data and 'agenda_heading' in week_data and pd.notna(week_data['agenda_heading']) else ''
            week_agenda_notes = week_data['agenda_notes'] if week_data and 'agenda_notes' in week_data and pd.notna(week_data['agenda_notes']) else ''
            notes = week_calendar_agenda + '\n' + week_agenda_heading + '\n' + week_agenda_notes
            weeks_dict[week_id] = {
                'id': week_id,
                'start_date': week_start,
                'end_date': week_start + timedelta(days=6),
                'type': week_type,
                'notes': notes
            }
        day_data = days_data_dict.get(current_date)
        if current_date.weekday() in [5, 6]:  # Check if it's a weekend
            day_modifier = 'weekend'
        else: # Check if it's a school day or holiday
            day_modifier = day_data['type'] if day_data and 'type' in day_data and pd.notna(day_data['type']) else 'undefined'    
        day_auto_agenda = day_data['auto_agenda'] if day_data and 'auto_agenda' in day_data and pd.notna(day_data['auto_agenda']) else ''
        day_agenda_heading = day_data['agenda_heading'] if day_data and 'agenda_heading' in day_data and pd.notna(day_data['agenda_heading']) else ''
        day_agenda_notes = day_data['agenda_notes'] if day_data and 'agenda_notes' in day_data and pd.notna(day_data['agenda_notes']) else ''
        agenda_notes = day_auto_agenda + '\n' + day_agenda_heading + '\n' + day_agenda_notes
        days_dict[current_date.strftime('%Y-%m-%d')] = {
            'date': current_date,
            'day': current_date.strftime('%A'),
            'type': day_modifier,
            'modifier': week_type,
            'notes': agenda_notes
        }
        current_date += timedelta(days=1)
    return weeks_dict, days_dict

# %% [markdown]
# #### Functions to create term and period nodes from external data and weeks and days data

# %%
def create_academic_term_nodes_dict(session, local_planner_node_and_relationship_labels, local_academic_term_node_label, calendar_df, academic_year_dir=None):
    logging.prod(f"Creating academic term nodes")
    labels = local_planner_node_and_relationship_labels
    term_dates = planner.extract_academic_terms_or_breaks(calendar_df, 'term')
    academic_term_nodes_dict = {}
    # function to convert a string to an int
    for i, term in enumerate(term_dates, 1):
        term_name = term['name'] # just the number
        start_date = term['start_date'].date()
        end_date = term['end_date'].date()
        term_id = f"Term_{i}"
        term_node_properties = {
            'term_name': term_id,
            'start_date': start_date,
            'end_date': end_date
        }
        if academic_year_dir:
            term_node_properties['data_dir'] = os.path.join(academic_year_dir, term_id)
            if not os.path.exists(term_node_properties['data_dir']):
                os.makedirs(term_node_properties['data_dir'])
        node = create_local_planner_node_using_labels(session, labels, local_academic_term_node_label, term_node_properties)
        academic_term_nodes_dict[term_id] = {**term_node_properties, 'node': node}
    return academic_term_nodes_dict

def create_academic_term_break_nodes_dict(session, local_planner_node_and_relationship_labels, local_academic_term_break_node_label, calendar_df, academic_year_dir=None):
    logging.prod(f"Creating academic term break nodes")
    labels = local_planner_node_and_relationship_labels
    term_break_dates = planner.extract_academic_terms_or_breaks(calendar_df, 'break')
    academic_term_break_nodes_dict = {}
    for i, term in enumerate(term_break_dates, 1):
        term_break_name = term['name']
        start_date = term['start_date'].date()
        end_date = term['end_date'].date()
        term_break_id = f"Break_{i}_{term_break_name}"
        term_break_node_properties = {
            'term_break_name': term_break_name,
            'start_date': start_date,
            'end_date': end_date
        }
        if academic_year_dir:
            term_break_node_properties['data_dir'] = os.path.join(academic_year_dir, term_break_id)
            if not os.path.exists(term_break_node_properties['data_dir']):
                os.makedirs(term_break_node_properties['data_dir'])
        node = create_local_planner_node_using_labels(session, labels, local_academic_term_break_node_label, term_break_node_properties)
        academic_term_break_nodes_dict[term_break_id] = {**term_break_node_properties, 'node': node}
    return academic_term_break_nodes_dict

def create_week_nodes_dict(session, local_planner_node_and_relationship_labels, label, academic_year_start, weeks_dict, academic_year_data_dir=None, include_weekends=True):
    logging.prod(f"Creating week nodes for academic year starting from {academic_year_start}")
    labels = local_planner_node_and_relationship_labels
    search_start_date = date(academic_year_start, 1, 1)
    search_end_date = date(academic_year_start + 1, 12, 23)  # Cover the whole academic year
    week_nodes_dict = {}
    weeks_data_dict = weeks_dict  
    current_date = search_start_date
    week_start_date = search_start_date - timedelta(days=search_start_date.weekday())
    while week_start_date <= search_end_date:
        if include_weekends:
            week_end_date = week_start_date + timedelta(days=6)  # Week ends on Sunday
        else:
            week_end_date = week_start_date + timedelta(days=4)  # Week ends on Friday if not including weekends
        week_id = week_start_date.strftime('%Y-W%V')  # Use %V for ISO week number to match your keys format
        if week_id in weeks_data_dict:  # Check if the week's data exists
            week_data = weeks_data_dict[week_id]
            week_type = week_data.get('type')
            if week_type != 'undefined':
                week_notes = week_data.get('notes', '')
                week_nodes_dict[week_id] = {
                    'week': week_id,
                    'start_date': week_start_date,
                    'end_date': week_end_date,
                    'type': week_type,
                    'notes': week_notes
                }
                if academic_year_data_dir:
                    week_nodes_dict[week_id]['data_dir'] = os.path.join(academic_year_data_dir, f"{week_id}")
                    if not os.path.exists(week_nodes_dict[week_id]['data_dir']):
                        os.makedirs(week_nodes_dict[week_id]['data_dir'])
                week_nodes_dict[week_id]['node'] = create_local_planner_node_using_labels(session, labels, label, week_nodes_dict[week_id])
        week_start_date += timedelta(days=7)  # Move to the next week
    return week_nodes_dict

def create_day_nodes_dict(session, labels, label, academic_year_start, academic_year_end, days_dict, week_nodes_dict, include_weekends=True, data_dir=None):
    logging.prod(f"Creating day nodes for academic days from {academic_year_start} to {academic_year_end}")
    
    day_nodes_dict = {}
    current_date = academic_year_start
    
    def get_day_agenda(day_data):
        agenda_parts = [
            day_data.get(part, '') for part in ['calendar_agenda', 'agenda_heading', 'agenda_notes']
        ]
        return '\n'.join(agenda_parts)
    
    def update_week_type(current_date_str, week_data, next_week_data):
        if week_data:
            week_type = week_data.get('type', '')
            if next_week_data and next_week_data.get('type') == 'holiday' and current_date.weekday() >= 5:
                week_type = 'holiday'
            day_nodes_dict[current_date_str]['week_type'] = week_type
            
    def create_or_get_node_dir(current_date_str):
        if data_dir:
            node_path = os.path.join(data_dir, 'dates', current_date_str)
        else:
            node_path = os.path.join('dates', current_date_str)
        if not os.path.exists(node_path):
            os.makedirs(node_path)
        return node_path
    
    while current_date <= academic_year_end:
        current_date_str = current_date.strftime('%Y-%m-%d')
        day_data = days_dict.get(current_date_str)
        day_modifier = 'undefined'  # Default type
        if day_data and 'type' in day_data and pd.notna(day_data['type']):
            day_modifier = day_data['type']
        if include_weekends or current_date.weekday() < 5:
            if day_modifier != 'undefined':  # Process only if day is defined
                day_agenda = get_day_agenda(day_data)
                day_nodes_dict[current_date_str] = {
                    'date': current_date.date(),
                    'type': day_modifier,
                    'notes': day_agenda,
                    'data_dir': create_or_get_node_dir(current_date_str)
                }
                first_monday = current_date - timedelta(days=current_date.weekday())
                next_monday = first_monday + timedelta(days=7)
                week_data = week_nodes_dict.get(first_monday.strftime('%Y-W%W'))
                next_week_data = week_nodes_dict.get(next_monday.strftime('%Y-W%W'))
                update_week_type(current_date_str, week_data, next_week_data)
                
                day_nodes_dict[current_date_str]['node'] = create_local_planner_node_using_labels(session, labels, label, day_nodes_dict[current_date_str])
                
        current_date += timedelta(days=1)
    return day_nodes_dict

def create_academic_period_nodes_dict_for_academic_days(session, local_planner_node_and_relationship_labels, label, period_times, academic_year_start, academic_year_end, day_nodes_dict, include_all=True, include_timetable_only=False, data_dir=None):
    logging.prod(f"Creating academic period nodes for academic days from {academic_year_start} to {academic_year_end}")
    labels = local_planner_node_and_relationship_labels
    period_nodes_dict = {}
    current_date = academic_year_start
    while current_date <= academic_year_end:
        current_date_str = current_date.strftime('%Y-%m-%d')
        day_node_dict = day_nodes_dict.get(current_date_str)
        if day_node_dict and day_node_dict['type'] == 'academic_day':
            date = day_node_dict['date']
            for period_name, times in period_times.items():
                period_class = times['class']
                if period_class == 'P':
                    period_type = 'lesson'
                    period = f"{period_type}_{period_name}" # TODO: This should be handled earlier
                else:
                    period_type = period_class # TODO: Implement named periods
                    period = f"{period_name}"
                    
                period_id = f"{date}_{period}"
                start = times['start']
                end = times['end']
                start_datetime = datetime.combine(datetime.today(), start)
                end_datetime = datetime.combine(datetime.today(), end)
                time_difference = end_datetime - start_datetime
                minutes = time_difference.total_seconds() / 60
                week_type = day_node_dict['week_type'][-1] # Get the last character of the week_type
                period_node_properties = {
                        'start': datetime.combine(day_node_dict['date'], start),
                        'minutes': minutes,
                        'period': period,
                        'type': period_type,
                        'week_type': week_type
                    }
                if data_dir:
                    period_node_properties['data_dir'] = os.path.join(data_dir, period)
                else:
                    period_node_properties['data_dir'] = os.path.join(day_node_dict['data_dir'], period)
                if not os.path.exists(period_node_properties['data_dir']):
                    os.makedirs(period_node_properties['data_dir'])
                # TODO: Make this more flexible as currently it's hard coded (if using for other schools)
                if include_all: # Include all timetabled periods, breaks, meetings and other periods defined in the excel file
                    period_nodes_dict[period_id] = period_node_properties
                    period_nodes_dict[period_id]['node'] = create_local_planner_node_using_labels(session, labels, label, period_node_properties)
                else:
                    logging.error('Must be either include_all or include_timetable_only or both')
                    return ValueError("Invalid period options")
        current_date += timedelta(days=1)
    return period_nodes_dict

# %% [markdown]
# #### Initialise the local planner

# %%
# Function to create a local calendar
def initialise_local_planner(session, node_and_relationship_labels, init_options, planner_dataframes, path=None, local_node=None):
    logging.prod(f"Initialising local planner...")
    # Unpack the options
    packed_options = init_options
    option_keys = ['local_planner_owner_type', 'local_planner_type', 'local_planner_name', 'create_data_directories', 'create_init_constraints', 'create_academic_year', 'create_academic_terms', 'create_academic_term_breaks', 'create_academic_weeks', 'create_academic_week_holidays', 'create_academic_dates', 'create_academic_days', 'create_academic_holiday_days', 'create_academic_staff_days', 'create_academic_off_timetable', 'create_academic_periods', 'create_academic_period_timetabled_lessons', 'create_academic_period_registrations', 'create_academic_period_breaks', 'create_academic_period_meetings', 'create_academic_period_tasks', 'create_academic_time_chunks', 'create_sequenced_relationships']
    sequenced_relationship_options_keys = ['create_sequenced_academic_terms_with_breaks', 'create_sequenced_academic_terms_without_breaks', 'create_sequenced_academic_weeks_with_breaks', 'create_sequenced_academic_weeks_without_breaks', 'create_sequenced_academic_dates_with_breaks', 'create_sequenced_academic_dates_without_breaks', 'create_sequenced_academic_periods_with_all', 'create_sequenced_academic_periods_with_timetabled_periods', 'create_sequenced_academic_periods_with_lessons', 'create_sequenced_academic_time_chunks']
    options = {}
    for key in option_keys:
        if key == 'create_sequenced_relationships' and init_options.get(key) == 'True':
            # Only unpack sequenced relationship options if 'create_sequenced_relationships' is true
            sequenced_options = init_options.get('sequenced_relationship_options', {})  # Default to empty dict if not found
            options[key] = {k: sequenced_options.get(k) for k in sequenced_relationship_options_keys}
        else:
            # For all other keys, just get the value from init_options
            options[key] = init_options.get(key)
    # Unpack the time chunk duration
    if options.get('create_academic_time_chunks') == 'True':  # Ensure it's a string comparison
        options['time_chunk_duration'] = init_options.get('time_chunk_duration')
    # Unpack the labels
    packed_labels = node_and_relationship_labels
    label_keys = ['local_planner_node_label', 'local_academic_year_node_label', 'local_academic_term_node_label', 'local_academic_term_break_node_label', 'local_academic_week_node_label', 'local_academic_week_holiday_node_label', 'local_academic_date_node_label', 'local_academic_day_node_label', 'local_academic_holiday_day_node_label', 'local_academic_staff_day_node_label', 'local_academic_off_timetable_node_label', 'local_academic_period_node_label','local_academic_period_timetabled_lesson_node_label', 'local_academic_period_registration_node_label','local_academic_period_break_node_label', 'local_academic_period_meeting_node_label', 'local_academic_period_task_node_label', 'local_academic_time_chunk_node_label', 'contains_many_hierarchy_label', 'contains_set_hierarchy_label', 'contains_single_hierarchy_label']
    labels = {key: packed_labels.get(key) for key in label_keys}
    
    # Verify and unpack the data
    if str_to_bool(options['create_data_directories']) and not path:
        logging.error("Path must be provided to create data directories.")
        return ValueError("Initialisation error.")
    logging.app(f"Initialising local planner with dataframes.")
    calendar_df = planner_dataframes['calendarlookup_df']
    days_df = planner_dataframes['dayslookup_df']
    weeks_df = planner_dataframes['weekslookup_df']
    excel_days_list_of_dicts = planner.populate_days_array(days_df)
    excel_weeks_list_of_dicts = planner.populate_weeks_array(weeks_df)
    # Create planner variables from options
    if options['local_planner_owner_type'] == 'staff':
        academic_year_info = planner.extract_academic_year_info(calendar_df, 'staff')
    elif options['local_planner_owner_type'] == 'student':
        academic_year_info = planner.extract_academic_year_info(calendar_df, 'student')
    else:
        logging.error(f"Owner type {options['local_planner_owner_type']} not recognised.")
        return ValueError("Initialisation error.")
    academic_year_start = academic_year_info['start_date']
    academic_year_end = academic_year_info['end_date']
    if academic_year_start > academic_year_end:
        logging.error(f"Academic year start date {academic_year_start} is after end date {academic_year_end}.")
        return ValueError("Initialisation error.")
    
    weeks_dict, days_dict = create_weeks_days_dicts(academic_year_start.year, excel_days_list_of_dicts, excel_weeks_list_of_dicts)
    period_times = planner.extract_period_times(calendar_df)
    
    # Create the local planner
    local_planner = {
        'local_planner_node': None,
        'local_academic_year_node': None,
        'local_academic_term_nodes': {},
        'local_academic_term_break_nodes': {},
        'local_academic_week_nodes': {},
        'local_academic_week_holiday_nodes': {},
        'local_academic_date_nodes': {},
        'local_academic_day_nodes': {},
        'local_academic_holiday_day_nodes': {},
        'local_academic_staff_day_nodes': {},
        'local_academic_off_timetable_nodes': {},
        'local_academic_period_nodes': {},
        'local_academic_period_timetabled_lesson_nodes': {},
        'local_academic_period_registration_nodes': {},
        'local_academic_period_break_nodes': {},
        'local_academic_period_meeting_nodes': {},
        'local_academic_period_task_nodes': {},
        'local_academic_time_chunk_nodes': {},
        'hierarchy_local_planner': {},
        'hierarchy_local_academic_year': {},
        'hierarchy_local_academic_term': {},
        'hierarchy_local_academic_week': {},
        'hierarchy_local_academic_date': {},
        'hierarchy_local_academic_period': {},
        'hierarchy_local_academic_time_chunk': {},
        'sequenced_local_academic_year_relationships': {},
        'sequenced_local_academic_term_relationships': {},
        'sequenced_local_academic_week_relationships': {},
        'sequenced_local_academic_date_relationships': {},
        'sequenced_local_academic_period_relationships': {},
        'sequenced_local_academic_time_chunk_relationships': {},
    }
    # Create the local planner node
    properties = f"TEST_PLANNER: {options['local_planner_owner_type']}{options['local_planner_name']}{options['local_planner_type']}"
    local_planner_node = create_local_planner_node_using_labels(session, node_and_relationship_labels, labels['local_planner_node_label'], properties)
    local_planner['local_planner_node'] = local_planner_node
    if local_node:
        local_planner['hierarchy_local_planner'] = create_local_planner_relationship(session, local_node, local_planner_node, labels['contains_set_hierarchy_label'], node_and_relationship_labels)
    
    # Create the academic year node
    if str_to_bool(options['create_academic_year']):
        local_academic_year_properties = [academic_year_start.year, academic_year_end.year]
        academic_year_data_dir = os.path.join(path, f"{academic_year_start.year}-{academic_year_end.year}")
        if not os.path.exists(academic_year_data_dir):
            os.makedirs(academic_year_data_dir)
        local_academic_year_properties.append(academic_year_data_dir)
        local_academic_year_node = create_local_planner_node_using_labels(session, node_and_relationship_labels, labels['local_academic_year_node_label'], local_academic_year_properties)
        academic_planner_relationship = create_local_planner_relationship(session, local_planner_node, local_academic_year_node, labels['contains_set_hierarchy_label'], node_and_relationship_labels)
        local_planner['local_academic_year_node'] = local_academic_year_node
        local_planner['hierarchy_local_academic_year'] = academic_planner_relationship

    if str_to_bool(options['create_academic_terms']):
        if str_to_bool(options['create_data_directories']):
            academic_term_data_dir = os.path.join(academic_year_data_dir, "terms")
        else:
            academic_term_data_dir = None
        academic_term_nodes = create_academic_term_nodes_dict(session, node_and_relationship_labels, labels['local_academic_term_node_label'], calendar_df, academic_term_data_dir)
        local_planner['local_academic_term_nodes'] = academic_term_nodes
        for term_node in academic_term_nodes.values():
            academic_year_relationship = create_local_planner_relationship(session, local_academic_year_node, term_node['node'], labels['contains_set_hierarchy_label'], node_and_relationship_labels)
            local_planner['hierarchy_local_academic_year'] = academic_year_relationship

    if str_to_bool(options['create_academic_term_breaks']):
        academic_term_break_data_dir = os.path.join(academic_year_data_dir, "breaks")
        academic_term_break_nodes = create_academic_term_break_nodes_dict(session, node_and_relationship_labels, labels['local_academic_term_break_node_label'], calendar_df, academic_term_break_data_dir)
        local_planner['local_academic_term_break_nodes'] = academic_term_break_nodes
        for term_break_node in academic_term_break_nodes.values():
            academic_year_relationship = create_local_planner_relationship(session, local_academic_year_node, term_break_node['node'], labels['contains_set_hierarchy_label'], node_and_relationship_labels)
            local_planner['hierarchy_local_academic_year'] = academic_year_relationship

    if str_to_bool(options['create_academic_weeks']):
        if options['create_data_directories']:
            academic_week_data_dir = os.path.join(academic_year_data_dir, "weeks")
        else:
            academic_week_data_dir = None
        week_nodes_dict = create_week_nodes_dict(session, node_and_relationship_labels, labels['local_academic_week_node_label'], academic_year_start.year, weeks_dict, academic_week_data_dir, include_weekends=True)
        local_planner['local_academic_week_nodes'] = week_nodes_dict
        if str_to_bool(options['create_academic_terms']) or str_to_bool(options['create_academic_term_breaks']):
            if str_to_bool(options['create_academic_terms']):
                for academic_term_node in academic_term_nodes.values():
                    for week_node in week_nodes_dict.values():
                        if ((week_node['start_date'] <= academic_term_node['start_date'] and week_node['start_date'] + timedelta(days=6) >= academic_term_node['start_date']) or
                            (week_node['start_date'] >= academic_term_node['start_date'] and week_node['start_date'] + timedelta(days=6) <= academic_term_node['end_date']) or
                            (week_node['start_date'] <= academic_term_node['end_date'] and week_node['start_date'] + timedelta(days=6) >= academic_term_node['end_date'])):
                            academic_term_relationship = create_local_planner_relationship(session, academic_term_node['node'], week_node['node'], labels['contains_set_hierarchy_label'], node_and_relationship_labels)
                            local_planner['hierarchy_local_academic_term'] = academic_term_relationship
            if str_to_bool(options['create_academic_term_breaks']):
                for academic_term_break_node in academic_term_break_nodes.values():
                    for week_node in week_nodes_dict.values():
                        if week_node['start_date'] >= academic_term_break_node['start_date'] and week_node['start_date'] + timedelta(days=6) <= academic_term_break_node['end_date']:
                            academic_term_break_relationship = create_local_planner_relationship(session, academic_term_break_node['node'], week_node['node'], labels['contains_set_hierarchy_label'], node_and_relationship_labels)
                            local_planner['hierarchy_local_academic_term'] = academic_term_break_relationship
        else:
            for week_node in week_nodes_dict.values():
                academic_year_relationship = create_local_planner_relationship(session, local_academic_year_node, week_node['node'], labels['contains_set_hierarchy_label'], node_and_relationship_labels)
                local_planner['hierarchy_local_academic_year'] = academic_year_relationship

    if str_to_bool(options['create_academic_dates']):
        if str_to_bool(options['create_data_directories']):
            academic_date_data_dir = os.path.join(academic_year_data_dir, "dates")
        else:
            academic_date_data_dir = None
        day_nodes_dict = create_day_nodes_dict(session, node_and_relationship_labels, labels['local_academic_date_node_label'], academic_year_start, academic_year_end, days_dict, week_nodes_dict, include_weekends=True, data_dir=academic_date_data_dir)
        local_planner['local_academic_date_nodes'] = day_nodes_dict
        if str_to_bool(options['create_academic_weeks']):
            for week_node in week_nodes_dict.values():
                for day_node in day_nodes_dict.values():                    
                    if day_node['date'] >= week_node['start_date'] and day_node['date'] <= week_node['end_date']:
                        academic_week_relationship = create_local_planner_relationship(session, week_node['node'], day_node['node'], labels['contains_set_hierarchy_label'], node_and_relationship_labels)
                        local_planner['hierarchy_local_academic_week'] = academic_week_relationship
        elif str_to_bool(options['create_academic_terms']) or str_to_bool(options['create_academic_term_breaks']):
            for academic_term_node in academic_term_nodes:
                for day_node in day_nodes_dict.values():
                    if day_node['date'] >= academic_term_node['start_date'] and day_node['date'] <= academic_term_node['end_date']:
                        academic_term_relationship = create_local_planner_relationship(session, academic_term_node['node'], day_node['node'], labels['contains_set_hierarchy_label'], node_and_relationship_labels)
                        local_planner['hierarchy_local_academic_term'] = academic_term_relationship
            for academic_term_break_node in academic_term_break_nodes:
                for day_node in day_nodes_dict.values():
                    if day_node['date'] >= academic_term_break_node['start_date'] and day_node['date'] <= academic_term_break_node['end_date']:
                        academic_term_break_relationship = create_local_planner_relationship(session, academic_term_break_node['node'], day_node['node'], labels['contains_set_hierarchy_label'], node_and_relationship_labels)
                        local_planner['hierarchy_local_academic_term'] = academic_term_break_relationship
        else:
            for day_node in day_nodes_dict.values():
                academic_year_relationship = create_local_planner_relationship(session, local_academic_year_node['node'], day_node['node'], labels['contains_set_hierarchy_label'], node_and_relationship_labels)
                local_planner['hierarchy_local_academic_year'] = academic_year_relationship

    if str_to_bool(options['create_academic_periods']):
        period_nodes_dict = create_academic_period_nodes_dict_for_academic_days(session, node_and_relationship_labels, labels['local_academic_period_node_label'], period_times, academic_year_start, academic_year_end, day_nodes_dict, include_all=True, include_timetable_only=False, data_dir=False)
        local_planner['local_academic_period_nodes'] = period_nodes_dict
        for period_node in period_nodes_dict.values():
            for day_node in day_nodes_dict.values():
                if day_node['date'] == period_node['start'].date():
                    academic_date_relationship = create_local_planner_relationship(session, day_node['node'], period_node['node'], labels['contains_set_hierarchy_label'], node_and_relationship_labels)
                    local_planner['hierarchy_local_academic_date'] = academic_date_relationship

    if str_to_bool(options['create_academic_time_chunks']) and str_to_bool(options['create_academic_periods']):
        logging.prod("Creating academic time chunks for academic periods")
        for period_node in local_planner['local_academic_period_nodes'].values():
            if 'lesson' in period_node['type']:
                period_length = period_node['minutes']
                time_chunk_start = period_node['start']
                time_chunk_duration = options['time_chunk_duration']
                if time_chunk_duration == 'parent':
                    time_chunk_minutes = period_node['minutes']
                else:
                    time_chunk_minutes = time_chunk_duration
                time_chunks_for_period = period_length / int(time_chunk_minutes)
                if time_chunks_for_period.is_integer():
                    for i in range(int(time_chunks_for_period)):
                        properties = {
                            'start': time_chunk_start,
                            'minutes': time_chunk_minutes
                        }
                        time_chunk_node = create_local_planner_node_using_labels(session, node_and_relationship_labels, labels['local_academic_time_chunk_node_label'], properties)
                        academic_period_relationship = create_local_planner_relationship(session, period_node['node'], time_chunk_node, labels['contains_set_hierarchy_label'], node_and_relationship_labels)
                        local_planner['hierarchy_local_academic_period'] = academic_period_relationship
                        local_planner['local_academic_time_chunk_nodes'][period_node['type']] = time_chunk_node
                        time_chunk_start = time_chunk_start + timedelta(minutes=int(time_chunk_minutes))
                else:
                    logging.error(f"Time chunk length {time_chunk_minutes} does not divide evenly into period length {period_length}.")
                    return ValueError("Time chunk length does not divide evenly into period length.")
    elif options['create_academic_time_chunks'] and not options['create_academic_periods']:
        logging.warning("Cannot create academic time chunks without academic periods. Create a calendar instead.")    

    if options['create_sequenced_relationships']:
        if str_to_bool(options['create_sequenced_relationships'].get('create_sequenced_academic_terms_with_breaks')):
            combined_nodes = []
            for term, info in local_planner['local_academic_term_nodes'].items():
                combined_nodes.append({
                    'node': info['node'], 
                    'date': info['start_date']
                })
            for term_break, info in local_planner['local_academic_term_break_nodes'].items():
                combined_nodes.append({
                    'node': info['node'], 
                    'date': info['start_date']
                })
            nodes_ordered_by_date = sorted(combined_nodes, key=lambda x: x['date'])
            sorted_nodes_only = [item['node'] for item in nodes_ordered_by_date]
            local_planner['sequenced_local_academic_term_relationships'] = sequence_list_of_nodes(session, sorted_nodes_only)
            logging.success("Sequenced academic term relationships created.")
            pass
        if str_to_bool(options['create_sequenced_relationships'].get('create_sequenced_academic_terms_without_breaks')):
            academic_term_nodes = local_planner['local_academic_term_nodes']
            node_list = [term_info['node'] for term_info in academic_term_nodes.values()]
            local_planner['sequenced_local_academic_term_relationships'] = sequence_list_of_nodes(session, node_list)
            logging.success("Sequenced academic term relationships created.")
        if str_to_bool(options['create_sequenced_relationships'].get('create_sequenced_academic_weeks_with_breaks')):
            node_list = [week_info['node'] for week_info in local_planner['local_academic_week_nodes'].values()]
            sorted_node_list = sorted(node_list, key=lambda x: x['start_date'])
            local_planner['sequenced_local_academic_week_relationships'] = sequence_list_of_nodes(session, sorted_node_list)
            logging.success("Sequenced academic week relationships created.")
        if str_to_bool(options['create_sequenced_relationships'].get('create_sequenced_academic_weeks_without_breaks')):
            pass
        if str_to_bool(options['create_sequenced_relationships'].get('create_sequenced_academic_dates_with_breaks')):
            node_list = [day_info['node'] for day_info in local_planner['local_academic_date_nodes'].values()]
            local_planner['sequenced_local_academic_date_relationships'] = sequence_list_of_nodes(session, node_list)
            logging.success("Sequenced academic date relationships created.")
        if str_to_bool(options['create_sequenced_relationships'].get('create_sequenced_academic_dates_without_breaks')):
            pass
        if str_to_bool(options['create_sequenced_relationships'].get('create_sequenced_academic_periods_with_all')):
            node_list = []
            for period_info in local_planner['local_academic_period_nodes'].values():
                if 'node' in period_info:
                    node_list.append(period_info['node'])
                else:
                    logging.warning("Missing 'node' information in period data.")
            if node_list:
                local_planner['sequenced_local_academic_period_relationships'] = sequence_list_of_nodes(session, node_list)
                logging.success("Sequenced academic period relationships created.")
            else:
                logging.error("No valid period nodes found for sequencing.")
        if str_to_bool(options['create_sequenced_relationships'].get('create_sequenced_academic_periods_with_timetabled_periods')):
            pass
        if str_to_bool(options['create_sequenced_relationships'].get('create_sequenced_academic_periods_with_lessons')):
            pass
        if str_to_bool(options['create_sequenced_relationships'].get('create_sequenced_academic_time_chunks')):
            node_list = []
            for key in local_planner['local_academic_time_chunk_nodes']:
                node_list.append(local_planner['local_academic_time_chunk_nodes'][key])
            local_planner['sequenced_local_academic_time_chunk_relationships'] = sequence_list_of_nodes(session, node_list)
            logging.success("Sequenced academic time chunk relationships created.")
    return local_planner

# %% [markdown]
# ### Local curriculum

# %% [markdown]
# #### Local curriculum KevlarAI enhanced node and relationships preparations

# %%
# Functions to prepare properties
def prepare_local_curriculum_node(label, data, data_dir=None):
    if label == 'LocalCurriculum':
        properties = {
            'curriculum_name': data # e.g. national_curriculum
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'LearningStage': # TODO: for uk only? is it necessary? how is it quantised and laddered?
        learning_stage = data[0]
        subject_name = data[1]
        key_stage_curriculum = f"key_stage_{learning_stage}" # e.g. key_stage_{3}
        properties = {
            'key_stage_curriculum:': key_stage_curriculum
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'YearGroup': # TODO: for uk only? is it necessary? how is it quantised and laddered?
        year_group = data
        properties = {
            'year_group': year_group
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'Subject':
        subject_name = data
        properties = {
            'subject_name': subject_name
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'SubjectLevel': # TODO: This MUST be necessary. How is it quantised and laddered?
        subject = data[0]
        level = data[1]
        subject_level = f"key_stage_{level}_{subject}" # e.g. key_stage_{3}_{science}
        properties = {
            'subject_level': subject_level
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'SubjectYearGroup': # TODO: for uk only? is it necessary? how is it quantised and laddered?
        subject = data[0]
        year_group = data[1]
        subject_year_group = f"year_{year_group}_{subject}"
        properties = {
            'subject_year_group': subject_year_group
        }
    elif label == 'Syllabus':
        curriculum = data[0],
        syllabus_group = data[1]
        subject = data[2]
        syllabus_name = f"{curriculum}_{syllabus_group}_{subject}" # e.g.{fpgs_national_curriculum}_{year_7}_{science} or {edexcel}_{gcse}_{science}
        properties = {
            'syllabus_name': syllabus_name
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'SchemeOfWork':
        department = data[0]
        subject = data[1]
        year_groups = data[2]
        if isinstance(year_groups, list):
            year_label = 'years'
            year_groups_string = '_'.join([str(year) for year in year_groups])
        else:
            year_label = 'year'
        scheme_of_work_name = f"{department}_{year_label}_{year_groups_string}_{subject}"
        properties = {
            'scheme_of_work_name': scheme_of_work_name,
            'department': department,
            'subject': subject,
            'year_groups': year_groups, # TODO: will probably fail here because of the list
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'SchemeTopic':
        topic_id = data[0]
        topic_name = data[1]
        topic_created_in_academic_year = data[2]
        topic_type = data[3]
        topic_lessons = data[4]
        assessment_type = data[5]
        topic_name_full = f"{topic_id}_{topic_name}_{topic_created_in_academic_year}_({topic_type})"
        topic_name_short = f"{topic_id}_{topic_name}"
        properties = {
            'topic_name_full': topic_name_full,
            'topic_name_short': topic_name_short,
            'topic_id': topic_id,
            'topic_type': topic_type,
            'topic_lessons': topic_lessons,
            'assessment_type': assessment_type
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'SchemeLesson':
        lesson_id = data[0]
        lesson_name = data[1]
        lesson_created_in_academic_year = data[2]
        lesson_type = data[3]
        lesson_topic_id = data[4]
        lesson_name_full = f"{lesson_id}_{lesson_name}_{lesson_created_in_academic_year}_({lesson_type})"
        lesson_name_short = f"{lesson_id}_{lesson_name}"
        properties = {
            'lesson_name_full': lesson_name_full,
            'lesson_name_short': lesson_name_short,
            'lesson_id': lesson_id,
            'lesson_type': lesson_type,
            'lesson_topic_id': lesson_topic_id
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'SchemeStatement':
        statement_id = data[0]
        statement_name = data[1]
        statement_created_in_academic_year = data[2]
        statement_type = data[3]
        statement_lesson_id = data[4]
        statement_name_full = f"{statement_id}_{statement_name}_{statement_created_in_academic_year}_({statement_type})"
        statement_name_short = f"{statement_id}_{statement_name}"
        properties = {
            'statement_name_full': statement_name_full,
            'statement_name_short': statement_name_short,
            'statement_id': statement_id,
            'statement_type': statement_type,
            'statement_lesson_id': statement_lesson_id
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    elif label == 'SchemeResource':
        resource_id = data[0]
        resource_name = data[1]
        resource_created_in_academic_year = data[2]
        resource_type = data[3]
        properties = {
            'resource_name': f"{resource_id}_{resource_name}_{resource_created_in_academic_year}_({resource_type})",
            'resource_id': resource_id,
            'resource_type': resource_type
        }
        if data_dir:
            properties['data_dir'] = data_dir
        return properties
    else:
        return ValueError("Invalid type of local curriculum node")

def prepare_local_learning_stage_node(learning_stage, data_dir=None):
    properties = {
        'learning_stage': f"key_stage_{learning_stage}"
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_year_group_node(year_group, data_dir=None):
    properties = {
        'year_group': year_group
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_subject_node(subject_name, data_dir=None):
    properties = {
        'subject_name': subject_name
        }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_department_node(department, data_dir=None):
    properties = {
        'department': department
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_subject_level_node(subject, level, data_dir=None):
    properties = {
        'subject_level': f"key_stage_{level}_{subject}"
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_subject_year_group_node(subject, year_group, data_dir=None):
    properties = {
        'subject_year_group': f"year_{year_group}_{subject}"
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_syllabus_node(curriculum, syllabus_group, subject, data_dir=None):
    properties = {
        'syllabus_name': f"{curriculum}_{syllabus_group}_{subject}"
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_scheme_of_work_node(department, subject, year_groups, topic_created_in_academic_year, data_dir=None):
    if year_groups == 'GCSE' or year_groups == 'A_Level':
        year_label = ''
        year_groups_string = year_groups
    else:
        year_label = 'year_'
        year_groups_string = year_groups
    properties = {
        'scheme_of_work_name': f"{department}_{year_label}{year_groups_string}_{subject}_({topic_created_in_academic_year})",
        'department': department,
        'subject': subject,
        'year_groups': year_groups,
        'created:': topic_created_in_academic_year # TODO: producer of the scheme of work
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_scheme_topic_node(topic_id, topic_name, topic_created_in_academic_year, topic_type, topic_lessons, assessment_type, data_dir=None):
    topic_name_full = f"{topic_id}_{topic_name}_{topic_created_in_academic_year}_({topic_type})"
    topic_name_short = f"{topic_id}_{topic_name}"
    properties = {
        'topic_name_full': topic_name_full,
        'topic_name_short': topic_name_short,
        'topic_id': topic_id,
        'topic_type': topic_type,
        'topic_lessons': topic_lessons,
        'assessment_type': assessment_type
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_scheme_lesson_node(lesson_id, lesson_name, lesson_created_in_academic_year, lesson_type, lesson_topic_id, data_dir=None):
    lesson_name_full = f"{lesson_id}_{lesson_name}_{lesson_created_in_academic_year}_({lesson_type})"
    lesson_name_short = f"{lesson_id}_{lesson_name}"
    properties = {
        'lesson_name_full': lesson_name_full,
        'lesson_name_short': lesson_name_short,
        'lesson_id': lesson_id,
        'lesson_type': lesson_type,
        'lesson_topic_id': lesson_topic_id
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_scheme_statement_node(statement_id, statement_name, statement_created_in_academic_year, statement_type, statement_lesson_id, data_dir=None):
    statement_name_full = f"{statement_id}_{statement_name}_{statement_created_in_academic_year}_({statement_type})"
    statement_name_short = f"{statement_id}_{statement_name}"
    properties = {
        'statement_name_full': statement_name_full,
        'statement_name_short': statement_name_short,
        'statement_id': statement_id,
        'statement_type': statement_type,
        'statement_lesson_id': statement_lesson_id
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

def prepare_local_scheme_resource_node(resource_id, resource_name, resource_created_in_academic_year, resource_type, data_dir=None):
    properties = {
        'resource_name': f"{resource_id}_{resource_name}_({resource_type})",
        'resource_id': resource_id,
        'resource_type': resource_type,
        'created_in_academic_year': resource_created_in_academic_year # # TODO: producer of the resource
    }
    if data_dir:
        properties['data_dir'] = data_dir
    return properties

# %% [markdown]
# #### Get curriculum labels, properties, relationships and initialisation options

# %%
def get_local_curriculum_node_and_relationship_labels_using_accessor(local_curriculum_labels_file):
    curriculum_node_labels_accessor, hierarchy_labels_accessor = [get_curriculum_labels_accessor(local_curriculum_labels_file)[i] for i in [1, 3]]
    local_curriculum_node_and_relationship_labels = {
        'local_curriculum_node_label': curriculum_node_labels_accessor.get('local_curriculum_node_label'),
        'local_learning_stage_node_label': curriculum_node_labels_accessor.get('local_learning_stage_node_label'),
        'local_year_group_node_label': curriculum_node_labels_accessor.get('local_year_group_node_label'),
        'local_subject_node_label': curriculum_node_labels_accessor.get('local_subject_node_label'),
        'local_department_node_label': curriculum_node_labels_accessor.get('local_department_node_label'),
        'local_subject_level_node_label': curriculum_node_labels_accessor.get('local_subject_level_node_label'),
        'local_subject_year_group_node_label': curriculum_node_labels_accessor.get('local_subject_year_group_node_label'),
        'local_syllabus_node_label': curriculum_node_labels_accessor.get('local_syllabus_node_label'),
        'local_scheme_of_work_node_label': curriculum_node_labels_accessor.get('local_scheme_of_work_node_label'),
        'local_scheme_topic_node_label': curriculum_node_labels_accessor.get('local_scheme_topic_node_label'),
        'local_scheme_lesson_node_label': curriculum_node_labels_accessor.get('local_scheme_lesson_node_label'),
        'local_scheme_statement_node_label': curriculum_node_labels_accessor.get('local_scheme_statement_node_label'),
        'local_scheme_resource_node_label': curriculum_node_labels_accessor.get('local_scheme_resource_node_label'),
        'contains_many_hierarchy_label': curriculum_node_labels_accessor.get('contains_many_hierarchy_label'),
        'contains_set_hierarchy_label': curriculum_node_labels_accessor.get('contains_set_hierarchy_label'),
        'contains_single_hierarchy_label': curriculum_node_labels_accessor.get('contains_single_hierarchy_label')
    }
    return local_curriculum_node_and_relationship_labels

def get_local_curriculum_init_options(init_options):
    logging.success(f"Initialising local curriculum options: {init_options}.")
    local_curriculum_name = init_options.get('local_curriculum_name', 'LocalCurriculum'),
    
    def str_to_bool(s, default=False):
        return s.lower() in ['true', 't', 'yes', 'y'] if s is not None else default
    options_keys = [
        'create_syllabus_structure', 'create_learning_stages', 'create_year_groups', 'create_subjects', 'create_departments', 'create_subject_levels', 'create_subject_year_groups', 'create_syllabuses', 'create_schemes_of_works', 'create_scheme_topics', 'create_scheme_lessons', 'create_scheme_statements', 'create_scheme_resources', 'create_sequenced_relationships', 'create_data_directories'
    ]
    options = {k: str_to_bool(init_options.get(k), k not in ['create_data_directories','create_sequenced_relationships', 'create_syllabus_structure', 'create_scheme_resources', 'create_scheme_statements', 'create_scheme_lessons', 'create_scheme_topics', 'create_schemes_of_works', 'create_syllabuses', 'create_subject_year_groups', 'create_subject_levels', 'create_year_groups', 'create_learning_stages', 'create_subjects', 'create_departments']) for k in options_keys}
    sequenced_relationships_options = init_options.get('sequenced_relationships', {})
    if sequenced_relationships_options:
        sequenced_options_keys = [
            'create_sequenced_learning_stages', 'create_sequenced_year_groups',  'create_sequenced_subject_levels', 'create_sequenced_subject_year_groups','create_sequenced_scheme_topics', 'create_sequenced_scheme_lessons', 'create_sequenced_scheme_statements', 'create_sequenced_scheme_resources'
        ]
        sequenced_options = {k: str_to_bool(sequenced_relationships_options.get(k)) for k in sequenced_options_keys}
        local_curriculum_init_options = {**options, **sequenced_options, 'local_curriculum_name': local_curriculum_name, 'local_curriculum_options': init_options}
    else:
        local_curriculum_init_options = {**options, 'local_curriculum_name': local_curriculum_name, 'local_curriculum_options': init_options}
    return local_curriculum_init_options

# %% [markdown]
# #### Create curriculum constraints

# %%
def create_local_curriculum_node_constraints_using_file(session, local_curriculum_labels_file):
    labels = get_local_curriculum_node_and_relationship_labels_using_accessor(local_curriculum_labels_file)
    label_constraints = {
        'local_curriculum_node_label': 'curriculum_name',
        'local_learning_stage_node_label': 'learning_stage',
        'local_year_group_node_label': 'year_group',
        'local_subject_node_label': 'subject_name',
        'local_department_node_label': 'department',
        'local_subject_level_node_label': 'subject_level',
        'local_subject_year_group_node_label': 'subject_year_group',
        'local_syllabus_node_label': 'syllabus_name',
        'local_scheme_of_work_node_label': 'scheme_of_work_name',
        'local_scheme_topic_node_label': 'topic_name_full',
        'local_scheme_lesson_node_label': 'lesson_name_full',
        'local_scheme_statement_node_label': 'statement_name_full',
        'local_scheme_resource_node_label': 'resource_name'
    }

    constraint_queries = [
        f"CREATE CONSTRAINT FOR (n:{labels.get(label)}) REQUIRE n.{prop} IS NOT NULL"
        for label, prop in label_constraints.items()
        if labels.get(label)  # Ensure label is not None
    ]

    with session.begin_transaction() as tx:
        for query in constraint_queries:
            logging.info(f'Running curriculum node constraint query: {query}')
            tx.run(query)

    return True

def create_allowed_curriculum_relationship_constraints_using_labels(packed_labels):
    label_keys = ['local_curriculum_node_label', 'local_subject_node_label', 'local_department_node_label', 'local_learning_stage_node_label', 'local_year_group_node_label', 'local_subject_level_node_label', 'local_subject_year_group_node_label', 'local_syllabus_node_label', 'local_scheme_of_work_node_label', 'local_scheme_topic_node_label', 'local_scheme_lesson_node_label', 'local_scheme_statement_node_label', 'local_scheme_resource_node_label', 'contains_many_hierarchy_label', 'contains_set_hierarchy_label', 'contains_single_hierarchy_label']
    labels = {key: packed_labels.get(key) for key in label_keys}
    allowed_curriculum_relationship_constraints_dict_from_labels = {
    (labels['local_curriculum_node_label'], labels['local_subject_node_label']): labels['contains_set_hierarchy_label'], # curriculum does not include year groups - this is a pastoral element
    (labels['local_curriculum_node_label'], labels['local_learning_stage_node_label']): labels['contains_many_hierarchy_label'],
    (labels['local_curriculum_node_label'], labels['local_year_group_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_curriculum_node_label'], labels['local_department_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_curriculum_node_label'], labels['local_subject_level_node_label']): labels['contains_many_hierarchy_label'],
    (labels['local_curriculum_node_label'], labels['local_subject_year_group_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_curriculum_node_label'], labels['local_syllabus_node_label']): labels['contains_many_hierarchy_label'],
    (labels['local_curriculum_node_label'], labels['local_scheme_of_work_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_subject_node_label'], labels['local_subject_level_node_label']): labels['contains_many_hierarchy_label'],
    (labels['local_subject_node_label'], labels['local_subject_year_group_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_subject_node_label'], labels['local_syllabus_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_subject_node_label'], labels['local_scheme_of_work_node_label']): labels['contains_set_hierarchy_label'],
    (labels['local_scheme_of_work_node_label'], labels['local_scheme_topic_node_label']): labels['contains_many_hierarchy_label'],
    (labels['local_scheme_topic_node_label'], labels['local_scheme_lesson_node_label']): labels['contains_many_hierarchy_label'],
    (labels['local_scheme_lesson_node_label'], labels['local_scheme_statement_node_label']): labels['contains_many_hierarchy_label'],
    (labels['local_scheme_lesson_node_label'], labels['local_scheme_resource_node_label']): labels['contains_many_hierarchy_label']
    # TODO: Add new labels for resource types, statement types and their relationships
    }
    return allowed_curriculum_relationship_constraints_dict_from_labels

# %% [markdown]
# #### Functions to create local curriculum nodes and relationships

# %%
# Create a local planner
def create_local_curriculum_node_using_labels(session, labels, label, properties, path=None):
    logging.success(f"Creating local curriculum node with label: {label} and properties: {properties}.")
    if label == labels.get('local_curriculum_node_label'): # Handle local curriculum node at initialisation
        logging.debug(f"Creating local curriculum node with properties: {properties}")
        prepared_properties = prepare_local_curriculum_node(label, properties, path)
    elif label == labels.get('local_learning_stage_node_label'):
        logging.debug(f"Creating local learning stage node with properties: learning_stage: {properties}")
        prepared_properties = prepare_local_learning_stage_node(properties, path)
    elif label == labels.get('local_year_group_node_label'):
        logging.debug(f"Creating local year group node with properties: year_group: {properties}")
        prepared_properties = prepare_local_year_group_node(properties, path)
    elif label == labels.get('local_subject_node_label'):
        logging.debug(f"Creating local subject node with properties: subject_name: {properties}")
        prepared_properties = prepare_local_subject_node(properties, path)
    elif label == labels.get('local_department_node_label'):
        logging.debug(f"Creating local department node with properties: department: {properties}")
        prepared_properties = prepare_local_department_node(properties, path)
    elif label == labels.get('local_subject_level_node_label'):
        logging.debug(f"Creating local subject level node with properties: subject: {properties['subject']}, learning_stage: {properties['learning_stage']}")
        prepared_properties = prepare_local_subject_level_node(properties['subject'], properties['learning_stage'], path)
    elif label == labels.get('local_subject_year_group_node_label'):
        logging.debug(f"Creating local subject year group node with properties: subject: {properties['subject']}, year_group: {properties['year_group']}")
        prepared_properties = prepare_local_subject_year_group_node(properties['subject'], properties['year_group'], path)
    elif label == labels.get('local_syllabus_node_label'):
        logging.debug(f"Creating local syllabus node with properties: curriculum: {properties['curriculum']}, syllabus_group: {properties['syllabus_group']}, subject: {properties['subject']}")
        prepared_properties = prepare_local_syllabus_node(properties['curriculum'], properties['syllabus_group'], properties['subject'], path)
    elif label == labels.get('local_scheme_of_work_node_label'):
        logging.debug(f"Creating local scheme of work node with properties: department: {properties['department']}, subject: {properties['subject']}, year_groups: {properties['year_groups']}")
        prepared_properties = prepare_local_scheme_of_work_node(properties['department'], properties['subject'], properties['year_groups'], path)
    elif label == labels.get('local_scheme_topic_node_label'):
        logging.debug(f"Creating local scheme topic node with properties: topic_id: {properties['topic_id']}, topic_name: {properties['topic_name']}, topic_created_in_academic_year: {properties['topic_created_in_academic_year']}, topic_type: {properties['topic_type']}, topic_lessons: {properties['topic_lessons']}, assessment_type: {properties['assessment_type']}")
        prepared_properties = prepare_local_scheme_topic_node(properties['topic_id'], properties['topic_name'], properties['topic_created_in_academic_year'], properties['topic_type'], properties['topic_lessons'], properties['assessment_type'], path)
    elif label == labels.get('local_scheme_lesson_node_label'):
        logging.debug(f"Creating local scheme lesson node with properties: lesson_id: {properties['lesson_id']}, lesson_name: {properties['lesson_name']}, lesson_created_in_academic_year: {properties['lesson_created_in_academic_year']}, lesson_type: {properties['lesson_type']}, lesson_topic_id: {properties['lesson_topic_id']}")
        prepared_properties = prepare_local_scheme_lesson_node(properties['lesson_id'], properties['lesson_name'], properties['lesson_created_in_academic_year'], properties['lesson_type'], properties['lesson_topic_id'], path)
    elif label == labels.get('local_scheme_statement_node_label'):
        logging.debug(f"Creating local scheme statement node with properties: statement_id: {properties['statement_id']}, statement_name: {properties['statement_name']}, statement_created_in_academic_year: {properties['statement_created_in_academic_year']}, statement_type: {properties['statement_type']}, statement_lesson_id: {properties['statement_lesson_id']}")
        prepared_properties = prepare_local_scheme_statement_node(properties['statement_id'], properties['statement_name'], properties['statement_created_in_academic_year'], properties['statement_type'], properties['statement_lesson_id'], path)
    elif label == labels.get('local_scheme_resource_node_label'):
        logging.debug(f"Creating local scheme resource node with properties: resource_id: {properties['resource_id']}, resource_name: {properties['resource_name']}, resource_created_in_academic_year: {properties['resource_created_in_academic_year']}, resource_type: {properties['resource_type']}")
        prepared_properties = prepare_local_scheme_resource_node(properties['resource_id'], properties['resource_name'], properties['resource_created_in_academic_year'], properties['resource_type'], path)
    else:
        logging.error(f"Invalid label: {label}.")
        return ValueError("Invalid label.")
    node = neo.create_node(session, label, prepared_properties, returns=True)
    return node

# Create relationships
def create_local_curriculum_relationship(session, start_node, end_node, label, labels, constraints=True, properties=None):
    try:
        start_label = next(iter(start_node.labels), None)
        end_label = next(iter(end_node.labels), None)
    except Exception:
        logging.error(f"start_node and end_node must be nodes. Got {start_node} and {end_node} instead.")
        return ValueError("Create relationship error.")
    if constraints:
        allowed_curriculum_relationship_constraints = create_allowed_curriculum_relationship_constraints_using_labels(labels)
        allowed = any(
            start == start_label
            and end == end_label
            and label in relationships
            for (
                start,
                end,
            ), relationships in allowed_curriculum_relationship_constraints.items()
        )
        if allowed:
            logging.info(f"Creating local curriculum relationship with constraints: {label} between {start_label} and {end_label}")
            return neo.create_relationship(
                session, start_node, end_node, label, properties, returns=True
            )
        else:
            logging.error(f"Attempted to create disallowed relationship '{label}' between '{start_label}' and '{end_label}'")
            return ValueError("Create relationship error.")
    else:
        logging.warning("Creating local curriculum relationship without constraints")
        return neo.create_relationship(
            session, start_node, end_node, label, properties, returns=True
        )

# %% [markdown]
# #### Intermediate property dictionary for the scheme of work from external data.
# The dictionary is used to create the scheme of work hierarchy for topics > lessons > statements. Resources are included alongside the statements.
# Within the scheme of work hierarchy, we will include data for the curriculum, learning level, year group, subject, 

# %%
def create_local_syllabus_dict(planner_dataframes):
    syllabus_df = planner_dataframes['syllabuslookup_df']
    
    # Split the dataframe into two based on 'SyllabusHierarchy'
    parent_df = syllabus_df[(syllabus_df['SyllabusHierarchy'] == 0) & (syllabus_df['SyllabusStatus'] == 'Active')]
    child_df = syllabus_df[(syllabus_df['SyllabusHierarchy'] == 1) & (syllabus_df['SyllabusStatus'] == 'Active')]
    
    # Initialize the syllabus dictionary
    syllabus_dict = {}
    
    # Process parent syllabuses
    for _, parent_row in parent_df.iterrows():
        syllabus_id = parent_row['SyllabusID']
        syllabus_info = {
            'syllabus_keystage': parent_row['SyllabusKeyStage'],
            'syllabus_subject': parent_row['SyllabusSubject'],
            'syllabus_department': parent_row['SyllabusDepartment'],
            'syllabus_source': parent_row['SyllabusSource'],
            'syllabus_year': parent_row['SyllabusYear']
        }
        
        # Preparing the structure for each syllabus in the dictionary
        syllabus_dict[syllabus_id] = {'info': syllabus_info, 'syllabus_yeargroups': {}}
    
    # Process child syllabuses (sub-syllabuses)
    for _, child_row in child_df.iterrows():
        # Find the parent syllabus ID for this child
        parent_id = "KS" + str(child_row['SyllabusKeyStage'])  + "." + child_row['SyllabusSubject'] # Hacky
        
        # Check if this child belongs to any parent in the dictionary
        if parent_id in syllabus_dict:
            subsyllabus_id = child_row['SyllabusID']
            syllabus_dict[parent_id]['syllabus_yeargroups'][subsyllabus_id] = {
                'syllabus_yeargroup': child_row['SyllabusYearGroup'],
                'syllabus_source': child_row['SyllabusSource'],
                'syllabus_year': child_row['SyllabusYear'],
            }

    with open('syllabus_dict.json', 'w') as json_file:
        json.dump(syllabus_dict, json_file, indent=4)
    
    return syllabus_dict

# %%
def create_local_topic_level_syllabus_dict(planner_dataframes):
    topic_df = planner_dataframes['topiclookup_df']
    statement_df = planner_dataframes['statementlookup_df']
    resource_df = planner_dataframes['resourcelookup_df']
    
    topic_syllabus_dict = {}
    
    # First, process each topic and organize them by type
    for _, topic_row in topic_df.iterrows():
        syllabus_id = topic_row['SyllabusStageID']
        topic_id = topic_row['TopicID']
        topic_type = topic_row['TopicType'].lower() + '_topic'  # Determines the topic type
        topic_info = topic_row.to_dict()
        
        # Ensure the syllabus_id exists and then organize by topic_type
        if syllabus_id not in topic_syllabus_dict:
            topic_syllabus_dict[syllabus_id] = {'standard_topic': {}, 'core_topic': {}, 'special_topic': {}}
        
        # Here, the specific topic type dictionary is chosen based on the topic's type
        topic_syllabus_dict[syllabus_id][topic_type][topic_id] = {'info': topic_info, 'statements': {}, 'resources': {}}
    
    # Process statements, assigning them to their respective topics
    for _, statement_row in statement_df.iterrows():
        syllabus_id = statement_row['SyllabusStageID']
        topic_id = statement_row['TopicID']
        statement_id = statement_row['StatementID']
        statement_info = statement_row.to_dict()
        
        # Find the topic_type for this statement's topic_id
        for topic_type in ['standard_topic', 'core_topic', 'special_topic']:
            if topic_id in topic_syllabus_dict[syllabus_id][topic_type]:
                topic_syllabus_dict[syllabus_id][topic_type][topic_id]['statements'][statement_id] = statement_info
                break  # Exit the loop once the statement has been added
                
    # Process resources, assigning them to their respective topics
    for _, resource_row in resource_df.iterrows():
        syllabus_id = resource_row['SyllabusStageID']
        topic_id = resource_row['TopicID']
        resource_id = resource_row['ResourceID']
        resource_info = resource_row.to_dict()
        
        # Find the topic_type for this resource's topic_id
        for topic_type in ['standard_topic', 'core_topic', 'special_topic']:
            if topic_id in topic_syllabus_dict[syllabus_id][topic_type]:
                topic_syllabus_dict[syllabus_id][topic_type][topic_id]['resources'][resource_id] = resource_info
                break  # Exit the loop once the resource has been added
            
    # Save the organized topics into a JSON file
    with open('topic_syllabus_dict.json', 'w') as json_file:
        json.dump(topic_syllabus_dict, json_file, indent=4)
        
    return topic_syllabus_dict

# %%
def create_local_lesson_level_syllabus_dict(planner_dataframes):
    topic_df = planner_dataframes['topiclookup_df']
    lesson_df = planner_dataframes['lessonlookup_df']
    statement_df = planner_dataframes['statementlookup_df']
    resource_df = planner_dataframes['resourcelookup_df']
    
    lesson_syllabus_dict = {}

    # Simplify the processing by grouping lessons, statements, and resources by TopicID and LessonID
    grouped_lessons = lesson_df.groupby('TopicID')
    grouped_statements = statement_df.groupby('LessonID')
    grouped_resources = resource_df.groupby('LessonID')

    for _, topic_row in topic_df.iterrows():
        syllabus_stage_id = topic_row['SyllabusStageID']
        syllabus_year_id = topic_row['SyllabusYearID']
        topic_id = topic_row['TopicID']
        topic_info = topic_row.to_dict()

        if syllabus_stage_id not in lesson_syllabus_dict:
            lesson_syllabus_dict[syllabus_stage_id] = {}
        if syllabus_year_id not in lesson_syllabus_dict[syllabus_stage_id]:
            lesson_syllabus_dict[syllabus_stage_id][syllabus_year_id] = {'standard_topic': {}, 'core_topic': {}, 'special_topic': {}}

        topic_type = topic_info['TopicType'].lower() + '_topic'  # standard_topic, core_topic, or special_topic
        lesson_syllabus_dict[syllabus_stage_id][syllabus_year_id][topic_type][topic_id] = {'info': topic_info, 'lessons': {}}

        if topic_id in grouped_lessons.groups:
            for _, lesson_row in grouped_lessons.get_group(topic_id).iterrows():
                lesson_id = lesson_row['LessonID']
                lesson_info = lesson_row.to_dict()
                lesson_syllabus_dict[syllabus_stage_id][syllabus_year_id][topic_type][topic_id]['lessons'][lesson_id] = {
                    'info': lesson_info,
                    'statements': {},
                    'resources': {}
                }

                if lesson_id in grouped_statements.groups:
                    statements = {row['StatementID']: row.to_dict() for _, row in grouped_statements.get_group(lesson_id).iterrows()}
                    lesson_syllabus_dict[syllabus_stage_id][syllabus_year_id][topic_type][topic_id]['lessons'][lesson_id]['statements'] = statements

                if lesson_id in grouped_resources.groups:
                    resources = {row['ResourceID']: row.to_dict() for _, row in grouped_resources.get_group(lesson_id).iterrows()}
                    lesson_syllabus_dict[syllabus_stage_id][syllabus_year_id][topic_type][topic_id]['lessons'][lesson_id]['resources'] = resources

    # Save the dictionary to a JSON file
    with open('lesson_syllabus_dict.json', 'w') as json_file:
        json.dump(lesson_syllabus_dict, json_file, indent=4)

    return lesson_syllabus_dict

# %%
def create_local_syllabus_nodes(session, local_curriculum_labels, syllabus_dict, curriculum_node, data_dir=None):
    labels = local_curriculum_labels
    local_syllabus_dict = {}

# %%
def create_local_curriculum_structure(session, local_curriculum_labels, topic_dict, curriculum_node, data_dir=None):
    labels = local_curriculum_labels
    local_curriculum_dict = {}
    
    def add_to_list_simple(label, value, list_to_check, curriculum_node, data_dir):
        if value not in list_to_check:
            # Create the node
            if label == 'LearningStage':
                properties = value
            elif label == 'YearGroup':
                properties = value
            elif label == 'Subject':
                properties = value
            elif label == 'Department':
                properties = value
            else:
                logging.error(f"Invalid label '{label}' for creating local curriculum node.")
                return ValueError("Invalid label for creating local curriculum node.")
            list_to_check.append(value)
            node = create_local_curriculum_node_using_labels(session, labels, label, properties, data_dir)
            rel = create_local_curriculum_relationship(session, curriculum_node, node, labels['contains_many_hierarchy_label'], labels, properties, data_dir)
        else:
            node = []
            rel = []
        return list_to_check, node, rel
    
    def add_subject_year_group_or_learning_stage_to_list(label, labels, subject, value, list_to_check, curriculum_node, data_dir):
        if label == labels['local_subject_level_node_label']:
            check_val = f"{value}_{subject}"
            if check_val not in list_to_check:
                logging.debug(f"Adding {label} '{value}' to list.")
                properties = {
                    'subject': subject,
                    'learning_stage': value
                }
                list_to_check.append(check_val)
                node = create_local_curriculum_node_using_labels(session, labels, label, properties, data_dir)
                rel = create_local_curriculum_relationship(session, curriculum_node, node, labels['contains_many_hierarchy_label'], labels, properties, data_dir)
                return list_to_check, node, rel
            else:
                return list_to_check, [], []
        elif label == labels['local_year_group_node_label']:
            check_val = f"year_{value}_{subject}"
            if check_val not in list_to_check:
                logging.debug(f"Adding {label} '{value}' to list.")
                properties = {
                    'subject': subject,
                    'year_group': value
                }
                list_to_check.append(check_val)
                node = create_local_curriculum_node_using_labels(session, labels, label, properties, data_dir)
                rel = create_local_curriculum_relationship(session, curriculum_node, node, labels['contains_many_hierarchy_label'], labels, properties, data_dir)
                return list_to_check, node, rel
            else:
                return list_to_check, [], []
        else:
            logging.warning(f"Invalid label '{label}' for creating local curriculum node.")
            return list_to_check, [], []
    
    def add_syllabus_to_list(label, labels, curriculum, syllabus_group, subject, list_to_check, node, data_dir):
        syllabus = {}
        check_val = f"{curriculum}_{syllabus_group}_{subject}"
        if check_val not in list_to_check:
            logging.debug(f"Adding {label} '{check_val}' to list.")
            properties = {
                'curriculum': curriculum,
                'syllabus_group': syllabus_group,
                'subject': subject
            }
            syllabus_node = create_local_curriculum_node_using_labels(session, labels, label, properties, data_dir)
            rel = create_local_curriculum_relationship(session, node, syllabus_node, labels['contains_many_hierarchy_label'], labels, properties, data_dir)
            syllabus['properties'] = properties
            syllabus['node'] = syllabus_node
            syllabus['relationship'] = rel
            list_to_check.append(syllabus)
            return list_to_check
    
    def add_scheme_of_work_to_list(label, department, subject, year_groups, topic_created_in_academic_year, list_to_check, node, data_dir):
        scheme_of_work = {}
        if year_groups == 'GCSE' or year_groups == 'A_Level':
            year_label = ''
            year_groups_string = year_groups
        else:
            year_label = 'year_'
            year_groups_string = year_groups
        check_val = f"{department}_{year_label}{year_groups_string}_{subject}_({topic_created_in_academic_year})"
        if check_val not in list_to_check:
            logging.debug(f"Adding {label} '{check_val}' to list.")
            properties = {
                'department': department,
                'subject': subject,
                'year_groups': year_groups,
                'created:': topic_created_in_academic_year # TODO: producer of the scheme of work
            }
            scheme_of_work_node = create_local_curriculum_node_using_labels(session, labels, label, properties, data_dir)
            rel = create_local_curriculum_relationship(session, node, scheme_of_work_node, labels['contains_many_hierarchy_label'], labels, properties, data_dir)
            scheme_of_work['properties'] = properties
            scheme_of_work['node'] = scheme_of_work_node
            scheme_of_work['relationship'] = rel
            list_to_check.append(scheme_of_work)
            return list_to_check
    
    def subject_code_to_name(subject_code):
        if subject_code == 'P':
            subject_name = 'Physics'
        elif subject_code == 'C':
            subject_name = 'Chemistry'
        elif subject_code == 'B':
            subject_name = 'Biology'
        else:
            subject_name = subject_code
        return subject_name
    
    def year_group_to_label(year_group):
        if year_group == 7:
            year_group_label = 'year_7'
        elif year_group == 8:
            year_group_label = 'year_8'
        elif year_group == 9:
            year_group_label = 'year_9'
        elif year_group == 10:
            year_group_label = 'year_10'
        elif year_group == 11:
            year_group_label = 'year_11'
        elif year_group == 12:
            year_group_label = 'year_12'
        elif year_group == 13:
            year_group_label = 'year_13'
        elif year_group == 'G':
            year_group_label = 'GCSE'
        elif year_group == 'A':
            year_group_label = 'A_Level'
        else:
            logging.warning(f"Invalid year group '{year_group}'.")
            year_group_label = year_group
        return year_group_label
    
    def get_learning_stages(topic_dict):
        learning_stages_dict = {}
        learning_stages = []
        for topic in topic_dict:
            learning_stage = topic_dict[topic]['info'].get('TopicKeyStage')
            learning_stages, learning_stage_node, learning_stage_rel = add_to_list_simple(labels['local_learning_stage_node_label'], learning_stage, learning_stages, curriculum_node, data_dir)
            learning_stages_dict[learning_stage] = learning_stage_node
        return learning_stages_dict
    
    def get_year_groups(topic_dict):
        year_groups_dict = {}
        year_groups = []
        for topic in topic_dict:
            year_group = year_group_to_label(topic_dict[topic]['info'].get('TopicYear'))
            year_groups, year_group_node, year_group_rel = add_to_list_simple(labels['local_year_group_node_label'], year_group, year_groups, curriculum_node, data_dir)
            year_groups_dict[year_group] = year_group_node
        return year_groups_dict
    
    def get_subjects(topic_dict):
        subjects_dict = {}
        subjects = []
        for topic in topic_dict:
            subject = subject_code_to_name(topic_dict[topic]['info'].get('TopicSubject'))                
            subjects, subject_node, subject_rel = add_to_list_simple(labels['local_subject_node_label'], subject, subjects, curriculum_node, data_dir)
            subjects_dict[subject] = subject_node
        return subjects_dict
    
    def get_departments(topic_dict):
        departments_dict = {}
        departments = []
        for topic in topic_dict:
            department = topic_dict[topic]['info'].get('TopicDepartment')
            departments, department_node, department_rel = add_to_list_simple(labels['local_department_node_label'], department, departments, curriculum_node, data_dir)
            departments_dict[department] = department_node
        return departments_dict
    
    def get_subject_learning_stages(topic_dict, labels):
        subject_levels_dict = {}
        subject_levels = []
        for topic in topic_dict:
            subject = subject_code_to_name(topic_dict[topic]['info'].get('TopicSubject'))
            level = topic_dict[topic]['info'].get('TopicKeyStage')
            subject_level = f"key_stage_{level}_{subject}"
            subject_levels, subject_level_node, subject_level_rel = add_subject_year_group_or_learning_stage_to_list(labels['local_subject_level_node_label'], labels, subject, level, subject_levels, curriculum_node, data_dir)
            subject_levels_dict[subject_level] = subject_level_node
        return subject_levels_dict
    
    def get_subject_year_groups(topic_dict, labels):
        subject_year_groups_dict = {}
        subject_year_groups = []
        for topic in topic_dict:
            subject = subject_code_to_name(topic_dict[topic]['info'].get('TopicSubject'))
            year_group = topic_dict[topic]['info'].get('TopicYear')
            subject_year_group = f"year_{year_group}_{subject}"
            subject_year_groups, subject_year_group_node, subject_year_group_rel = add_subject_year_group_or_learning_stage_to_list(labels['local_subject_year_group_node_label'], labels, subject, year_group, subject_year_groups, curriculum_node, data_dir)
            subject_year_groups_dict[subject_year_group] = subject_year_group_node
        return subject_year_groups_dict
    
    def create_syllabuses(topic_dict, labels, curriculum_node, data_dir):
        syllabuses_dict = {}
        syllabuses = []
        subject_levels, subject_year_groups = get_subject_learning_stages(topic_dict, labels), get_subject_year_groups(topic_dict, labels)
        for subject_level in subject_levels:
            for topic in topic_dict:
                curriculum = topic_dict[topic]['info'].get('TopicSource')
                group = subject_level
                subject = subject_code_to_name(topic_dict[topic]['info'].get('TopicSubject'))
                syllabuses = add_syllabus_to_list(labels['local_syllabus_node_label'], labels, curriculum, group, subject, syllabuses, curriculum_node, data_dir)
                syllabuses_dict[subject_level] = syllabuses
        for subject_year_group in subject_year_groups:
            for topic in topic_dict:
                curriculum = topic_dict[topic]['info'].get('TopicSource')
                group = subject_year_group
                subject = subject_code_to_name(topic_dict[topic]['info'].get('TopicSubject'))
                syllabuses = add_syllabus_to_list(labels['local_syllabus_node_label'], labels, curriculum, group, subject, syllabuses, curriculum_node, data_dir)
                syllabuses_dict[subject_year_group] = syllabuses
        return syllabuses_dict
    
    def create_schemes_of_works(topic_dict, syllabuses):
        schemes_of_works_dict = {}
        scheme_of_works = []
        created = '2023_2024'
        for topic in topic_dict:
            department = topic_dict[topic]['info'].get('TopicDepartment')
            subject = topic_dict[topic]['info'].get('TopicSubject')
            year_groups = topic_dict[topic]['info'].get('TopicYear')
            for syllabus in syllabuses:
                # if the first character of topic is a digit, it's a year_group scheme, if it's a letter, it's a key_stage scheme
                identifier = topic[0]
                if identifier in syllabus['properties']['syllabus_group']:
                    scheme_of_works = add_scheme_of_work_to_list(labels['local_scheme_of_work_node_label'], department, subject, year_groups, created, scheme_of_works, curriculum_node, data_dir)
                    schemes_of_works_dict[topic] = scheme_of_works
        return schemes_of_works_dict
    
    learning_stages_dict = get_learning_stages(topic_dict)
    year_groups_dict = get_year_groups(topic_dict)
    subjects_dict = get_subjects(topic_dict)
    departments_dict = get_departments(topic_dict)
    subject_learning_stages_dict = get_subject_learning_stages(topic_dict, labels)
    subject_year_groups_dict = get_subject_year_groups(topic_dict, labels)
    syllabuses_dict = create_syllabuses(topic_dict, labels, curriculum_node, data_dir)
    schemes_of_works_dict = create_schemes_of_works(topic_dict, syllabuses_dict)
    
    local_curriculum_dict['learning_stages'] = learning_stages_dict
    local_curriculum_dict['year_groups'] = year_groups_dict
    local_curriculum_dict['subjects'] = subjects_dict
    local_curriculum_dict['departments'] = departments_dict
    local_curriculum_dict['subject_learning_stages'] = subject_learning_stages_dict
    local_curriculum_dict['subject_year_groups'] = subject_year_groups_dict
    local_curriculum_dict['syllabuses'] = syllabuses_dict
    local_curriculum_dict['schemes_of_works'] = schemes_of_works_dict
    return local_curriculum_dict


# %% [markdown]
# #### Initialise the local curriculum

# %%
def initialise_local_curriculum(session, local_curriculum_labels, local_curriculum_options, planner_dataframes, local_curriculum_data_dir=None, local_node=None):
    local_curriculum_init_options = get_local_curriculum_init_options(local_curriculum_options)
    labels = local_curriculum_labels
    options = local_curriculum_init_options
    
    local_curriculum_dict = {}
    
    syllabus_dict = create_local_syllabus_dict(planner_dataframes)
    topic_dict = create_local_topic_level_syllabus_dict(planner_dataframes)
    lesson_dict = create_local_lesson_level_syllabus_dict(planner_dataframes)
    
    if options['create_syllabus_structure'] and not options['create_schemes_of_works']:
        logging.error("Cannot create curriculum structure without creating schemes of works.")
        return ValueError("Initialisation error.")
    if options['create_syllabus_structure']:
        if local_node:
            local_curriculum_node = local_node
        else:
            node_data = options['local_curriculum_name']
            local_curriculum_node = create_local_curriculum_node_using_labels(session, labels, labels['local_curriculum_node_label'], node_data, local_curriculum_data_dir)
            
        local_curriculum = create_local_curriculum_structure(session, labels, syllabus_dict, local_curriculum_node, local_curriculum_data_dir)
        logging.success("Local curriculum nodes created.")
    
    if options['create_scheme_topics']:
        for topic in topic_dict:
            topic_properties = {
                'topic_id': topic,
                'topic_name': topic_dict[topic]['info']['TopicTitle'],
                'topic_created_in_academic_year': '2023-2024', # TODO: Hardcoded for now
                'topic_type': topic_dict[topic]['info']['TopicType'],
                'topic_lessons': topic_dict[topic]['info']['TotalNumberOfLessonsForTopic'],
                'assessment_type': topic_dict[topic]['info']['TopicAssessmentType']
            }
            print(topic_properties)
            print(labels)
            topic_node = create_local_curriculum_node_using_labels(session, labels, labels['local_scheme_topic_node_label'], topic_properties, local_curriculum_data_dir)
            create_local_curriculum_relationship(session, scheme_node, topic_node, labels['contains_many_hierarchy_label'], labels, constraints=True)
            if options['create_scheme_lessons']:
                for lesson in topic_dict[topic]['lessons']:
                    lesson_properties = {
                        'lesson_id': lesson,
                        'lesson_name': topic_dict[topic]['lessons'][lesson]['info']['LessonName'],
                        'lesson_created_in_academic_year': '2023-2024', # TODO: Hardcoded for now
                        'lesson_type': topic_dict[topic]['lessons'][lesson]['info']['LessonType'],
                        'lesson_topic_id': topic
                    }
                    lesson_node = create_local_curriculum_node_using_labels(session, labels['local_scheme_lesson_node_label'], lesson_properties, local_curriculum_data_dir)
                    create_local_curriculum_relationship(session, topic_node, lesson_node, labels['contains_many_hierarchy_label'], labels, constraints=True)
                    if options['create_scheme_statements']:
                        for statement in topic_dict[topic]['lessons'][lesson]['statements']:
                            statement_properties = {
                                'statement_id': statement,
                                'statement_name': topic_dict[topic]['lessons'][lesson]['statements'][statement]['StatementName'],
                                'statement_created_in_academic_year': '2023-2024', # TODO: Hardcoded for now
                                'statement_type': topic_dict[topic]['lessons'][lesson]['statements'][statement]['StatementType'],
                                'statement_lesson_id': lesson
                            }
                            statement_node = create_local_curriculum_node_using_labels(session, labels['local_scheme_statement_node_label'], statement_properties, local_curriculum_data_dir)
                            create_local_curriculum_relationship(session, lesson_node, statement_node, labels['contains_many_hierarchy_label'], labels, constraints=True)
                    if options['create_scheme_resources']:
                        for resource in topic_dict[topic]['lessons'][lesson]['resources']:
                            resource_properties = {
                                'resource_id': resource,
                                'resource_name': topic_dict[topic]['lessons'][lesson]['resources'][resource]['ResourceName'],
                                'resource_created_in_academic_year': '2023-2024', # TODO: Hardcoded for now
                                'resource_type': topic_dict[topic]['lessons'][lesson]['resources'][resource]['ResourceType']
                            }
                            resource_node = create_local_curriculum_node_using_labels(session, labels['local_scheme_resource_node_label'], resource_properties, local_curriculum_data_dir)
                            create_local_curriculum_relationship(session, lesson_node, resource_node, labels['contains_many_hierarchy_label'], labels, constraints=True)
    return True

# %% [markdown]
# ## Application

# %% [markdown]
# ### Initialise databases

# %%
def initialise_database(session, database, data, labels, init_options):
    logging.prod('Initialising database: ' + database)
    def test_initialisation(initialised_python_structure, structure_type, database):
        try:
            initialised_python_structure
        except ValueError:  
            logging.error('Initialisation failed for ' + structure_type + ' in ' + database)
            return False
        else:
            logging.success('Initialisation successful for ' + structure_type + ' in ' + database)
            return True
    if database == os.getenv('LOCAL_CALENDAR_DATABASE'):
        structure_type = 'local_calendar'
        if data is not None:                
            if isinstance(data[0], datetime.date) and isinstance(data[1], datetime.date):
                if data[0] < data[1] or data[0] == data[1]:
                    if str_to_bool(init_options['create_data_directories']):
                        local_calendar_path = os.path.join(dbfs_path, database)
                        if not os.path.exists(local_calendar_path):
                            os.makedirs(local_calendar_path)
                            logging.prod('Creating local calendar at: ' + local_calendar_path)
                    if str_to_bool(init_options['create_init_constraints']):
                        create_local_calendar_node_constraints(session, labels)
                        logging.prod('Created local calendar node constraints.')
                        init = initialise_local_calendar(session, labels, data=data, init_options=init_options, path=local_calendar_path, local_node=None)
                    else:
                        logging.testing('Creating local calendar without node and relationship constraints')
                        init = initialise_local_calendar(session, labels, data=data, init_options=init_options, path=local_calendar_path, local_node=None)
                else:
                    logging.error('Start date must be before end date')
                    init = ValueError('Initialisation data not valid')
            else:
                logging.error('Data must be provided as a tuple of datetime.date objects')
                init = ValueError('Initialisation data not valid')
        else:
            logging.error('Initialisation data not provided')
            init = ValueError('Initialisation data not valid')
    elif database == os.getenv('LOCAL_PLANNER_DATABASE'):
        structure_type = 'local_planner'
        if data is None:
            planner_dataframes = planner.get_excel_sheets(os.getenv('EXCEL_FILE'))
            accessed_labels = get_local_planner_node_and_relationship_labels_using_accessor(labels)
            local_planner_path = os.path.join(dbfs_path, database)
            if not os.path.exists(local_planner_path):
                os.makedirs(local_planner_path)
                logging.prod('Creating local planner at: ' + local_planner_path)
            if str_to_bool(init_options['create_init_constraints']):
                create_local_planner_node_constraints_using_file(session, labels)
                logging.prod('Created local planner node constraints and data directory: ' + local_planner_path)
                init = initialise_local_planner(session, accessed_labels, init_options, planner_dataframes, path=local_planner_path, local_node=None)
            else:
                logging.testing('Creating local planner without node and relationship constraints')
                init = initialise_local_planner(session, accessed_labels, init_options, planner_dataframes, local_planner_path, local_node=None)
        else:
            logging.error('Initialisation data not provided')
            init = ValueError('Initialisation data not valid')
    elif database == os.getenv('LOCAL_CURRICULUM_DATABASE'):
        structure_type = 'local_curriculum'
        if data is None:
            planner_dataframes = planner.get_excel_sheets(os.getenv('EXCEL_FILE'))            
            accessed_labels = get_local_curriculum_node_and_relationship_labels_using_accessor(labels)
            local_curriculum_path = os.path.join(dbfs_path, database)
            if not os.path.exists(local_curriculum_path):
                os.makedirs(local_curriculum_path)
                logging.prod('Creating local curriculum at: ' + local_curriculum_path)
            if str_to_bool(init_options['create_init_constraints']):
                create_local_curriculum_node_constraints_using_file(session, labels)
                logging.prod('Created local curriculum node constraints and data directory: ' + local_curriculum_path)
                init = initialise_local_curriculum(session, accessed_labels, init_options, planner_dataframes,local_curriculum_data_dir=local_curriculum_path, local_node=None)
            else:
                logging.testing('Creating local curriculum without node and relationship constraints')
                init = initialise_local_curriculum(session, accessed_labels, init_options, planner_dataframes, local_curriculum_data_dir=local_curriculum_path, local_node=None)
        else:
            logging.error('Initialisation data not provided')
            init = ValueError('Initialisation data not valid')
    else:
        logging.error('Database not recognised, cannot initialise')
        init = ValueError('Database not recognised')
    if test_initialisation(init, structure_type, database):
        return init
    else:
        return ValueError('Initialisation failed')

def create_database_indexes():
    logging.error('create_database_indexes not implemented')
    pass

# %% [markdown]
# ### Run actions on databases

# %%
def cc_action(session, action, database, data, labels, init_options):
    if action == 'initialise':
        return initialise_database(session, database, data, labels, init_options)
    elif action == 'create_indexes':
        return create_database_indexes()
    else:
        logging.error('Action not recognised')
        return ValueError('Action not recognised')

# %% [markdown]
# ### Access the application

# %%
# Run the app
def cc_app(data=None, path=None, default_options=None):
    def str_to_bool(s):
        return s.lower() == 'true'

    if data is None:
        logging.app('Loading default JSON data')
    if path is None:
        path = os.getenv('DBFS_PATH')
        if not os.path.exists(path):
            os.makedirs(path)
        logging.app('Using default path: ' + path) 
    if default_options is None:
        logging.app('Loading default options...')
        options = load_options_from_file(os.getenv('APP_DEFAULT_OPTIONS_PATH'))
        (options_accessor, access_options_accessor, run_options_accessor,
            init_options_accessor, local_calendar_options_accessor, local_planner_options_accessor, local_curriculum_options_accessor) = get_options_accessor(options)     
        
    # Initialise a Neo4j database with the default options and handle data
    if str_to_bool(init_options_accessor.get('create_default_local_planner') and init_options_accessor.get('create_default_local_calendar')):
        logging.error('Cannot create both a local planner and a local calendar at the same time.')
        raise ValueError('Run options are not valid')
    elif str_to_bool(init_options_accessor.get('create_default_local_calendar')):
        database = os.getenv('LOCAL_CALENDAR_DATABASE')
        init_options = options['init_options']['local_calendar_init_options']
        labels = load_labels_from_file(os.getenv('LOCAL_CALENDAR_LABELS'))
    elif str_to_bool(init_options_accessor.get('create_default_local_planner')):
        database = os.getenv('LOCAL_PLANNER_DATABASE')
        init_options = options['init_options']['local_planner_init_options']
        labels = load_labels_from_file(os.getenv('LOCAL_PLANNER_LABELS'))
    elif str_to_bool(init_options_accessor.get('create_default_local_curriculum')):
        database = os.getenv('LOCAL_CURRICULUM_DATABASE')
        init_options = options['init_options']['local_curriculum_init_options']
        labels = load_labels_from_file(os.getenv('LOCAL_CURRICULUM_LABELS'))
    else:
        logging.error('No valid run options provided.')
        raise ValueError('Run options are not valid')
        
    driver = neo.get_driver()
    with driver.session(database=database) as session:
        if str_to_bool(run_options_accessor.get('init_existing_and_close')):
            logging.app(f'Initialising existing database and then closing session: {database}')
            # Use the existing database
            if str_to_bool(init_options_accessor.get('clear_existing')):
                logging.app(f'Clearing existing database: {database} and deleting all data from path: {path}')
                neo.reset_database(session)
                # Delete all contents within path\{database}
                db_path = os.path.join(path, database)
                if os.path.exists(db_path):
                    shutil.rmtree(db_path)
                initialised_database_python_structure = initialise_database(session, database, data, labels, init_options)
                if initialised_database_python_structure:
                    logging.app('Database initialisation successful for existing database. Closing session.')
                    neo.close_session(session)
                    return initialised_database_python_structure
                else:
                    logging.error('Database initialisation failed for existing database. Closing session.')
                    neo.close_session(session)
                    raise ValueError('Database initialisation failed for existing database')
    neo.close_session(session)
    return ValueError('Database access finished unexpectedly')

# %% [markdown]
# ## Run

# %%
app_data = cc_app()

# %%
import dill

with open('data.pkl', 'wb') as f:
    dill.dump(app_data, f)


