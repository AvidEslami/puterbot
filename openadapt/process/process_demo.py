""" Retrieves screenshot + action + window title data from the recording database then processes it into a format that can be used by pm4py. """
import pm4py
import tempfile
import pandas
from PIL import Image
from openadapt.db.crud import get_latest_recording, get_recording
from openadapt.events import get_events
from openadapt.utils import (
    EMPTY,
    configure_logging,
    display_event,
    image2utf8,
    plot_performance,
    row2dict,
    rows2dicts,
)
from openadapt.adapters.claude import create_payload, get_completion, prompt

def load_data():
    """ Loads the screenshot + action + window title data from the recording database. """
    recording = get_latest_recording()
    action_events = get_events(recording, process=True)
    processed_image_sequence = []
    for event in action_events:
        processed_image_sequence.append(display_event(event))
        # image.show()

    return processed_image_sequence

def generate_descriptions(images):
    """ Generates action descriptions from the processed screenshots using the Claude API. """
    prompt_string = "What action is being performed by the user in the screenshot? (Answer very briefly)"
    descriptions = []
    for image in images:
        new_width = int(image.width * 0.5)
        new_height = int(image.height * 0.5)
        img_resized = image.resize((new_width, new_height), Image.ANTIALIAS)
        base64_image = image2utf8(img_resized)

        description = prompt(prompt_string, base64_image)
        descriptions.append(description)
    return descriptions

def setup_csv(descriptions):
    """ Sets up the CSV file for pm4py.py to display. """
    # Desired format: case_id=1, activity=description, timestamp=1,2,3,...,n, costs=0, resource=Agent
    csv = []

    # HEADER: case_id;activity;timestamp;costs;resource
    csv.append("case_id;activity;timestamp;costs;resource")
    for i, description in enumerate(descriptions):
        # Seperate entries with a semicolon instead of a comma in a string
        csv.append("1;{};2010-12-30 14:32:00+01:0{};0;Agent".format(description, i+1))
    # Save to a CSV file in this directory (process.csv), later change to a temporary file
    temp_csv_path = "process.csv"
    with open(temp_csv_path, "w") as file:
        file.write("\n".join(csv))
    # Return the path to the temporary CSV file
    return temp_csv_path

def display_process(csv_path):
    """ Displays the process using pm4py. """
    # Load the CSV file
    event_log = pm4py.format_dataframe(pandas.read_csv(csv_path, sep=";"), case_id="case_id", activity_key="activity", timestamp_key="timestamp")
    # Display the process
    bpmn_model = pm4py.discover_bpmn_inductive(event_log)
    pm4py.view_bpmn(bpmn_model)



if __name__ == "__main__":
    images = load_data()
    descriptions = generate_descriptions(images)
    csv_path = setup_csv(descriptions)
    display_process(csv_path)
