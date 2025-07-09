document.addEventListener("DOMContentLoaded", () => {
    const simpleForm = document.getElementById("simple-form");
    const advancedForm = document.getElementById("advanced-form");
    const btnSimple = document.getElementById("btn-simple");
    const btnAdvanced = document.getElementById("btn-advanced");
    const mockList = document.getElementById("mock-list");

    if (btnSimple && btnAdvanced) {
        btnSimple.addEventListener("click", () => {
            simpleForm.style.display = "block";
            advancedForm.style.display = "none";
            btnSimple.classList.add("active");
            btnAdvanced.classList.remove("active");
        });

        btnAdvanced.addEventListener("click", () => {
            simpleForm.style.display = "none";
            advancedForm.style.display = "block";
            btnSimple.classList.remove("active");
            btnAdvanced.classList.add("active");
        });
    }

    function validateJSONField(field) {
        try {
            if (!field.value.trim()) return true;
            JSON.parse(field.value);
            field.classList.remove("invalid");
            return true;
        } catch (err) {
            field.classList.add("invalid");
            return false;
        }
    }

    function applyJSONValidationTo(fieldId) {
        const field = document.getElementById(fieldId);
        field.addEventListener("input", () => validateJSONField(field));
    }

    ["adv_query_params", "adv_body_params", "adv_headers", "adv_response_body"].forEach(applyJSONValidationTo);

    // 🟩 Formulario simple
    simpleForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const mensaje = document.getElementById("mensaje").value;
        const delay = parseInt(document.getElementById("delay_ms").value || "0", 10);

        const body = {
            path: `/mock/simple-${Date.now()}`,
            method: "GET",
            query_params: {},
            body_params: {},
            headers: {},
            response_status: 200,
            response_body: { mensaje },
            content_type: "application/json",
            delay_ms: delay,
        };

        try {
            const res = await fetch("/configure-mock", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });

            if (res.ok) {
                simpleForm.reset();
                fetchMocks();
            } else {
                alert("Error al guardar el mock");
            }
        } catch (err) {
            console.error(err);
        }
    });

    // 🟦 Botón de mock automático
    const autoBtn = document.getElementById("auto-generate");
    if (autoBtn) {
        autoBtn.addEventListener("click", async () => {
            const mensaje = `Respuesta automática ${Date.now()}`;
            const body = {
                path: `/mock/auto-${Date.now()}`,
                method: "GET",
                query_params: {},
                body_params: {},
                headers: {},
                response_status: 200,
                response_body: { mensaje },
                content_type: "application/json",
                delay_ms: 0,
            };

            try {
                const res = await fetch("/configure-mock", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(body),
                });

                if (res.ok) fetchMocks();
                else alert("Error al generar mock automático");
            } catch (err) {
                console.error(err);
            }
        });
    }

    // 🟨 Formulario avanzado
    advancedForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const fieldsToCheck = [
            "adv_query_params",
            "adv_body_params",
            "adv_headers",
            "adv_response_body",
        ];

        const allValid = fieldsToCheck.every((id) => validateJSONField(document.getElementById(id)));
        if (!allValid) {
            alert("Corrige los errores de JSON antes de continuar.");
            return;
        }

        const parseField = (field) => {
            try {
                return field.value.trim() ? JSON.parse(field.value) : {};
            } catch {
                return {};
            }
        };

        const body = {
            path: document.getElementById("adv_path").value,
            method: document.getElementById("adv_method").value,
            query_params: parseField(document.getElementById("adv_query_params")),
            body_params: parseField(document.getElementById("adv_body_params")),
            headers: parseField(document.getElementById("adv_headers")),
            response_status: parseInt(document.getElementById("adv_status").value),
            response_body: parseField(document.getElementById("adv_response_body")),
            content_type: document.getElementById("adv_content_type").value,
            delay_ms: parseInt(document.getElementById("adv_delay_ms").value || "0", 10),
        };

        try {
            const res = await fetch("/configure-mock", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });

            if (res.ok) {
                advancedForm.reset();
                fetchMocks();
            } else {
                alert("Error al guardar mock avanzado");
            }
        } catch (err) {
            console.error(err);
        }
    });

    // 📦 Lista de mocks
    async function fetchMocks() {
        try {
            const res = await fetch("/configure-mock");
            const mocks = await res.json();

            mockList.innerHTML = "";
            mocks.forEach((mock) => {
                const div = document.createElement("div");
                div.className = "mock-card";

                const details = `
                    <details>
                        <summary>Detalles</summary>
                        <pre><strong>Query:</strong> ${JSON.stringify(mock.query_params, null, 2)}</pre>
                        <pre><strong>Body:</strong> ${JSON.stringify(mock.body_params, null, 2)}</pre>
                        <pre><strong>Headers:</strong> ${JSON.stringify(mock.headers, null, 2)}</pre>
                    </details>
                `;

                div.innerHTML = `
                    <strong>${mock.method} ${mock.path}</strong><br>
                    Retardo: ${mock.delay_ms}ms<br>
                    <pre>${JSON.stringify(mock.response_body, null, 2)}</pre>
                    ${details}
                    <button data-id="${mock.id}" class="delete-btn">Eliminar</button>
                `;

                mockList.appendChild(div);
            });

            document.querySelectorAll(".delete-btn").forEach((btn) => {
                btn.addEventListener("click", async () => {
                    const id = btn.getAttribute("data-id");
                    const res = await fetch(`/configure-mock/${id}`, {
                        method: "DELETE",
                    });
                    if (res.ok) fetchMocks();
                    else alert("Error al eliminar mock");
                });
            });

        } catch (err) {
            console.error("Error al cargar mocks", err);
        }
    }

    fetchMocks();
});
