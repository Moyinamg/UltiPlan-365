document.addEventListener("DOMContentLoaded", function () {

    // View Tasks search
    const taskSearch = document.getElementById("task-search");

    if (taskSearch) {
        const taskRows = document.querySelectorAll(".view-task-row");
        const searchMessage = document.getElementById("search-message");

        taskSearch.addEventListener("input", function () {
            const searchText = taskSearch.value.toLowerCase().trim();
            let matchingTasks = 0;

            taskRows.forEach(function (taskRow) {
                const taskName = taskRow.dataset.taskName;
                const courseName = taskRow.dataset.course;

                const taskMatches =
                    taskName.includes(searchText) ||
                    courseName.includes(searchText);

                if (taskMatches) {
                    taskRow.style.display = "";
                    matchingTasks += 1;
                } else {
                    taskRow.style.display = "none";
                }
            });

            if (matchingTasks === 0 && searchText !== "") {
                searchMessage.textContent =
                    "No matching tasks found.";
            } else {
                searchMessage.textContent = "";
            }
        });
    }


    // Add Task page
    const taskNameInput = document.getElementById("task-name");
    const taskNameCounter = document.getElementById(
        "task-name-counter"
    );

    if (taskNameInput && taskNameCounter) {
        taskNameInput.addEventListener("input", function () {
            taskNameCounter.textContent =
                taskNameInput.value.length + "/120";
        });
    }


    const priorityCircle = document.getElementById(
        "priority-preview-circle"
    );

    if (priorityCircle) {
        const deadlineInput = document.getElementById("deadline");
        const importanceInput = document.getElementById("importance");
        const difficultyInput = document.getElementById("difficulty");

        const priorityNumber = document.getElementById(
            "priority-preview-number"
        );

        const priorityLabel = document.getElementById(
            "priority-preview-label"
        );

        const priorityMessage = document.getElementById(
            "priority-preview-message"
        );


        // Calculate the number of days before the deadline
        function getDaysLeft(deadlineValue) {
            const deadlineDate = new Date(
                deadlineValue + "T00:00:00"
            );

            const today = new Date();

            today.setHours(0, 0, 0, 0);

            const timeDifference =
                deadlineDate.getTime() - today.getTime();

            return Math.ceil(
                timeDifference / (1000 * 60 * 60 * 24)
            );
        }


        // Use the same scoring system as priority.py
        function calculatePreviewPriority() {
            const deadline = deadlineInput.value;
            const importance = importanceInput.value;
            const difficulty = difficultyInput.value;

            if (!deadline || !importance || !difficulty) {
                showPriorityPreview(
                    0,
                    "Enter task details"
                );

                priorityMessage.textContent =
                    "Select a deadline, importance, and difficulty " +
                    "to see the estimated priority score.";

                return;
            }

            const daysLeft = getDaysLeft(deadline);

            let score = 0;

            // Deadline score
            if (daysLeft === 0) {
                score += 50;
            } else if (daysLeft <= 2) {
                score += 40;
            } else if (daysLeft === 5) {
                score += 30;
            } else if (daysLeft === 7) {
                score += 20;
            } else {
                score += 10;
            }

            // Importance score
            if (importance === "High") {
                score += 30;
            } else if (importance === "Medium") {
                score += 20;
            } else {
                score += 10;
            }

            // Difficulty score
            if (difficulty === "Hard") {
                score += 20;
            } else if (difficulty === "Medium") {
                score += 10;
            } else {
                score += 5;
            }

            let scoreLabel = "Low Priority";

            if (score >= 70) {
                scoreLabel = "High Priority";
            } else if (score >= 45) {
                scoreLabel = "Medium Priority";
            }

            showPriorityPreview(
                score,
                scoreLabel
            );

            priorityMessage.textContent =
                "This is the expected score. The final score is " +
                "calculated again when the task is saved.";
        }


        // Update the number and blue progress circle
        function showPriorityPreview(score, label) {
            let progress = score;

            if (progress > 100) {
                progress = 100;
            }

            priorityNumber.textContent = score;
            priorityLabel.textContent = label;

            priorityCircle.style.background =
                "conic-gradient(" +
                "#2563eb 0%, " +
                "#2563eb " + progress + "%, " +
                "#e5e7eb " + progress + "%, " +
                "#e5e7eb 100%)";
        }


        deadlineInput.addEventListener(
            "change",
            calculatePreviewPriority
        );

        importanceInput.addEventListener(
            "change",
            calculatePreviewPriority
        );

        difficultyInput.addEventListener(
            "change",
            calculatePreviewPriority
        );

        showPriorityPreview(
            0,
            "Enter task details"
        );
    }


    // Real daily progress circle
    const dailyProgressCircle = document.getElementById(
        "daily-progress-circle"
    );

    if (dailyProgressCircle) {
        const progress = Number(
            dailyProgressCircle.dataset.progress
        );

        dailyProgressCircle.style.background =
            "conic-gradient(" +
            "#2563eb 0%, " +
            "#2563eb " + progress + "%, " +
            "#e5e7eb " + progress + "%, " +
            "#e5e7eb 100%)";
    }


    // Focus First timer
    const timerDisplay = document.getElementById(
        "focus-timer-display"
    );

    const timerCircle = document.getElementById(
        "focus-timer-circle"
    );

    // Only run the remaining code on Focus First
    if (!timerDisplay || !timerCircle) {
        return;
    }

    const taskDataElement = document.getElementById(
        "focus-task-data"
    );

    const focusTasks = JSON.parse(
        taskDataElement.textContent
    );

    const startButton = document.getElementById(
        "start-focus-button"
    );

    const resetButton = document.getElementById(
        "reset-focus-button"
    );

    const skipTaskButton = document.getElementById(
        "skip-task-button"
    );

    const timerMessage = document.getElementById(
        "focus-timer-message"
    );

    const timerModeText = document.getElementById(
        "focus-timer-mode"
    );

    const methodButtons = document.querySelectorAll(
        ".focus-method-button"
    );

    const useBreaksCheckbox = document.getElementById(
        "use-breaks-checkbox"
    );

    const taskContent = document.getElementById(
        "focus-task-content"
    );

    const emptyTask = document.getElementById(
        "focus-empty-task"
    );

    const timerCard = document.getElementById(
        "focus-timer-card"
    );

    const taskName = document.getElementById(
        "focus-task-name"
    );

    const taskCourse = document.getElementById(
        "focus-task-course"
    );

    const taskDeadline = document.getElementById(
        "focus-task-deadline"
    );

    const taskEstimatedTime = document.getElementById(
        "focus-task-estimated-time"
    );

    const taskImportance = document.getElementById(
        "focus-task-importance"
    );

    const taskDifficulty = document.getElementById(
        "focus-task-difficulty"
    );

    const taskPriorityScore = document.getElementById(
        "focus-priority-score"
    );

    const taskPosition = document.getElementById(
        "focus-task-position"
    );

    const taskProgressText = document.getElementById(
        "focus-task-progress-text"
    );

    const taskProgressFill = document.getElementById(
        "focus-progress-fill"
    );

    const completionPopup = document.getElementById(
        "focus-complete-popup"
    );

    const popupMessage = document.getElementById(
        "focus-popup-message"
    );

    const continueWorkingButton = document.getElementById(
        "continue-working-button"
    );

    const nextTaskButton = document.getElementById(
        "next-task-button"
    );

    let currentTaskIndex = 0;

    let selectedMinutes = 25;
    let selectedBreakMinutes = 5;

    let totalSessionSeconds = selectedMinutes * 60;
    let timeRemaining = totalSessionSeconds;

    let taskWorkedSeconds = 0;
    let taskTargetSeconds = 0;

    let timerInterval = null;
    let timerIsRunning = false;
    let timerMode = "focus";
    let workingPastGoal = false;


    function updateTimerDisplay() {
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;

        timerDisplay.textContent =
            String(minutes).padStart(2, "0") +
            ":" +
            String(seconds).padStart(2, "0");

        updateTimerCircle();
    }


    function updateTimerCircle() {
        let progressPercent = 0;

        if (totalSessionSeconds > 0) {
            const timeUsed =
                totalSessionSeconds - timeRemaining;

            progressPercent =
                (timeUsed / totalSessionSeconds) * 100;
        }

        let progressColor = "#2563eb";

        if (timerMode === "break") {
            progressColor = "#22a447";
        }

        timerCircle.style.background =
            "conic-gradient(" +
            progressColor + " 0%, " +
            progressColor + " " + progressPercent + "%, " +
            "#e5e7eb " + progressPercent + "%, " +
            "#e5e7eb 100%)";
    }


    function updateTaskProgress() {
        if (focusTasks.length === 0) {
            taskProgressText.textContent =
                "0 of 0 minutes";

            taskProgressFill.style.width = "0%";
            return;
        }

        const workedMinutes = Math.floor(
            taskWorkedSeconds / 60
        );

        const targetMinutes = Math.floor(
            taskTargetSeconds / 60
        );

        taskProgressText.textContent =
            workedMinutes +
            " of " +
            targetMinutes +
            " minutes";

        let progressPercent =
            (taskWorkedSeconds / taskTargetSeconds) * 100;

        if (progressPercent > 100) {
            progressPercent = 100;
        }

        taskProgressFill.style.width =
            progressPercent + "%";
    }


    function displayCurrentTask() {
        if (focusTasks.length === 0) {
            taskContent.hidden = true;
            emptyTask.hidden = false;
            timerCard.classList.add(
                "disabled-focus-timer"
            );

            taskPosition.textContent = "No tasks";
            taskPriorityScore.textContent = "";

            return;
        }

        const currentTask =
            focusTasks[currentTaskIndex];

        taskContent.hidden = false;
        emptyTask.hidden = true;

        timerCard.classList.remove(
            "disabled-focus-timer"
        );

        taskName.textContent =
            currentTask.task_name;

        taskCourse.textContent =
            currentTask.course;

        taskDeadline.textContent =
            currentTask.deadline;

        taskEstimatedTime.textContent =
            currentTask.estimated_minutes +
            " minutes";

        taskImportance.textContent =
            currentTask.importance;

        taskDifficulty.textContent =
            currentTask.difficulty;

        taskPriorityScore.textContent =
            "Priority Score: " +
            currentTask.priority_score;

        taskPosition.textContent =
            "Task " +
            (currentTaskIndex + 1) +
            " of " +
            focusTasks.length;

        taskTargetSeconds =
            Number(currentTask.estimated_minutes) * 60;

        taskWorkedSeconds = 0;
        workingPastGoal = false;

        prepareFocusSession();
        updateTaskProgress();
    }


    function prepareFocusSession() {
        clearInterval(timerInterval);

        timerIsRunning = false;
        timerMode = "focus";

        totalSessionSeconds =
            selectedMinutes * 60;

        timeRemaining =
            totalSessionSeconds;

        timerModeText.textContent =
            "Focus Time";

        startButton.textContent =
            "▶ Start Focus";

        timerMessage.textContent =
            selectedMinutes +
            "-minute focus session ready.";

        updateTimerDisplay();
    }


    function prepareBreak() {
        clearInterval(timerInterval);

        timerIsRunning = false;
        timerMode = "break";

        totalSessionSeconds =
            selectedBreakMinutes * 60;

        timeRemaining =
            totalSessionSeconds;

        timerModeText.textContent =
            "Break Time";

        startButton.textContent =
            "▶ Start Break";

        timerMessage.textContent =
            "Your focus session is complete. A " +
            selectedBreakMinutes +
            "-minute break is ready.";

        updateTimerDisplay();
    }


    function startOrPauseTimer() {
        if (focusTasks.length === 0) {
            timerMessage.textContent =
                "Add a task before starting the timer.";

            return;
        }

        if (timerIsRunning) {
            clearInterval(timerInterval);

            timerIsRunning = false;
            startButton.textContent =
                "▶ Continue";

            if (timerMode === "focus") {
                timerMessage.textContent =
                    "Your focus session is paused.";
            } else {
                timerMessage.textContent =
                    "Your break is paused.";
            }

            return;
        }

        timerIsRunning = true;
        startButton.textContent = "Ⅱ Pause";

        if (timerMode === "focus") {
            timerMessage.textContent =
                "Stay focused. You are making progress.";
        } else {
            timerMessage.textContent =
                "Take a short break and return refreshed.";
        }

        timerInterval = setInterval(function () {
            timeRemaining -= 1;

            if (timerMode === "focus") {
                taskWorkedSeconds += 1;
                updateTaskProgress();

                if (
                    taskWorkedSeconds >= taskTargetSeconds &&
                    workingPastGoal === false
                ) {
                    showTaskCompletePopup();
                    return;
                }
            }

            updateTimerDisplay();

            if (timeRemaining <= 0) {
                finishCurrentSession();
            }
        }, 1000);
    }


    function finishCurrentSession() {
        clearInterval(timerInterval);

        timerIsRunning = false;
        timeRemaining = 0;

        updateTimerDisplay();

        if (timerMode === "break") {
            prepareFocusSession();

            timerMessage.textContent =
                "Your break is finished. Start your next focus session.";

            return;
        }

        if (useBreaksCheckbox.checked) {
            prepareBreak();
        } else {
            prepareFocusSession();

            timerMessage.textContent =
                "Focus session finished. Start another session when ready.";
        }
    }


    function showTaskCompletePopup() {
        clearInterval(timerInterval);

        timerIsRunning = false;

        const currentTask =
            focusTasks[currentTaskIndex];

        popupMessage.textContent =
            "You completed the planned " +
            currentTask.estimated_minutes +
            " minutes for " +
            currentTask.task_name +
            ". Would you like to continue or move to the next task?";

        completionPopup.hidden = false;
    }


    function moveToNextTask() {
        clearInterval(timerInterval);

        timerIsRunning = false;
        completionPopup.hidden = true;

        if (focusTasks.length === 0) {
            return;
        }

        currentTaskIndex += 1;

        if (currentTaskIndex >= focusTasks.length) {
            currentTaskIndex = 0;

            timerMessage.textContent =
                "You reached the end of your task list.";
        }

        displayCurrentTask();
    }


    methodButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            clearInterval(timerInterval);

            timerIsRunning = false;

            selectedMinutes = Number(
                button.dataset.minutes
            );

            selectedBreakMinutes = Number(
                button.dataset.break
            );

            methodButtons.forEach(
                function (methodButton) {
                    methodButton.classList.remove(
                        "active-method"
                    );
                }
            );

            button.classList.add(
                "active-method"
            );

            prepareFocusSession();
        });
    });


    startButton.addEventListener(
        "click",
        startOrPauseTimer
    );


    resetButton.addEventListener("click", function () {
        clearInterval(timerInterval);

        timerIsRunning = false;

        if (timerMode === "break") {
            totalSessionSeconds =
                selectedBreakMinutes * 60;
        } else {
            totalSessionSeconds =
                selectedMinutes * 60;
        }

        timeRemaining =
            totalSessionSeconds;

        if (timerMode === "break") {
            startButton.textContent =
                "▶ Start Break";
        } else {
            startButton.textContent =
                "▶ Start Focus";
        }

        timerMessage.textContent =
            "The current timer has been reset.";

        updateTimerDisplay();
    });


    skipTaskButton.addEventListener(
        "click",
        function () {
            moveToNextTask();

            timerMessage.textContent =
                "Task skipped. Your next priority task is ready.";
        }
    );


    continueWorkingButton.addEventListener(
        "click",
        function () {
            completionPopup.hidden = true;
            workingPastGoal = true;

            prepareFocusSession();

            timerMessage.textContent =
                "Extra focus time is ready.";
        }
    );


    nextTaskButton.addEventListener(
        "click",
        function () {
            moveToNextTask();

            timerMessage.textContent =
                "Great work. Your next priority task is ready.";
        }
    );

    displayCurrentTask();
});