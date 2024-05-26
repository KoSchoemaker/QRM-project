
def getPatientIds(demographicsDataFrame, sleepDataFrame, activityDataFrame):
    # get a list of all patientIds
    patientIds = demographicsDataFrame[['patient_id']].to_numpy().flatten()

    # only consider participants that have both sleep and activity data
    patientIds = [id for id in patientIds if id in sleepDataFrame[['patient_id']].values and id in activityDataFrame[['patient_id']].values]

    # TODO remove participants with less that x sleep data

    return patientIds