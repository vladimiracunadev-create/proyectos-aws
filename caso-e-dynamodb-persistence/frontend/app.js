const apiBaseUrlInput = document.getElementById("apiBaseUrl");
const resultNode = document.getElementById("result");
const form = document.getElementById("orderForm");

const storedBaseUrl = window.localStorage.getItem("case-e-api-base-url") || "";
apiBaseUrlInput.value = storedBaseUrl;

function setResult(payload) {
  resultNode.textContent = JSON.stringify(payload, null, 2);
}

function getBaseUrl() {
  const value = apiBaseUrlInput.value.trim().replace(/\/$/, "");
  window.localStorage.setItem("case-e-api-base-url", value);
  return value;
}

async function request(path, options = {}) {
  const baseUrl = getBaseUrl();
  if (!baseUrl) {
    throw new Error("Debes configurar la API base URL antes de ejecutar consultas.");
  }

  const response = await fetch(`${baseUrl}${path}`, {
    headers: {
      "content-type": "application/json",
    },
    ...options,
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "Error desconocido");
  }

  return payload;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());
  payload.total = Number(payload.total);

  setResult({ status: "Procesando..." });

  try {
    const response = await request("/orders", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    setResult(response);
  } catch (error) {
    setResult({ ok: false, error: error.message });
  }
});

document.querySelectorAll("[data-query]").forEach((button) => {
  button.addEventListener("click", async () => {
    const query = button.dataset.query;
    const customerId = document.getElementById("queryCustomerId").value.trim();
    const status = document.getElementById("queryStatus").value.trim();
    const productId = document.getElementById("queryProductId").value.trim();

    const routes = {
      customer: `/customers/${customerId}/orders`,
      status: `/orders/status/${status}`,
      product: `/products/${productId}/orders`,
    };

    setResult({ status: "Consultando..." });

    try {
      const response = await request(routes[query], { method: "GET" });
      setResult(response);
    } catch (error) {
      setResult({ ok: false, error: error.message });
    }
  });
});
