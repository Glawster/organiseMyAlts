from src.widgets.weeklyPanel import WeeklyPanel


def testWeeklyPanelShowsEmptyStateWhenNoTasksRemain(qtbot):
    panel = WeeklyPanel()
    qtbot.addWidget(panel)

    panel.updateTasks([])

    assert panel.tasksLabel.text() == "No weekly tasks remaining"
