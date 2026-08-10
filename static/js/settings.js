// UltiPlan 365 settings

document.addEventListener("DOMContentLoaded", function () {
    const themeSetting = document.getElementById("theme-setting");
    const textSizeSetting = document.getElementById(
        "text-size-setting"
    );
    const focusMethodSetting = document.getElementById(
        "focus-method-setting"
    );
    const breakSetting = document.getElementById("break-setting");
    const motionSetting = document.getElementById("motion-setting");
    const resetButton = document.getElementById(
        "reset-settings-button"
    );
    const settingsStatus = document.getElementById("settings-status");

    // Load saved preferences or use the starting choices
    const savedTheme =
        localStorage.getItem("ultiplanTheme") || "light";

    const savedTextSize =
        localStorage.getItem("ultiplanTextSize") || "normal";

    const savedFocusMethod =
        localStorage.getItem("ultiplanFocusMethod") || "25";

    const savedBreakSetting =
        localStorage.getItem("ultiplanBreaks") !== "false";

    const savedMotionSetting =
        localStorage.getItem("ultiplanReduceMotion") === "true";


    // Apply appearance preferences to every page
    function applyAppearanceSettings() {
        document.body.classList.toggle(
            "dark-theme",
            savedTheme === "dark"
        );

        document.body.classList.toggle(
            "large-text-theme",
            savedTextSize === "large"
        );

        document.body.classList.toggle(
            "reduce-motion-theme",
            savedMotionSetting
        );
    }

    applyAppearanceSettings();


    // Apply saved Focus First preferences
    const focusMethodButtons = document.querySelectorAll(
        ".focus-method-button"
    );

    focusMethodButtons.forEach(function (button) {
        if (button.dataset.minutes === savedFocusMethod) {
            button.click();
        }
    });

    const focusBreakCheckbox = document.getElementById(
        "use-breaks-checkbox"
    );

    if (focusBreakCheckbox) {
        focusBreakCheckbox.checked = savedBreakSetting;
    }


    // Stop here when the user is not on the Settings page
    if (
        !themeSetting ||
        !textSizeSetting ||
        !focusMethodSetting ||
        !breakSetting ||
        !motionSetting
    ) {
        return;
    }


    // Display the saved choices
    themeSetting.value = savedTheme;
    textSizeSetting.value = savedTextSize;
    focusMethodSetting.value = savedFocusMethod;
    breakSetting.checked = savedBreakSetting;
    motionSetting.checked = savedMotionSetting;


    function showSavedMessage() {
        settingsStatus.textContent =
            "Your preferences have been saved.";

        setTimeout(function () {
            settingsStatus.textContent =
                "Changes are saved when you select them.";
        }, 2000);
    }


    // Save the theme
    themeSetting.addEventListener("change", function () {
        localStorage.setItem(
            "ultiplanTheme",
            themeSetting.value
        );

        document.body.classList.toggle(
            "dark-theme",
            themeSetting.value === "dark"
        );

        showSavedMessage();
    });


    // Save the text size
    textSizeSetting.addEventListener("change", function () {
        localStorage.setItem(
            "ultiplanTextSize",
            textSizeSetting.value
        );

        document.body.classList.toggle(
            "large-text-theme",
            textSizeSetting.value === "large"
        );

        showSavedMessage();
    });


    // Save the default focus method
    focusMethodSetting.addEventListener("change", function () {
        localStorage.setItem(
            "ultiplanFocusMethod",
            focusMethodSetting.value
        );

        showSavedMessage();
    });


    // Save the break preference
    breakSetting.addEventListener("change", function () {
        localStorage.setItem(
            "ultiplanBreaks",
            breakSetting.checked
        );

        showSavedMessage();
    });


    // Save the reduce-motion preference
    motionSetting.addEventListener("change", function () {
        localStorage.setItem(
            "ultiplanReduceMotion",
            motionSetting.checked
        );

        document.body.classList.toggle(
            "reduce-motion-theme",
            motionSetting.checked
        );

        showSavedMessage();
    });


    // Return all choices to their starting values
    resetButton.addEventListener("click", function () {
        localStorage.removeItem("ultiplanTheme");
        localStorage.removeItem("ultiplanTextSize");
        localStorage.removeItem("ultiplanFocusMethod");
        localStorage.removeItem("ultiplanBreaks");
        localStorage.removeItem("ultiplanReduceMotion");

        themeSetting.value = "light";
        textSizeSetting.value = "normal";
        focusMethodSetting.value = "25";
        breakSetting.checked = true;
        motionSetting.checked = false;

        document.body.classList.remove("dark-theme");
        document.body.classList.remove("large-text-theme");
        document.body.classList.remove("reduce-motion-theme");

        settingsStatus.textContent =
            "Your preferences have been reset.";
    });
});