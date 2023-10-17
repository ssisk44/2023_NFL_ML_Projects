from controllers.modelTrainingController import trainSingleGameModelScheduleData

model = trainSingleGameModelScheduleData('scheduleV1', "singleGame", "2002-06-01", "2023-06-01", [])
model.handleTrainingRequest()
