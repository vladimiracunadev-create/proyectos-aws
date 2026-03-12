const apiBaseUrlInput = document.getElementById("apiBaseUrl");
const payloadInput = document.getElementById("payload");
const output = document.getElementById("output");
const btnHealth = document.getElementById("btnHealth");
const btnPublish = document.getElementById("btnPublish");

function writeResult(title, payload) {
  output.textContent = `${title}\n\n${JSON.stringify(payload, null, 2)}`;
}

async function parseResponse(response) {
  const text = await response.text();

  try {
    return JSON.parse(text);
  } catch (_error) {
    return { raw: text };
  }
}

btnHealth.addEventListener("click", async () => {
  const baseUrl = apiBaseUrlInput.value.trim().replace(/\/$/, "");
  if (!baseUrl) {
    writeResult("Error", { message: "Debes ingresar la API Base URL." });
    return;
  }

  try {
    const response = await fetch(`${baseUrl}/health`);
    const data = await parseResponse(response);
    writeResult("Health check", { status: response.status, data });
  } catch (error) {
    writeResult("Error", { message: error.message });
  }
});

btnPublish.addEventListener("click", async () => {
  const baseUrl = apiBaseUrlInput.value.trim().replace(/\/$/, "");
  if (!baseUrl) {
    writeResult("Error", { message: "Debes ingresar la API Base URL." });
    return;
  }

  let payload;
  try {
    payload = JSON.parse(payloadInput.value);
  } catch (_error) {
    writeResult("Error", { message: "El payload no es JSON valido." });
    return;
  }

  try {
    const response = await fetch(`${baseUrl}/events/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await parseResponse(response);
    writeResult("Publicacion de evento", { status: response.status, data });
  } catch (error) {
    writeResult("Error", { message: error.message });
  }
});
