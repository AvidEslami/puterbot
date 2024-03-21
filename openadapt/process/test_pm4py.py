import pandas
import pm4py

def import_csv():
    event_log = pm4py.format_dataframe(pandas.read_csv(r"C:\Users\avide\Documents\Work\PROJECTS\puterbot\openadapt\process\simpler-example.csv", sep=';'), case_id='case_id',
                                           activity_key='activity', timestamp_key='timestamp')
    num_events = len(event_log)
    num_cases = len(event_log.case_id.unique())
    print("Number of events: {}\nNumber of cases: {}".format(num_events, num_cases))
    return event_log


if __name__ == "__main__":
    log = import_csv()
    bpmn_model = pm4py.discover_bpmn_inductive(log)
    pm4py.view_bpmn(bpmn_model)

    dfg, start_activities, end_activities = pm4py.discover_dfg(log)
    pm4py.view_dfg(dfg, start_activities, end_activities)

    map = pm4py.discover_heuristics_net(log)
    pm4py.view_heuristics_net(map)