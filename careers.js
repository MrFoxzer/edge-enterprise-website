(function (root, factory) {
    const api = factory();
    if (typeof module !== "undefined" && module.exports) module.exports = api;
    if (root) root.EdgeCareers = api;
})(typeof window !== "undefined" ? window : null, function () {
    const MAX_RESUME_SIZE = 5 * 1024 * 1024;
    const allowedTypes = new Set([
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]);
    const allowedExtensions = new Set(["pdf", "doc", "docx"]);

    function validateResume(file) {
        if (!file) return { valid: false, error: "Please attach your résumé." };
        if (file.size > MAX_RESUME_SIZE) return { valid: false, error: "Résumé must be 5 MB or smaller." };
        const extension = (file.name || "").split(".").pop().toLowerCase();
        const allowed = allowedTypes.has(file.type) || (!file.type && allowedExtensions.has(extension));
        return allowed ? { valid: true, error: "" } : { valid: false, error: "Upload a PDF, DOC, or DOCX résumé." };
    }

    function setResumeError(errorRegion, input, result) {
        errorRegion.textContent = result.error;
        input.setCustomValidity(result.error);
    }

    if (typeof document !== "undefined") {
        document.addEventListener("DOMContentLoaded", function () {
            const form = document.querySelector(".application-form");
            const input = document.querySelector("#resume");
            const errorRegion = document.querySelector("#resume-error");
            if (!form || !input || !errorRegion) return;

            const validateInput = function () {
                const result = validateResume(input.files && input.files[0]);
                setResumeError(errorRegion, input, result);
                return result;
            };

            input.addEventListener("change", validateInput);
            input.addEventListener("invalid", validateInput);
            form.addEventListener("submit", function (event) {
                const result = validateInput();
                if (!result.valid) event.preventDefault();
            });
        });
    }

    return { validateResume };
});
