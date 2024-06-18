import sys
import os
import pandas as pd
import json

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

py_modules_env = sys.path.append(os.getenv("PY_MODULES_PATH"))

import py_modules.setup_dev as dev

def excel_planner_to_json(excel_planner_file=None, json_output_path=None, area=None):
    print_prefix = "DATA> "
    print_prefix = print_prefix + "excel_planner_to_json> "
    json_output_path_append = '/json'
    json_output_file_prepend = 'planner'
    json_output_file_append = '.json'
    env = dev.get_env()
    if area != None:
        print(print_prefix + "Area is not None. Using area: " + area)
        area_env = dev.get_env(area)
    # Check if the excel planner file is None and if so use the default excel planner file
    if excel_planner_file == None:
        print(print_prefix + "No Excel planner file provided. Using default Excel planner file.")
        excel_planner_file = env.dev_planner_excel_file
        print(print_prefix + "Excel planner file: " + excel_planner_file)
    # Load the Excel file
    excel_data = pd.ExcelFile(excel_planner_file)

    # Load individual sheets into dataframes
    topic_lookup_df = pd.read_excel(excel_data, 'TopicLookup')
    lesson_lookup_df = pd.read_excel(excel_data, 'LessonLookup')
    statement_lookup_df = pd.read_excel(excel_data, 'StatementLookup')
    lab_lookup_df = pd.read_excel(excel_data, 'LabLookup')

    # Function to replace NaN with None (or any other value you prefer)
    def replace_nan(value):
        return None if pd.isna(value) else value

    # Initialize the main dictionary to hold topics
    json_data = {}

    # Process each sheet and populate the dictionary
    for _, topic_row in topic_lookup_df.iterrows():
        topic_id = replace_nan(topic_row['TopicID'])
        json_data[topic_id] = {
            'TopicDepartment': replace_nan(topic_row['TopicDepartment']),
            'TopicKeyStage': str(replace_nan(topic_row['TopicKeyStage']))[0],
            'TopicYear': replace_nan(topic_row['TopicYear']),
            'TopicSubject': replace_nan(topic_row['TopicSubject']),
            'TopicID': replace_nan(topic_row['TopicID']),
            'TopicTitle': replace_nan(topic_row['TopicTitleEnter']),
            'TotalNumberOfLessonsForTopic': replace_nan(topic_row['TotalNumberOfLessonsForTopic']),
            'TopicType': replace_nan(topic_row['TopicType']),
            'TopicAssessmentType': replace_nan(topic_row['TopicAssessmentType']),
            'Lessons': {}
        }

        topic_lessons = lesson_lookup_df[lesson_lookup_df['TopicID'] == topic_id]
        for _, lesson_row in topic_lessons.iterrows():
            lesson_id = replace_nan(lesson_row['LessonID'])
            json_data[topic_id]['Lessons'][lesson_id] = {
                'LessonDepartment': replace_nan(topic_row['TopicDepartment']),
                'LessonKeyStage': str(replace_nan(lesson_row['TopicKeyStage']))[0],
                'LessonYear': replace_nan(topic_row['TopicYear']),
                'LessonSubject': replace_nan(topic_row['TopicSubject']),
                'LessonTopicID': replace_nan(topic_row['TopicID']),
                'LessonID': replace_nan(lesson_row['LessonID']),
                'LessonTitle': replace_nan(lesson_row['LessonTitle']),
                'LessonLearningObjective': replace_nan(lesson_row['LessonLearningObjective']),
                'LessonSequence': replace_nan(lesson_row['LessonSequence']),
                'NumberOfPeriodsForLesson': replace_nan(lesson_row['NumberOfPeriodsForLesson']),
                'LearningStatements': [],
                'Labs': []
            }

            lesson_statements = statement_lookup_df[statement_lookup_df['LessonID'] == lesson_id]
            for _, statement_row in lesson_statements.iterrows():
                json_data[topic_id]['Lessons'][lesson_id]['LearningStatements'].append({
                    'LearningOutcomeID': replace_nan(statement_row['LearningOutcomeID']),
                    'LearningOutcomeStatement': replace_nan(statement_row['LearningOutcomeStatement'])
                })

            lesson_labs = lab_lookup_df[lab_lookup_df['LessonID'] == lesson_id]
            for _, lab_row in lesson_labs.iterrows():
                json_data[topic_id]['Lessons'][lesson_id]['Labs'].append({
                    'LabID': replace_nan(lab_row['LabID']),
                    'LabTitle': replace_nan(lab_row['LabTitle']),
                    'LabSummary': replace_nan(lab_row['LabSummary']),
                    'GroupPractical': replace_nan(lab_row['GroupPractical']),
                    'Demo': replace_nan(lab_row['Demo']),
                    'LabSequence': replace_nan(lab_row['LabSequence']),
                    'LabRequirements': replace_nan(lab_row['LabRequirements']),
                    'LabLinks': replace_nan(lab_row['LabLinks']),
                })
    # Convert the dictionary to JSON format and save it
    # Check if the json file path is None and if so create a new json file path
    if json_output_path == None:
        print(print_prefix + "No JSON output path provided. Using default JSON output path.")
        json_output_path = env.dev_output_path + json_output_path_append
        # If the path does not exist, create it
        if not os.path.exists(json_output_path):
            os.makedirs(json_output_path)
        # join the path and the file name
        json_output_filename = json_output_file_prepend + json_output_file_append
        json_output_file = os.path.join(json_output_path, json_output_filename)
    else:
        # join the path and the file name
        print("Using JSON output path: " + json_output_path)
        json_output_filename = json_output_file_prepend + json_output_file_append
        print("Using JSON output filename: " + json_output_filename)
        print("Using JSON output file: " + json_output_path + json_output_filename)
        json_output_file = os.path.join(json_output_path, json_output_filename)
        print("JSON output file: " + json_output_file)
    print(print_prefix + "Saving JSON file: " + json_output_file)
    # if the file exists, delete it
    if os.path.exists(json_output_file):
        os.remove(json_output_file)
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(json_output_file), exist_ok=True)         
    # save the JSON file
    with open(json_output_file, 'w') as file:
        print(print_prefix + "Saving JSON file: " + json_output_file)
        os.makedirs(os.path.dirname(json_output_file), exist_ok=True)
        json.dump(json_data, file, indent=4)
    return json_data

def get_topic_json_from_planner_json_by_id(topic_id, json_input=None, json_output=None, area=None):
    print_prefix = "DATA> "
    print_prefix = print_prefix + "get_topic_json_from_planner_json_by_id> "
    json_output_path_append = '/json/topic'
    json_output_file_prepend = 'topic_'
    json_output_file_append = '.json'
    env = dev.get_env()
    print(print_prefix + "Getting topic by ID ... " + topic_id)
    # Check if the topic_id is None and if so return None
    if topic_id == None:
        print(print_prefix + "Topic ID is None. You must enter a valid topic ID.")
        return None
    # Check if the JSON is None and if so use the default JSON file or the JSON file for the specified area
    if json_input == None:
        if area == None:
            print(print_prefix + "JSON is None and no area chosen. Loading default JSON file.")
            json_file = env.dev_planner_json_file
            print(print_prefix + "JSON file loaded ...")
            print(json_file)
            with open(json_file, 'r') as file:
                print(print_prefix + "Loading JSON file: " + json_file)
                data_json = json.load(file)
        elif area in ["kcar", "kevlarai", "fpgs"]:
            print(print_prefix + "JSON is None. Loading default JSON file or JSON file for area: " + area)
            print(print_prefix + "Not implemented yet. Exiting.")
            #load_dotenv(find_dotenv(area))
            return
    print(print_prefix + "Successfully loaded JSON file ...")
    print(json_input)
    # Check if the topic_id exists in the JSON
    if topic_id in json_input:
        # Save the topic to a JSON file and return the topic
        if json_output != None:
            print(print_prefix + "JSON output is not None. Saving topic to JSON file: " + json_output)
            with open(json_output, 'w') as file:
                print(print_prefix + "Saving JSON file: " + json_output)
                json.dump(json_input[topic_id], file, indent=4)
        else:
            print(print_prefix + "JSON output is None. Saving topic to default JSON file.")
            json_output_path = env.dev_output_path + json_output_path_append
            # If the path does not exist, create it
            if not os.path.exists(json_output_path):
                os.makedirs(json_output_path)
            print(print_prefix + "JSON output path: " + json_output_path)
            print(print_prefix + "JSON output file prepend: " + json_output_file_prepend)
            print(print_prefix + "JSON output file append: " + json_output_file_append)
            json_output_filename = json_output_file_prepend + topic_id + json_output_file_append
            json_output_file = os.path.join(json_output_path, json_output_filename)
            print(print_prefix + "Saving JSON file: " + json_output_file)
            with open(json_output_file, 'w') as file:
                print(print_prefix + "Saving JSON file: " + json_output_file)
                json.dump(json_input[topic_id], file, indent=4)
        return json_input[topic_id]
    else:
        print(print_prefix + "Topic ID does not exist: " + topic_id)
        return None
    
def get_lesson_json_from_topic_json_by_id(lesson_id, json_input=None, area=None):
    print("Using module get_lesson_json_from_topic_json_by_id")
    print_prefix = "DATA> "
    print_prefix = print_prefix + "get_lesson_json_from_topic_json_by_id> "
    json_output_path_append = '/json/lesson'
    json_output_file_prepend = 'lesson_'
    json_output_file_append = '.json'
    env = dev.get_env()
    print(print_prefix + "get_lesson_json_from_topic_json_by_id")
    # Check if the lesson_id is None and if so return None
    if lesson_id == None:
        print(print_prefix + "Lesson ID is None. You must enter a valid lesson ID.")
        return None
    print("Testing...")
    print(lesson_id)
    print(print_prefix + "Getting lesson by ID ... ")
    print(print_prefix + "Lesson ID: " + lesson_id)
    # Check if the JSON is None and if so use the default JSON file or the JSON file for the specified area
    if json_input == None:
        if area == None:
            print(print_prefix + "Lesson area is None, ignoring...")
        elif area in ["kcar", "kevlarai", "fpgs"]:
            print(print_prefix + "JSON is None. Loading default JSON file or JSON file for area: " + area)
            print(print_prefix + "Not implemented yet. Exiting.")
            #load_dotenv(find_dotenv(area))
            return
        else:
            print(print_prefix + "Unknown area: " + area + ". Please specify a valid area or leave the area parameter blank to load the default tools.")
            return
    data_json = json_input
    print(print_prefix + "Successfully loaded JSON file ...")
    print(data_json)
    lessons = data_json.get('Lessons', {})
    print(print_prefix + "Lessons: " + str(lessons))
    for topic_id in data_json.items():
        for current_lesson_id, lesson_info in lessons.items():
            if current_lesson_id == lesson_id:
                print(print_prefix + "Lesson ID exists: " + lesson_id)
                json_output_path = env.dev_output_path + json_output_path_append + lesson_id
                print(json_output_path)   

                if not os.path.exists(json_output_path):
                    os.makedirs(json_output_path)
                json_output_path = env.dev_output_path + json_output_path_append
                json_output_filename = json_output_file_prepend + "/" + lesson_id + json_output_file_append
                json_output_file = os.path.join(json_output_path, json_output_filename)

                with open(json_output_file, 'w') as file:
                    print(print_prefix + "Saving JSON file: " + json_output_file)
                    json.dump(lesson_info, file, indent=4)

                return lesson_info

    print(print_prefix + "Lesson ID does not exist: " + lesson_id)
    # save the lesson to a JSON file and return the lesson
    return None

def get_topic_ids_from_planner_json(json_input=None, area=None):
    print_prefix = "DATA> "
    print_prefix = print_prefix + "get_topic_ids_from_planner_json> "
    env = dev.get_env()
    # Check if the JSON is None and if so use the default JSON file or the JSON file for the specified area
    if json_input == None:
        if area == None:
            print(print_prefix + "JSON is None. Loading default JSON file.")
            json_file = env.dev_planner_json_file
            with open(json_file, 'r') as file:
                print(print_prefix + "Loading JSON file: " + json_file)
                data_json = json.load(file)
        elif area in ["kcar", "kevlarai", "fpgs"]:
            print(print_prefix + "JSON is None. Loading default JSON file or JSON file for area: " + area)
            print(print_prefix + "Not implemented yet. Exiting.")
            #load_dotenv(find_dotenv(area))
            return
    # Get the topic IDs from the JSON
    topic_ids = []
    print(print_prefix + "Getting topic IDs ... ")
    for topic_id, topic_info in json_input.items():
        topic_ids.append(topic_id)
    print(print_prefix + "Topic IDs are .. ")
    return topic_ids

def get_lesson_ids_from_topic_json(topic_json):
    print_prefix = "DATA> "
    print_prefix = print_prefix + "get_lesson_ids_from_topic_json> "
    # Get the lesson IDs from the JSON
    lesson_ids = []
    print(print_prefix + "Getting lesson IDs ... ")
    for lesson_id, lesson_info in topic_json.get('Lessons', {}).items():
        print(print_prefix + "Lesson ID: " + lesson_id)
        print(print_prefix + "Lesson info: " + str(lesson_info))
        lesson_ids.append(lesson_id)
    print(print_prefix + "Lesson IDs are .. ")
    print(lesson_ids)
    return lesson_ids

def get_topics_by_keystage(data_json, key_stage):
    print_prefix = "DATA> "
    print(print_prefix + "Getting topics by key stage ... " + str(key_stage))
    print(str(data_json))
    matching_topics = {}
    for topic_id, topic_info in data_json.items():
        if topic_info.get('TopicKeyStage') == key_stage:
            matching_topics[topic_id] = topic_info
    print(print_prefix + "Matching topics are ... ")
    print(matching_topics)
    return matching_topics

def get_lessons_from_topic_json(data_json):
    print_prefix = "DATA> "
    print(print_prefix + "Getting lessons from topic JSON ...")
    print(print_prefix + str(data_json))
    # Get the TopicID from the JSON
    topic_id = data_json.get('TopicID')
    print(print_prefix + "Topic ID: " + topic_id)
    print(print_prefix + "Getting lessons by topic ID ... " + topic_id)
    # Check if the topic_id is None and if so return None
    if topic_id is None:
        print(print_prefix + "Topic ID is None. The topic JSON is not formatted correctly")
        return None
    # Get the lessons from the JSON
    matching_lessons = {}
    for lesson_id, lesson_info in data_json.get('Lessons', {}).items():
        print(print_prefix + "Lesson ID: " + lesson_id + " has lesson info: " + str(lesson_info))
        matching_lessons[lesson_id] = lesson_info
    return matching_lessons

# Probably unnecessary
def get_core_sequence_lessons_by_topic_id(data_json, topic_id):
    matching_lessons = {}
    for topic, topic_info in data_json.items():
        if topic_info.get('TopicID') == topic_id:
            for lesson_id, lesson_info in topic_info.get('Lessons', {}).items():
                # Check if the lesson sequence is a letter, if not, discard it
                if not lesson_info.get('LessonSequence').isalpha():
                    matching_lessons[lesson_id] = lesson_info
    return matching_lessons

def get_topics_by_year(data_json, year):
    matching_topics = {}
    for topic_id, topic_info in data_json.items():
        if topic_info.get('TopicYear') == year:
            matching_topics[topic_id] = topic_info
    return matching_topics

def get_lessons_by_sequence(data_json, sequence):
    matching_lessons = {}
    for topic_id, topic_info in data_json.items():
        for lesson_id, lesson_info in topic_info.get('Lessons', {}).items():
            if lesson_info.get('LessonSequence') == sequence:
                matching_lessons[lesson_id] = lesson_info
    return matching_lessons

def get_sequence_lessons_by_yeargroup(data_json, yeargroup, sequence):
    print("Getting sequence lessons by yeargroup ... " + yeargroup + " " + sequence)
    matching_lessons = {}
    for topic_id, topic_info in data_json.items():
        print("Topic ID: " + topic_id)
        if topic_info.get('TopicYear') == yeargroup:
            print("Topic year: " + topic_info.get('TopicYear'))
            for lesson_id, lesson_info in topic_info.get('Lessons', {}).items():
                print("Lesson ID: " + lesson_id)
                if lesson_info.get('LessonSequence') == sequence:
                    print("Lesson sequence: " + lesson_info.get('LessonSequence'))
                    matching_lessons[lesson_id] = lesson_info
    return matching_lessons



# TODO: Add a function to convert the Excel file to a ... database?
# def convert_excel_to_planner_db(excel_file_path, other=None):