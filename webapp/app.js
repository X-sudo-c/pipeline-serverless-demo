const storageKey = "pipeline_serverless_demo_api_url";

function getApiUrl() {
  return localStorage.getItem(storageKey) || "";
}

function setApiUrl(url) {
  localStorage.setItem(storageKey, url);
}

function showSavedNote(text) {
  const note = document.getElementById("savedNote");
  note.textContent = text;
  setTimeout(() => (note.textContent = ""), 2000);
}

async function callApi(url) {
  const result = document.getElementById("result");
  result.textContent = "Calling...";
  try {
    const resp = await fetch(url, { method: "GET" });
    const contentType = resp.headers.get("content-type") || "";
    let bodyText;
    if (contentType.includes("application/json")) {
      const json = await resp.json();
      bodyText = JSON.stringify(json, null, 2);
    } else {
      bodyText = await resp.text();
    }
    result.textContent = `Status: ${resp.status}\n\n${bodyText}`;
  } catch (err) {
    result.textContent = `Error: ${err?.message || String(err)}`;
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("apiUrlInput");
  const saveBtn = document.getElementById("saveBtn");
  const callBtn = document.getElementById("callBtn");

  input.value = getApiUrl();

  saveBtn.addEventListener("click", () => {
    const url = input.value.trim();
    if (!url) {
      showSavedNote("Please enter a valid URL.");
      return;
    }
    setApiUrl(url);
    showSavedNote("Saved ✔");
  });

  callBtn.addEventListener("click", () => {
    const url = input.value.trim() || getApiUrl();
    if (!url) {
      showSavedNote("Set the API URL first.");
      return;
    }
    callApi(url);
  });
});


